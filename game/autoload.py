from game.utils.midiIO import MidiIO
from game.utils.audio import Audio
from game.utils.utilFunctions import loadConfig


class Autoload:  # Class used for singleton pattern, for storing global midiIO config
    class __Autoload:
        def __init__(self):
            # audio instance of midiIO
            self.config = loadConfig()
            self.configIn = self.config["MIDI_interface_in"]
            self.configOut = self.config["MIDI_interface_out"]
            print("default interface :", self.configIn, self.configOut)
            self.midiIO = MidiIO(self.configIn, self.configOut)
            self.audioPCM = Audio()
            self.audioPCM.convertNewFiles()
            self.sound = Audio()
    instance = None

    def __init__(self):
        if not Autoload.instance:
            Autoload.instance = Autoload.__Autoload()
            print("Creation of instance")
        else:
            print("Recuperation of instance")
            pass

    def getInstance(self):
        return self.instance.midiIO

    def getInstanceAudio(self):
        return self.instance.sound
