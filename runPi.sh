### BEGIN INIT INFO
# Provides: raspikeys
# Required-Start: $all
# Required-Stop:
# Default-Start: 2 3 4 5
# Default-Stop:
# Short-Description: launch raspikeys service in systemd
### END INIT INFO

# aconnect -x
# ulimit -s 2000
#export DISPLAY=:0
# xdotool mousemove 1000 1000
/home/pi/raspiKeys/killPi.sh
# /home/pi/raspiKeys/main.py --runDevice=pi
/home/pi/raspiKeys/src/main.py &
#xinit


