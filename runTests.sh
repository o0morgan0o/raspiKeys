#!/bin/bash
#export DISPLAY=localhost:10.0
aconnect -x
ulimit -s 2000
export DISPLAY='192.168.0.14:0.0'
python3 -m unittest