import env
import json

def formatOutputInterval(mInterval):
    #TODO: Extend to other responses
    # interval = abs(mInterval)
    interval=mInterval
    if interval ==0 : return "unisson"
    elif interval == 1: return "+min 2nd"
    elif interval == 2: return "+maj 2nd"
    elif interval == 3 : return "+min 3rd"
    elif interval == 4: return "+maj 3rd"
    elif interval == 5: return "+perf 4th"
    elif interval == 6 : return "+dim 5th"
    elif interval == 7 : return "+perf 5th"
    elif interval ==8 : return "+min 6th"
    elif interval ==9: return "+maj 6th"
    elif interval ==10: return "+min 7th"
    elif interval == 11 : return "+maj 7th"
    elif interval == 12: return "+octave"
    elif interval == 13: return "+min 9th"
    elif interval == 14: return "+maj 9th"
    elif interval == 15: return "+min 10th"
    elif interval == 16: return "+maj 10th"
    elif interval == 17: return "+perf 11th"
    elif interval == 18: return "+aug 11th"
    elif interval == 19: return "+perfect 12th"
    elif interval == -1: return "-min 2nd"
    elif interval == -2: return "-maj 2nd"
    elif interval == -3 : return "-min 3rd"
    elif interval == -4: return "-maj 3rd"
    elif interval == -5: return "-perf 4th"
    elif interval == -6 : return "-dim 5th"
    elif interval == -7 : return "-perf 5th"
    elif interval ==-8 : return "-min 6th"
    elif interval ==-9: return "-maj 6th"
    elif interval ==-10: return "-min 7th"
    elif interval == -11 : return "-maj 7th"
    elif interval == -12: return "-octave"
    elif interval == -13: return "-min 9th"
    elif interval == -14: return "-maj 9th"
    elif interval == -15: return "-min 10th"
    elif interval == -16: return "-maj 10th"
    elif interval == -17: return "-perf 11th"
    elif interval == -18: return "-aug 11th"
    else: 
        print("ERROR: interval unknow", interval)
        return ""

def getChordInterval(type):
    if type == "minor":
        return [0,3,7]
    elif type == "major":
        return [0,4,7]
    elif type=="min7":
        return [0,3,7,10]
    elif type =="maj7":
        return [0,4,7,11]
    elif type=="min7b5":
        return [0,3,6,10]
    elif type=="dom7":
        return [0,4,10]

def loadConfig():
    print("trying to load config") # location of config file
    # DEFAULT CONFIGURATION IF LOADING OF FILE FAILED
    default_config = {}
    default_config["default_mode"] = 0
    default_config["question_delay"] = 50
    default_config["difficulty"]=50
    default_config["times_each_transpose"]=4
    default_config["nb_of_transpose_before_change"]=4
    default_config["MIDI_interface_in"]=""
    default_config["MIDI_interface_out"]=""
    default_config["midi_hotkey"]=50
    default_config["volume"]= 80


    configFilePath = env.CONFIG_FILE
    config={}
    try:
        with open(configFilePath, 'r') as f:
            configFile = json.load(f)
            default_config["default_mode"]=configFile["default_mode"]
            default_config["question_delay"]=configFile["question_delay"]
            default_config["difficulty"]=configFile["difficulty"]
            default_config["times_each_transpose"]=configFile["times_each_transpose"]
            default_config["nb_of_transpose_before_change"]=configFile["nb_of_transpose_before_change"]
            default_config["MIDI_interface_in"]=configFile["MIDI_interface_in"]
            default_config["MIDI_interface_in"]=configFile["MIDI_interface_in"]
            default_config["MIDI_interface_in"]=configFile["MIDI_interface_in"]
    except:
        print("No config file found")
    # print("loaded config is " , config)
    return configFile


