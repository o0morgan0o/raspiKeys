xinit &

export DISPLAY=:0
aconnect -x
ulimit -s 2000
export PYTHONPATH=/home/pi/raspiKeys/
xset s off
xset -dpms
xset  s noblank
python3 /home/pi/raspiKeys/src/main.py


