import csv
import argparse

class Process:
    def __init__(self, name, arrival_time, service_time):
        self.name = name
        self.arrival_time = arrival_time
        self.service_time = service_time
        self.start_time = None
        self.finish_time = None
        self.turnaround_time = None
        self.normalized_turnaround_time = None
        self.initial_service_time = service_time

class Scheduler:
    def __init__(self, scheduler_type, quantum=None):
        self.scheduler_type = scheduler_type
        self.quantum = quantum
        self.clock = 0
        self.ready_queue = []
        self.current_process = None
        self.finished_processes = []

    def handle_arrivals(self, processes):
        for process in processes[:]:
            if process.arrival_time == self.clock:
                self.ready_queue.append(process)
                processes.remove(process)

    def handle_io_bursts(self):
        pass

    def tick(self):
        self.clock += 1

    def check_current_process(self):
        if self.scheduler_type in ["FF", "SP", "SR", "HR"]:
            if self.ready_queue:
                self.current_process = self.ready_queue.pop(0)
        elif self.scheduler_type == "RR":
            if self.ready_queue:
                self.current_process = self.ready_queue.pop(0)
            else:
                self.current_process = None
        elif self.scheduler_type == "FB":
            if self.ready_queue:
                self.current_process = self.ready_queue.pop(0)
                if self.current_process.quantum == 1:
                    self.current_process.quantum = 2
                else:
                    self.ready_queue.append(self.current_process)
                    self.current_process = None
            else:
                self.current_process = None

    def run_scheduler(self, processes):
        while processes or self.ready_queue or self.current_process:
            self.handle_arrivals(processes)
            self.handle_io_bursts()
            self.tick()
            
            if self.current_process is None and self.ready_queue:
                self.check_current_process()

            if self.current_process:
                if self.current_process.start_time is None:
                    self.current_process.start_time = self.clock

                self.current_process.service_time -= 1
                if self.current_process.service_time == 0:
                    self.current_process.finish_time = self.clock
                    self.current_process.turnaround_time = self.current_process.finish_time - self.current_process.arrival_time
                    self.current_process.normalized_turnaround_time = self.current_process.turnaround_time / self.current_process.initial_service_time
                    self.finished_processes.append(self.current_process)
                    self.current_process = None
            else:
                self.check_current_process()

def write_results_to_csv(output_file, processes, mean_turnaround_time, mean_normalized_turnaround_time):
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)

        # writing process data
        for process in processes:
            writer.writerow([process.name, process.arrival_time, process.service_time,
                             process.start_time, process.finish_time, process.turnaround_time,
                             process.normalized_turnaround_time])

        # writing mean statistics
        writer.writerow([mean_turnaround_time, mean_normalized_turnaround_time])

def main(args):
    input_file = args.input_file
    output_file = args.output_file

    processes = []

    # reading input from .csv file
    with open(input_file, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            name, arrival_time, service_time = row
            if arrival_time and service_time:  # Checking for empty data
                processes.append(Process(name, int(arrival_time), int(service_time)))

    # scheduler initialization
    scheduler = Scheduler(args.scheduler_type, args.quantum)

    # run the scheduler
    scheduler.run_scheduler(processes)

    
    total_turnaround_time = sum(process.turnaround_time for process in scheduler.finished_processes)
    mean_turnaround_time = total_turnaround_time / len(scheduler.finished_processes)
    total_normalized_turnaround_time = sum(process.normalized_turnaround_time for process in scheduler.finished_processes)
    mean_normalized_turnaround_time = total_normalized_turnaround_time / len(scheduler.finished_processes)

    # write results to .csv file
    write_results_to_csv(output_file, scheduler.finished_processes, mean_turnaround_time, mean_normalized_turnaround_time)

    

   

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--scheduler_type")
    parser.add_argument("-q", "--quantum")
    parser.add_argument("input_file")
    parser.add_argument("output_file")
    args = parser.parse_args()
    main(args)
