
import os

ROOT_DIR=os.path.dirname(os.getcwd())
print("ROOT :::", ROOT_DIR)
PROGRAM_FOLDER= os.path.join(ROOT_DIR,  "game")
USER_WAV_FOLDER=os.path.join(ROOT_DIR, "res", "backtracks", "user_wav")
USER_MP3_FOLDER=os.path.join(ROOT_DIR, "res", "backtracks", "user_mp3")
PROCESSED_WAV_FOLDER=os.path.join(ROOT_DIR, "res","backtracks", "processed_wav")
METRO_TICK_FILE=os.path.join(ROOT_DIR, "res", "metro", "tick.wav")
MIDI_FOLDER=os.path.join(ROOT_DIR, "res", "midi")
CONFIG_FILE=os.path.join(ROOT_DIR, "config.json")

COL_BG="black"
COL_MAIN="red"
COL_SEC="green"
COL_TOOLBG="bisque2"
COL_GREY="grey"