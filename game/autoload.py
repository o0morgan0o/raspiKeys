import os
from utils.midiIO import MidiIO
from utils.audio import Sound
from utils.utilFunctions import loadConfig
import sys
import mido

# Class used for singleton pattern, for storing global midiIO config
class Autoload:
    class __Autoload:
        def __init__(self):
            # audio instance of midiIO
            self.config=loadConfig()
            self.configIn = self.config["MIDI_interface_in"]
            self.configOut = self.config["MIDI_interface_out"]
            print("default interface :" , self.configIn, self.configOut)

            
            self.midiIO = MidiIO(self.configIn, self.configOut)
            self.audioPCM = Sound()
            self.audioPCM.convertNewFiles()

            self.sound = Sound()
            self.tracksWav=self.sound.loadBacktracksWav()
            self.activeSamples = self.sound.pickRandomSamples(self.tracksWav);

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

    def getInstanceAudio(self):
        return self.instance.sound
    
    def getTracksWav(self):
        return self.instance.tracksWav
    
    def getActiveSamples(self):
        return self.instance.activeSamples






