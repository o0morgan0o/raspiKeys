#!/bin/bash

#export DISPLAY=localhost:10.0
aconnect -x
ulimit -s 2000
export DISPLAY='192.168.0.12:0.0'
#python3 -m pdb /home/pi/raspiKeys/main.py
python3 /home/pi/raspiKeys/main.py


