import simpleaudio as sa
import soundfile
from pydub import AudioSegment
import os
import pygame
import env
import random

class Sound:

    def __init__(self):
        self.user_waveDir = env.USER_WAV_FOLDER
        self.user_mp3Dir = env.USER_MP3_FOLDER
        self.processed_waveDir =env.PROCESSED_WAV_FOLDER
        pygame.init()
#        pygame.mixer.pre_init(44100, 16, 2, 4096)
        pygame.mixer.init()


    def pickRandomSamples(self, tracks):
        return  random.sample(tracks, 4)

        
        # TODO: trigger this function on boutton pressed by user in the config to reload wav or mp3 files
    def convertNewFiles(self):
        # we try to convert all files put by the user. It is needed because we only want PCM 16 bits
        print(self.user_waveDir)
        for filename in os.listdir(self.user_waveDir):
            filenameFull = os.path.join(self.user_waveDir, filename)
            # print("will tyr to convert " , filenameFull)
            try:
                data , samplerate = soundfile.read(filenameFull)
                outfile = os.path.join(self.processed_waveDir, filename)
                soundfile.write(outfile, data, samplerate, subtype="PCM_16")
                print("done")
            except:
                print("error during conversion" , filename)



    def loadBacktracksWav(self):
        print("trying to load backtracks")
        tracks = []
        for filename in os.listdir(self.processed_waveDir):
            # print(filename)
            tracks.append(os.path.join(self.processed_waveDir, filename))
            
        # print(tracks)
        return tracks

    def simplePlay(self, filename):
        file = filename
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

    def setVolume( value):
        print("update sound voulme", value)
        pygame.mixer.music.set_volume(int(value)/100)


# s = Sound()
# tracks = s.loadBacktracksWav()

# track= tracks[0]
# data, samplerate = soundfile.read(track)
# print(samplerate)
# soundfile.write('new.wav', data, samplerate, subtype="PCM_16")


# #ss = s.convertToWav(track)

# #print(ss)
# s.simplePlay("new.wav")

# while True:
#     pass
        


