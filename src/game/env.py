import os

# ROOT_DIR = os.path.join("/", "home", "pi")
# ROOT_DIR = os.path.join(ROOT_DIR, "raspiKeys")
if os.name == 'nt':
    ROOT_DIR = os.getcwd()
else:
    ROOT_DIR = "/home/pi/raspiKeys/src"
TEST_ROOT_DIR_PROCESSED_WAV_FOLDER = os.path.join(ROOT_DIR, "res_test", "processed_wav")
TEST_ROOT_DIR_PROCESSED_EMPTY_FOLDER = os.path.join(ROOT_DIR, "res_test", "processed_wav_empty")
print("ROOT :::", ROOT_DIR)

PROGRAM_FOLDER = os.path.join(ROOT_DIR, "game")
USER_WAV_BASE_FOLDER = os.path.join(ROOT_DIR, "res", "backtracks", "user_wav")
USER_MP3_FOLDER = os.path.join(ROOT_DIR, "res", "backtracks", "user_mp3")
PROCESSED_WAV_BASE_FOLDER = os.path.join(ROOT_DIR, "res", "backtracks", "processed_wav")
METRO_TICK_FILE = os.path.join(ROOT_DIR, "res", "metro", "tick.wav")
MIDI_FOLDER = os.path.join(ROOT_DIR, "res", "midi")
CONFIG_FILE = os.path.join(ROOT_DIR, "config.json")

VOLUME_IMAGE = os.path.join(ROOT_DIR, "res", "icons", "volume.png")
SETTINGS_IMAGE = os.path.join(ROOT_DIR, "res", "icons", "settingsBlack.png")
MODE0_IMAGE_BLACK = os.path.join(ROOT_DIR, "res", "icons", "earTrainingNoteBlack.png")
MODE1_IMAGE_BLACK = os.path.join(ROOT_DIR, "res", "icons", "earTrainingChordBlack.png")
MODE2_IMAGE_BLACK = os.path.join(ROOT_DIR, "res", "icons", "drumsBlack.png")
MODE3_IMAGE_BLACK = os.path.join(ROOT_DIR, "res", "icons", "licksBlack.png")
MODE0_IMAGE_WHITE = os.path.join(ROOT_DIR, "res", "icons", "earTrainingNoteWhite.png")
MODE1_IMAGE_WHITE = os.path.join(ROOT_DIR, "res", "icons", "earTrainingChordWhite.png")
MODE2_IMAGE_WHITE = os.path.join(ROOT_DIR, "res", "icons", "drumsWhite.png")
MODE3_IMAGE_WHITE = os.path.join(ROOT_DIR, "res", "icons", "licksWhite.png")
PLAY_IMAGE = os.path.join(ROOT_DIR, "res", "icons", "playWhite.png")
PAUSE_IMAGE = os.path.join(ROOT_DIR, "res", "icons", "pauseWhite.png")
SHUFFLE_IMAGE = os.path.join(ROOT_DIR, "res", "icons", "shuffleWhite.png")
RECORD_IMAGE = os.path.join(ROOT_DIR, "res", "icons", "rec.png")

NAVBAR_WIDTH = 80
FOOTER_HEIGHT = 80
FULL_SCREEN_W = 800
FULL_SCREEN_H = 480
LEFT_SCREEN_W = 320
RIGHT_SCREEN_W = 480
LEFT_SCREEN_H = 330
RIGHT_SCREEN_H = 480

GAME_SCREEN_W = FULL_SCREEN_W - NAVBAR_WIDTH
GAME_SCREEN_H = FULL_SCREEN_H - FOOTER_HEIGHT
