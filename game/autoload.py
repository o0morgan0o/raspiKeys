import os
from game.utils.midiIO import MidiIO
from game.utils.audio import Sound
from game.utils.utilFunctions import loadConfig
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
            self.activeSample = self.sound.pickRandomSample(self.tracksWav);

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
    
    def getTracksWav(self):
        return self.instance.tracksWav
    
    def getActiveSample(self):
        return self.instance.activeSample[0]

    def getActiveSampleIndex(self):
        return self.instance.activeSample[1]
    






