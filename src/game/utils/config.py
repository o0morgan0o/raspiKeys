import logging

from src.game import env
import json
from enum import Enum
import mido


class ConfigurationFields(Enum):
    DEFAULT_MODE = "default_mode"
    EAR_TRAINING_NOTE_QUESTION_DELAY = "question_delay"
    EAR_TRAINING_NOTE_MAX_INTERVAL = "max_interval_question_note"
    DIFFICULTY = "difficulty"
    TIMES_EACH_TRANSPOSE = "times_each_transpose"
    NB_OF_TRANSPOSE_BEFORE_CHANGE = "nb_of_transpose_before_change"
    MIDI_INTERFACE_IN = "MIDI_interface_in"
    MIDI_INTERFACE_OUT = "MIDI_interface_out"
    MIDI_HOTKEY = "midi_hotkey"
    AUDIO_VOLUME = "audio_volume"
    MIDI_VOLUME = "midi_volume"
    METRO_BPM = "metroBpm"


def updateMetroBpm(new_value: float):
    config = loadConfig()
    config[ConfigurationFields.METRO_BPM.value] = new_value
    writeConfig(config)


def updateAudioVolume(new_value: float):
    config = loadConfig()
    config[ConfigurationFields.AUDIO_VOLUME.value] = new_value
    writeConfig(config)


def updateMidiVolume(new_value: int):
    config = loadConfig()
    config[ConfigurationFields.MIDI_VOLUME.value] = new_value
    writeConfig(config)


def updateMidiInConfig(new_value: str):
    config = loadConfig()
    config[ConfigurationFields.MIDI_INTERFACE_IN.value] = new_value
    writeConfig(config)


def updateMidiOutConfig(new_value: str):
    config = loadConfig()
    config[ConfigurationFields.MIDI_INTERFACE_OUT.value] = new_value
    writeConfig(config)


def updateEarTrainingNoteMaxInterval(new_value: int):
    config = loadConfig()
    config[ConfigurationFields.EAR_TRAINING_NOTE_MAX_INTERVAL.value] = new_value
    writeConfig(config)


def updateEarTrainingNoteDelay(new_value: int):
    config = loadConfig()
    config[ConfigurationFields.EAR_TRAINING_NOTE_QUESTION_DELAY.value] = new_value
    writeConfig(config)


def writeConfig(config):
    json_config = json.dumps(config, indent=4)
    print("saving change in config...")
    outfile = env.CONFIG_FILE
    try:
        with open(outfile, 'w+') as outfile:
            outfile.write(json_config)
            print('Config Saved !')
            return True
    except OSError as e:
        print(e)
        return False


def getMidiInterfaceIn() -> str:
    midi_in_config = loadConfig()[ConfigurationFields.MIDI_INTERFACE_IN.value]
    if midi_in_config == "":
        print("WARNING !! Empty MIDI-IN interface, will try to load first input")
        try:
            midi_in_config = mido.get_input_names()[0]
        except Exception as e:
            print("ERROR !! Could not load any MIDI-in interface")
            logging.exception(e)
            return ""
    return midi_in_config


def getMidiInterfaceOut() -> str:
    midi_out_config = loadConfig()[ConfigurationFields.MIDI_INTERFACE_OUT.value]
    if midi_out_config == "":
        print("WARNING !! Empty MIDI-OUT interface, will try to load first input")
        try:
            midi_out_config = mido.get_output_names()[0]
        except Exception as e:
            print("ERROR !! Could not load any MIDI-out interface")
            logging.exception(e)
            return ""
    return midi_out_config


def getNoteDelay() -> int:
    return loadConfig()[ConfigurationFields.EAR_TRAINING_NOTE_QUESTION_DELAY.value]


def getMaxIntervalQuestionNote() -> int:
    return loadConfig()[ConfigurationFields.EAR_TRAINING_NOTE_MAX_INTERVAL.value]


def getAudioVolume() -> float:
    return loadConfig()[ConfigurationFields.AUDIO_VOLUME.value]


def getMidiVolume() -> int:
    return loadConfig()[ConfigurationFields.MIDI_VOLUME.value]


def getMetroBpm() -> int:
    return loadConfig()[ConfigurationFields.METRO_BPM.value]


def loadConfigFromFile(config: dict) -> dict:
    if config is None:
        config = {}
    config[ConfigurationFields.DEFAULT_MODE.value] = \
        (0, config.get(ConfigurationFields.DEFAULT_MODE.value))[ConfigurationFields.DEFAULT_MODE.value in config.keys()]
    config[ConfigurationFields.EAR_TRAINING_NOTE_QUESTION_DELAY.value] = \
        (50, config.get(ConfigurationFields.EAR_TRAINING_NOTE_QUESTION_DELAY.value))[ConfigurationFields.EAR_TRAINING_NOTE_QUESTION_DELAY.value in config.keys()]
    config[ConfigurationFields.TIMES_EACH_TRANSPOSE.value] = \
        (4, config.get(ConfigurationFields.TIMES_EACH_TRANSPOSE.value))[ConfigurationFields.TIMES_EACH_TRANSPOSE.value in config.keys()]
    config[ConfigurationFields.NB_OF_TRANSPOSE_BEFORE_CHANGE.value] = \
        (4, config.get(ConfigurationFields.NB_OF_TRANSPOSE_BEFORE_CHANGE.value))[ConfigurationFields.NB_OF_TRANSPOSE_BEFORE_CHANGE.value in config.keys()]
    config[ConfigurationFields.MIDI_INTERFACE_IN.value] = \
        ("", config.get(ConfigurationFields.MIDI_INTERFACE_IN.value))[ConfigurationFields.MIDI_INTERFACE_IN.value in config.keys()]
    config[ConfigurationFields.MIDI_INTERFACE_OUT.value] = \
        ("", config.get(ConfigurationFields.MIDI_INTERFACE_OUT.value))[ConfigurationFields.MIDI_INTERFACE_OUT.value in config.keys()]
    config[ConfigurationFields.MIDI_HOTKEY.value] = \
        (50, config.get(ConfigurationFields.MIDI_HOTKEY.value))[ConfigurationFields.MIDI_HOTKEY.value in config.keys()]
    config[ConfigurationFields.AUDIO_VOLUME.value] = \
        (80, config.get(ConfigurationFields.AUDIO_VOLUME.value))[ConfigurationFields.AUDIO_VOLUME.value in config.keys()]
    config[ConfigurationFields.MIDI_VOLUME.value] = \
        (80, config.get(ConfigurationFields.MIDI_VOLUME.value))[ConfigurationFields.MIDI_VOLUME.value in config.keys()]
    config[ConfigurationFields.METRO_BPM.value] = \
        (91, config.get(ConfigurationFields.METRO_BPM.value))[ConfigurationFields.METRO_BPM.value in config.keys()]
    config[ConfigurationFields.EAR_TRAINING_NOTE_MAX_INTERVAL.value] = \
        (6, config.get(ConfigurationFields.EAR_TRAINING_NOTE_MAX_INTERVAL.value))[ConfigurationFields.EAR_TRAINING_NOTE_MAX_INTERVAL.value in config.keys()]
    return config


def loadConfig():
    try:
        with open(env.CONFIG_FILE, 'r') as f:
            configFile = json.load(f)
            return loadConfigFromFile(configFile)
    except OSError as e:
        print("No config file found", e)
        return None
    except KeyError as e:
        logging.exception(e)
        # it means a parameter is not correct, so we rewrite default config
        # writeConfig(src.game())
        return None
