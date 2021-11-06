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
IMAGE_BLACK_EAR_TRAINING_NOTE = os.path.join(ROOT_DIR, "res", "icons", "earTrainingNoteBlack.png")
IMAGE_BLACK_EAR_TRAINING_CHORD = os.path.join(ROOT_DIR, "res", "icons", "earTrainingChordBlack.png")
IMAGE_BLACK_BACKTRACKS = os.path.join(ROOT_DIR, "res", "icons", "drumsBlack.png")
IMAGE_BLACK_PRACTISE_LICKS = os.path.join(ROOT_DIR, "res", "icons", "licksBlack.png")
IMAGE_WHITE_EAR_TRAINING_NOTE = os.path.join(ROOT_DIR, "res", "icons", "earTrainingNoteWhite.png")
IMAGE_WHITE_EAR_TRAINING_CHORD = os.path.join(ROOT_DIR, "res", "icons", "earTrainingChordWhite.png")
IMAGE_WHITE_BACKTRACKS = os.path.join(ROOT_DIR, "res", "icons", "drumsWhite.png")
IMAGE_WHITE_PRACTISE_LICKS = os.path.join(ROOT_DIR, "res", "icons", "licksWhite.png")
PLAY_IMAGE = os.path.join(ROOT_DIR, "res", "icons", "playWhite.png")
PAUSE_IMAGE = os.path.join(ROOT_DIR, "res", "icons", "pauseWhite.png")
SHUFFLE_IMAGE = os.path.join(ROOT_DIR, "res", "icons", "shuffleWhite.png")
RECORD_IMAGE = os.path.join(ROOT_DIR, "res", "icons", "rec.png")
METRONOME_IMAGE= os.path.join(ROOT_DIR, "res", "icons", "metronome.png")

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
