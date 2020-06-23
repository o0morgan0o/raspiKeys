import simpleaudio as sa
import soundfile
from pydub import AudioSegment
import os
import pygame
class Sound:

    def __init__(self):
        self.waveDir = "/home/pi/raspiKeys/gui/games/res/wav/"
        self.backTracksDirWav="/home/pi/raspiKeys/gui/games/res/backtracks/wav/"
        self.backTracksDirMp3="/home/pi/raspiKeys/gui/games/res/backtracks/mp3/"
        pass

    def loadEffectSounds(self):
        # success sound
        success_sound = "/home/pi/raspiKeys/gui/games/res/wav/success.wav"
        self.success_sound = sa.WaveObject.from_wave_file(success_sound)
        # error sound
        error_sound = "/home/pi/raspiKeys/gui/games/res/wav/error.wav"
        self.error_sound= sa.WaveObject.from_wave_file(error_sound)

        

    # TODO: make a try excerpt because may be the sound could not be loaded
    def play_sound_success(self):
        sound_object = self.success_sound.play()
        sound_object.wait_done()

    def play_sound_error(self):
        sound_object = self.error_sound.play()
        sound_object.wait_done()


    def loadBacktracksWav(self):
        print("trying to load backtracks")
        tracks = []
        for filename in os.listdir(self.backTracksDirWav):
            tracks.append(os.path.join(self.backTracksDirWav, filename))
        return tracks

    def loadBacktracksMp3(self):
        print("trying to load backtracks mp3")
        tracks = []
        for filename in os.listdir(self.backTracksDirMp3):
            tracks.append(os.path.join(self.backTracksDirMp3, filename))
        return tracks

#    def simplePlay(self, filename):
#        wave_obj = sa.WaveObject.from_wave_file(filename)
#        play_obj = wave_obj.play()
#
#        play_obj.wait_done()
#        print("end play")

    def simplePlay(self, filename):
        file = filename
        pygame.init()
#        pygame.mixer.pre_init(44100, 16, 2, 4096)
        pygame.mixer.init(44100, 32, 2, 2116)
        pygame.mixer.music.load(file)
        pygame.mixer.music.play(loops=-1, fade_ms=200)

    def stopPlay(self):
        pygame.mixer.music.stop()

    def convertToWav(self, filename):
        sound = AudioSegment.from_mp3(filename)
        baseName =os.path.basename(filename)
        exportName = os.path.splitext(baseName)[0]
        print("outname " , exportName)
        sound.export(os.path.join(self.backTracksDirWav, exportName), format="wav")
        
    def unloadAudio(self):
        print( "try unload ....")
        pygame.mixer.music.unload()



        


