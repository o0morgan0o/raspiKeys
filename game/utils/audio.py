import time
import simpleaudio as sa
import _thread
import soundfile
from pydub import AudioSegment
import os
import pygame
from game import env
import random

class Audio:

    def __init__(self):
        self.user_waveDir = env.USER_WAV_FOLDER
        self.user_mp3Dir = env.USER_MP3_FOLDER
        self.processed_waveDir =env.PROCESSED_WAV_FOLDER
        self.metroTick = env.METRO_TICK_FILE
        self.currentFile=None
        self.currentFileLength =None

        pygame.mixer.pre_init(44100, 8, 2, 1024) # may be the buffer size will need to be increased if alsa problems in the console. ...
        pygame.mixer.init()
        pygame.init()
        pygame.mixer.music.set_volume(.1)
        self.isPlaying=False


    def pickRandomSample(self, tracks):
        if len(tracks) == 0 :
            return 
        index = random.randint(0,len(tracks) -1)
        return (tracks[index], index)
        # return  random.sample(tracks, 4)

        
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


    def loadTick(self):
        pygame.mixer.music.load(self.metroTick)
    
    def playTick(self):
        pygame.mixer.music.play()


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
        sound = pygame.mixer.Sound(file)
        # pygame.mixer.music.set_pos(0)
        self.currentFile = file # we keep trace of the current file if we want to retreive it for the lick recording
        self.currentFileLength = sound.get_length()
        print("Current audio file is ... :", sound.get_length(), " ms, ", self.currentFile)
        # _thread.start_new_thread(self.testLatency, (time.time(),))
        pygame.mixer.music.play(loops=-1)
        print("after play")
        # pygame.mixer.music.play(loops=-1, fade_ms=200)


# doesn't work
    # def testLatency(self, initialTime):
    #     print("starting thread latency")
    #     initialTime = initialTime
    #     isActive=True
    #     while isActive==True:
    #         pos = pygame.mixer.music.get_pos()
    #         print("waiting", pos)
    #         if pos > .1:
    #             newTime = time.time()
    #             deltaTime = newTime - initialTime
    #             print(f"Soud is PLAYING !!, latency is {deltaTime*1000}")
    #             isActive=False
                


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

    def setVolume(self,value):
        print("Update sound voulme", value)
        pygame.mixer.music.set_volume(int(value)/100)

    def getCurrentTrack(self):
        return (self.currentFile, self.currentFileLength)
    
    def getTimePlayed(self):
        return pygame.mixer.music.get_pos()/1000

    def prepareBacktrackForRecord(self, backtrackFile):
        # print(backtrackFile)
        pygame.mixer.music.load(backtrackFile)

    def playBacktrackForRecord(self, nbOfLoops):
        pygame.mixer.music.play(loops=nbOfLoops)

        # start a thread


    def stopBacktrackForRecord(self):
        pass

    def checkIsPlayingMusic(self):
        return pygame.mixer.music.get_busy()

