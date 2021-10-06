import os

#ROOT_DIR = os.path.join("/", "home", "pi")
#ROOT_DIR = os.path.join(ROOT_DIR, "raspiKeys")
ROOT_DIR = os.getcwd()
TEST_ROOT_DIR_PROCESSED_WAV_FOLDER = os.path.join(ROOT_DIR, "res_test", "processed_wav")
TEST_ROOT_DIR_PROCESSED_EMPTY_FOLDER = os.path.join( ROOT_DIR, "res_test", "processed_wav_empty")
print("ROOT :::", ROOT_DIR)

PROGRAM_FOLDER = os.path.join(ROOT_DIR, "game")
USER_WAV_FOLDER = os.path.join(ROOT_DIR, "res", "backtracks", "user_wav")
USER_MP3_FOLDER = os.path.join(ROOT_DIR, "res", "backtracks", "user_mp3")
PROCESSED_WAV_FOLDER = os.path.join( ROOT_DIR, "res", "backtracks", "processed_wav")
METRO_TICK_FILE = os.path.join(ROOT_DIR, "res", "metro", "tick.wav")
MIDI_FOLDER = os.path.join(ROOT_DIR, "res", "midi")
CONFIG_FILE = os.path.join(ROOT_DIR, "config.json")
CONFIG_METRO_BPM = os.path.join(ROOT_DIR, "metroBpm")

VOLUME_IMAGE = os.path.join(ROOT_DIR, "res", "icons", "volume.png")
SETTINGS_IMAGE = os.path.join(ROOT_DIR, "res", "icons", "settingsBlack.png")
MODE0_IMAGE_BLACK = os.path.join( ROOT_DIR, "res", "icons", "earTrainingNoteBlack.png")
MODE1_IMAGE_BLACK = os.path.join( ROOT_DIR, "res", "icons", "earTrainingChordBlack.png")
MODE2_IMAGE_BLACK = os.path.join(ROOT_DIR, "res", "icons", "drumsBlack.png")
MODE3_IMAGE_BLACK = os.path.join(ROOT_DIR, "res", "icons", "licksBlack.png")
MODE0_IMAGE_WHITE = os.path.join( ROOT_DIR, "res", "icons", "earTrainingNoteWhite.png")
MODE1_IMAGE_WHITE = os.path.join( ROOT_DIR, "res", "icons", "earTrainingChordWhite.png")
MODE2_IMAGE_WHITE = os.path.join(ROOT_DIR, "res", "icons", "drumsWhite.png")
MODE3_IMAGE_WHITE = os.path.join(ROOT_DIR, "res", "icons", "licksWhite.png")
PLAY_IMAGE = os.path.join(ROOT_DIR, "res", "icons", "playWhite.png")
PAUSE_IMAGE = os.path.join(ROOT_DIR, "res", "icons", "pauseWhite.png")
SHUFFLE_IMAGE = os.path.join(ROOT_DIR, "res", "icons", "shuffleWhite.png")
RECORD_IMAGE = os.path.join(ROOT_DIR, "res", "icons", "rec.png")

COL_BG = "black"
COL_MAIN = "red"
COL_SEC = "green"
COL_TOOLBG = "bisque2"
COL_GREY = "grey"

FULL_SCREEN_W = 800
FULL_SCREEN_H = 480
LEFT_SCREEN_W = 320
RIGHT_SCREEN_W = 480
LEFT_SCREEN_H= 330
RIGHT_SCREEN_H= 480