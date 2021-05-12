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
        self.processed_waveDir = env.PROCESSED_WAV_FOLDER
        self.metroTick = env.METRO_TICK_FILE
        self.currentFile = None
        self.currentFileLength = None
        self.convertNewFiles()

        # self.tracksWav = self.loadBacktracksWav()
        self.realMetro=None
        # initialisation des array contenant les tracks
        self.tracksWav = lambda: None
        self.tracksWav.house = []
        self.tracksWav.jazz = []
        self.tracksWav.latin = []
        self.tracksWav.hiphop = []

        self.activeSample = None
        self.activeFolder = None

    def initialize(self):
        self.loadBacktracksWav()
        self.pickRandomSample("house")

        # may be the buffer size will need to be increased if alsa problems in the console. ...

        pygame.mixer.pre_init(44100, -16, 2, 1024)
        pygame.mixer.init()
        pygame.init()
        pygame.mixer.music.set_volume(0.6)

        self.isPlaying = False

    def pickRandomSample(self, category):
        selectedFolder = None
        if category == "house":
            self.activeFolder = "house"
            selectedFolder = self.tracksWav.house
        elif category == "jazz":
            self.activeFolder = "jazz"
            selectedFolder = self.tracksWav.jazz
        elif category == "latin":
            self.activeFolder = "latin"
            selectedFolder = self.tracksWav.latin
        elif category == "hiphop":
            self.activeFolder = "hiphop"
            selectedFolder = self.tracksWav.hiphop
        else:
            # TODO : handle error here
            print("unknown category !")
            return
        if len(selectedFolder) == 0:
            return
        index = random.randint(0, len(selectedFolder) - 1)
        self.activeSample = (selectedFolder[index], index)
        # TODO: trigger this function on boutton pressed by user in the config to reload wav or mp3 files

    def convertNewFiles(self):
        # we try to convert all files put by the user. It is needed because we only want PCM 16 bits
        # TODO This should not work because of refactorization between to multiple folders
        # TODO make test to this to easier implementation
        print(self.user_waveDir)
        for filename in os.listdir(self.user_waveDir):
            filenameFull = os.path.join(self.user_waveDir, filename)
            # print("will tyr to convert " , filenameFull)
            try:
                data, samplerate = soundfile.read(filenameFull)
                outfile = os.path.join(self.processed_waveDir, filename)
                soundfile.write(outfile, data, samplerate, subtype="PCM_16")
                print("done")
            except Exception:
                print("error during conversion", filename)

    def loadTick(self):
        pygame.mixer.music.load(self.metroTick)

    def playTick(self):
        pygame.mixer.music.play()

    def loadBacktracksWav(self):
        path_to_search = os.path.join(self.processed_waveDir, "house")
        if(os.path.exists(path_to_search)):
            for filename in os.listdir(path_to_search):
                self.tracksWav.house.append(
                    os.path.join(path_to_search, filename))

        path_to_search = os.path.join(self.processed_waveDir, "jazz")
        if(os.path.exists(path_to_search)):
            for filename in os.listdir(path_to_search):
                self.tracksWav.jazz.append(
                    os.path.join(path_to_search, filename))

        path_to_search = os.path.join(self.processed_waveDir, "latin")
        if(os.path.exists(path_to_search)):
            for filename in os.listdir(path_to_search):
                self.tracksWav.latin.append(
                    os.path.join(path_to_search, filename))

        path_to_search = os.path.join(self.processed_waveDir, "hiphop")
        if(os.path.exists(path_to_search)):
            for filename in os.listdir(path_to_search):
                self.tracksWav.hiphop.append(
                    os.path.join(path_to_search, filename))

    def simplePlay(self):
        self.stopPlay()
        try:
            file = self.activeSample[0]
            pygame.mixer.music.load(file)
            sound = pygame.mixer.Sound(file)
            # pygame.mixer.music.set_pos(0)
            # we keep trace of the current file if we want to retreive it for the lick recording
            self.currentFile = file
            self.currentFileLength = sound.get_length()
            print("Current audio file is ... :",
                  sound.get_length(), " ms, ", self.currentFile)
            # _thread.start_new_thread(self.testLatency, (time.time(),))
            pygame.mixer.music.play(loops=-1, fade_ms=200)
            print("after play")
        except Exception as e:
            print(e)
            print("can't play file !!")
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

    def playRealMetro(self,bpm_asked):
        # the metro is handle a little differently than files it is considered as a sound (and not a music)
        # the sample is created and loop indefinitely.
        self.stopPlay()
        self.unloadAudio()
        bpm=bpm_asked # just for example
        # we must first calculate the length of 1 bar / 4 (1 tick + 1 space)
        tick_duration = 60.0/bpm # this value is in seconds
        # we must calculate the total length of the buffer according to audio
        # 1 sec = 44100 samples  * 2 channels => 88200 samples
        # we then determine the number of samples needed
        samples_needed = tick_duration * 44100 * 2 * 2

        bpmTick = pygame.mixer.Sound(file=self.metroTick)
        raw_array = bpmTick.get_raw()
        tick_sample_length = len(raw_array)
        if tick_sample_length < samples_needed:
            how_many_samples_missing = int(samples_needed-tick_sample_length)
            print('missing samples ', how_many_samples_missing)
            empty_bytes = bytes(how_many_samples_missing)
            raw_array += empty_bytes
        
        # here we can construct 1 bar
        raw_array += raw_array # (2ticks)
        raw_array+=raw_array # (4 ticks)
        # and a second bar
        raw_array+=raw_array # (8 ticks)
        # double again
        raw_array+=raw_array # (8 ticks)
        # and again
        raw_array+=raw_array # (8 ticks)
        self.realMetro = pygame.mixer.Sound(buffer=raw_array)
        self.realMetro.set_volume(0.1)
        self.realMetro.play(-1)

    def stopPlay(self):
        pygame.mixer.music.stop()
        try:
            self.realMetro.stop()
        except Exception as e:
            print('')

    def convertToWav(self, filename):
        sound = AudioSegment.from_file(filename, format="wav")
        sound.set_frame_rate
        baseName = os.path.basename(filename)
        exportName = os.path.splitext(baseName)[0]
        exportName = "out.wav"
        print("outname ", exportName)
        sound.export(os.path.join(self.waveDir, exportName),
                     format="wav", bitrate="16k")

        return exportName

    def unloadAudio(self):
        print("try unload ....")
        pygame.mixer.music.unload()

    def getVolume():
        actualVol= pygame.mixer.music.get_volume()
        print('Getting actual volume ...' , actualVol)
        return actualVol

    def setVolume(self, value):
        print("Updating sound volume ...", value)
        pygame.mixer.music.set_volume(value)
        try:
            self.realMetro.set_volume(value)
        except Exception as e:
            print('cannot change volume of metronome')
    
    # def setMetroVolume(value):
        # self.realMetro.set_volume(value)

    def getCurrentTrack(self):
        return (self.currentFile, self.currentFileLength)

    def getTimePlayed(self):
        return pygame.mixer.music.get_pos() / 1000

    def prepareBacktrackForRecord(self, backtrackFile):
        # print(backtrackFile)
        pygame.mixer.music.stop()
        pygame.mixer.music.load(backtrackFile)

    def playBacktrackForRecord(self, nbOfLoops):
        pygame.mixer.music.play(loops=nbOfLoops)

        # start a thread

    def stopBacktrackForRecord(self):
        pass

    def checkIsPlayingMusic(self):
        return pygame.mixer.music.get_busy()
