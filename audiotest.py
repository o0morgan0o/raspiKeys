import simpleaudio as sa
import soundfile
from pydub import AudioSegment
import os
import pygame

class Sound:

    def __init__(self):
        self.waveDir = "/home/pi/raspiKeys/gui/games/res/backtracks/user_wav/"
        self.backTracksDirWav="/home/pi/raspiKeys/gui/games/res/backtracks/processed_wav"

        



    def loadBacktracksWav(self):
        print("trying to load backtracks")
        tracks = []
        for filename in os.listdir(self.waveDir):
            print(filename)
            tracks.append(os.path.join(self.waveDir, filename))
        return tracks

    def simplePlay(self, filename):
        file = filename
        pygame.init()
#        pygame.mixer.pre_init(44100, 16, 2, 4096)
        pygame.mixer.init()
        pygame.mixer.music.load(file)
        pygame.mixer.music.play(loops=-1, fade_ms=200)

    def stopPlay(self):
        pygame.mixer.music.stop()

    def convertToWav(self, filename):
        sound = AudioSegment.from_file(filename, format="wav")
        sound.set_frame_rate
        baseName =os.path.basename(filename)
        exportName = os.path.splitext(baseName)[0]
        exportName="out.wav"
        print("outname " , exportName)
        sound.export(os.path.join(self.waveDir, exportName), format="wav", bitrate="16k" )
        return exportName
        
    def unloadAudio(self):
        print( "try unload ....")
        pygame.mixer.music.unload()



s = Sound()
tracks = s.loadBacktracksWav()

track= tracks[0]
data, samplerate = soundfile.read(track)
print(samplerate)
soundfile.write('new.wav', data, samplerate, subtype="PCM_16")


#ss = s.convertToWav(track)

#print(ss)
s.simplePlay("new.wav")

while True:
    pass
        


