from game import env
import json


def formatOutputInterval(mInterval):
    # TODO: Extend to other responses
    # interval = abs(mInterval)
    interval = mInterval
    if interval == 0:
        return "unisson"
    elif interval == 1:
        return "+min 2nd"
    elif interval == 2:
        return "+maj 2nd"
    elif interval == 3:
        return "+min 3rd"
    elif interval == 4:
        return "+maj 3rd"
    elif interval == 5:
        return "+perf 4th"
    elif interval == 6:
        return "+dim 5th"
    elif interval == 7:
        return "+perf 5th"
    elif interval == 8:
        return "+min 6th"
    elif interval == 9:
        return "+maj 6th"
    elif interval == 10:
        return "+min 7th"
    elif interval == 11:
        return "+maj 7th"
    elif interval == 12:
        return "+octave"
    elif interval == 13:
        return "+min 9th"
    elif interval == 14:
        return "+maj 9th"
    elif interval == 15:
        return "+min 10th"
    elif interval == 16:
        return "+maj 10th"
    elif interval == 17:
        return "+perf 11th"
    elif interval == 18:
        return "+aug 11th"
    elif interval == 19:
        return "+perfect 12th"
    elif interval == -1:
        return "-min 2nd"
    elif interval == -2:
        return "-maj 2nd"
    elif interval == -3:
        return "-min 3rd"
    elif interval == -4:
        return "-maj 3rd"
    elif interval == -5:
        return "-perf 4th"
    elif interval == -6:
        return "-dim 5th"
    elif interval == -7:
        return "-perf 5th"
    elif interval == -8:
        return "-min 6th"
    elif interval == -9:
        return "-maj 6th"
    elif interval == -10:
        return "-min 7th"
    elif interval == -11:
        return "-maj 7th"
    elif interval == -12:
        return "-octave"
    elif interval == -13:
        return "-min 9th"
    elif interval == -14:
        return "-maj 9th"
    elif interval == -15:
        return "-min 10th"
    elif interval == -16:
        return "-maj 10th"
    elif interval == -17:
        return "-perf 11th"
    elif interval == -18:
        return "-aug 11th"
    else:
        print("ERROR: interval unknow", interval)
        return ""


def getChordInterval(type):
    if type == "minor":
        return [0, 3, 7]
    elif type == "major":
        return [0, 4, 7]
    elif type == "min7":
        return [0, 3, 7, 10]
    elif type == "maj7":
        return [0, 4, 7, 11]
    elif type == "min7b5":
        return [0, 3, 6, 10]
    elif type == "dom7":
        return [0, 4, 10]



def saveMode0IntervalOffset(value):
    newConfig = loadConfig()
    newConfig["mode0IntervalOffset"] = int(value)
    saveConfig(newConfig)

def saveMode0MidiVolume(value):
    newConfig = loadConfig()
    newConfig["mode0MidiVolume"] = int(value)
    saveConfig(newConfig)


