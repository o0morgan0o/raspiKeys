import os
from utils.midiIO import MidiIO
from utils.audio import Sound

# Class used for singleton pattern, for storing global midiIO config
class Autoload:
    class __Autoload:
        def __init__(self):
            # audio instance of midiIO
            self.midiIO = MidiIO()
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







