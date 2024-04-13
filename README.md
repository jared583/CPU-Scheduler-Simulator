# CPU-Scheduler-Simulator

Jared Ovokaitys
4/11/2024

run:
(main) $ python3 main.py -s FF -q 2 input.csv output.csv

Warnings: None

Example input:

"A",0,3
"B",2,6
,3,2
"C",4,4
"D",6,5
"E",8,2

Example output:

A,0,0,1,3,3,1.0
B,2,0,4,9,7,1.1666666666666667
,3,0,10,11,8,4.0
C,4,0,12,15,11,2.75
D,6,0,16,20,14,2.8
E,8,0,21,22,14,7.0
9.5,3.119444444444445
