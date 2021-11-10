import json
import logging
import uuid
from enum import Enum
from datetime import date
import os
from src.game import env


class JsonLickFields(Enum):
    FIELD_OS_NAME = "os_name"
    FIELD_LICK_ID = "lick_id"
    FIELD_LICK_DATE = "lick_date"
    FIELD_LICK_NAME = "lick_name"
    FIELD_LICK_KEY = "lick_key"
    FIELD_BACKTRACK_FILE = "backtrack_file"
    FIELD_NUMBER_OF_LOOPS = "number_of_loops"
    FIELD_CHORD_NOTES = "chord_notes"
    FIELD_MELODY_NOTES = "melody_notes"


def writeJsonLick(json_data, filename: str):
    try:
        outfile = os.path.join(env.MIDI_FOLDER, filename + ".json")
        print("Saving : ", outfile, "data :", json_data)
        with open(outfile, "w+") as outfile:
            outfile.write(json_data)
        return True
    except Exception as e:
        logging.exception(e)
        return False


def deleteJsonLickFile(filename: str):
    try:
        print("Deleting : {}".format(filename))
        filename_full = os.path.join(env.MIDI_FOLDER, filename)
        os.remove(filename_full)
    except Exception as e:
        logging.exception(e)


def getJsonDataFromFile(filename: str):
    file_path = os.path.join(env.MIDI_FOLDER, filename)
    json_file = open(file_path, 'r')
    data = json.load(json_file)
    return data


def getAllMidiLicksFilesForPlatform():
    all_files = []
    for filename in os.listdir(os.path.join(env.MIDI_FOLDER)):
        if os.path.splitext(filename)[1] == ".json":
            # check if the lick file is in the correct platform
            # it is mainly for development purpose
            with open(os.path.join(env.MIDI_FOLDER, filename), 'r') as lick_file:
                midi_file = json.loads(lick_file.read())
                lick_platform = midi_file[JsonLickFields.FIELD_OS_NAME.value]
                if lick_platform == os.name:
                    all_files.append(filename)

    all_files.sort()
    print("Loading MIDI Files. Found {} file(s)".format(len(all_files)))
    return all_files


def createJsonMidiLickFromNotes(
        os_name,
        lick_name,
        lick_key: int,
        backtrack_file: str,
        number_of_loops: int,
        chord_notes: list,

        melody_notes: list = None) -> tuple:
    """ This functions return a tuple containing an uuid which can be used for the name of a file, and the complete json object"""
    lick_id = str(uuid.uuid1())
    today = date.today()
    current_date = today.strftime("%d/%m/%Y %H:%M")
    obj = {
        JsonLickFields.FIELD_OS_NAME.value : os.name,
        JsonLickFields.FIELD_LICK_ID.value: lick_id,
        JsonLickFields.FIELD_LICK_DATE.value: current_date,
        JsonLickFields.FIELD_LICK_NAME.value: lick_name,
        JsonLickFields.FIELD_LICK_KEY.value: lick_key,
        JsonLickFields.FIELD_BACKTRACK_FILE.value: backtrack_file,
        JsonLickFields.FIELD_NUMBER_OF_LOOPS.value: number_of_loops,
        JsonLickFields.FIELD_CHORD_NOTES.value: chord_notes,
        JsonLickFields.FIELD_MELODY_NOTES.value: melody_notes,
    }
    json_object = json.dumps(obj, indent=4)
    return lick_id, json_object
