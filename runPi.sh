#!/bin/bash

export DISPLAY=:0
xdotool mousemove 1000 1000
/home/pi/rapiKeys/killPi.sh
/home/pi/raspiKeys/game/main.py --runDevice=pi


