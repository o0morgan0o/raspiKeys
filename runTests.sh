#!/bin/bash
#export DISPLAY=localhost:10.0
aconnect -x
# ulimit -s 2000
export DISPLAY='192.168.0.12:0.0'
python3 -m unittest


# tests DONE
# =============
# - main.py
# - env.py
# - autoload.py 
# - audio.py
# - bpm.py
# - midiChords.py 
# - canvasThread.py 
# - graph.py 
# - midiIo.py
# - midiToNoteNames.py 
# - waitingNote.py 

# test TODO
# =============
# - modeOptions.py
# - mode0gui.py
# - mode1gui.py
# - mode2gui.py
# - mode3gui.py
# - gameplay0.py
# - gameplay1.py 
# - gameplay2.py 
# -gameplay3.py
