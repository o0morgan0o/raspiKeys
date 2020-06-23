import os
from games.utils.midiIO import MidiIO

# Class used for singleton pattern, for storing global midiIO config
class Autoload:
    class __Autoload:
        def __init__(self):
            # audio instance of midiIO
            self.midiIO = MidiIO()
            self.loadConfig()

        def loadConfig(self):
            # location of config file
            configPath = os.path.join(os.path.dirname(__file__), "../config.ini") # TODO: find better way for the path
            print(configPath)
            configLabels=["DEFAULT_MODE" , "DEFAULT_QUESTION_DELAY" , "DEFAULT_DIFFICULTY" , "DEFAULT_TIMES_EACH_TRANSPOSE",
            "DEFAULT_NB_TRANSPOSES_BETWEEN_CHANGE", "DEFAULT_MIDI_INTERFACE"]
            try:
                config={}
                with open(configPath, 'r') as file:
                    for line in file:
                        for param in configLabels:
                            if line.find(param) != -1:
                                paramVal = line.split("=")[1].replace("\n","")
                                config[param]= paramVal
                print(config)
                        # maybe should test values
                        # loading in a dictionnary
                        # audio config trying to laod
            except:
                print("No config file found")

    instance = None
    def __init__(self):
        if not Autoload.instance:
            Autoload.instance = Autoload.__Autoload()
            print(" created")
        else:
            print(" not created")
            pass
    def getInstance(self):
        print(" returning")
        return self.instance.midiIO
    






