import logging
import os

import pygame
import soundfile

from src.game import env


class Audio:
    def __init__(self):

        self.isPlaying = False
        self.user_waveDir = env.USER_WAV_BASE_FOLDER
        self.user_mp3Dir = env.USER_MP3_FOLDER
        self.processed_waveDir = env.PROCESSED_WAV_BASE_FOLDER
        self.metroTick = env.METRO_TICK_FILE
        self.currentFile = None
        self.currentFileLength = None
        # self.convertNewFiles()

        self.backtracksFolders = self.findBacktracksFolders(self.processed_waveDir)
        self.allBacktracksInAllFolders = self.findAllBacktracksInAllFolders(self.processed_waveDir, self.backtracksFolders)

        self.audioVolume = None
        self.realMetro = None
        self.activeSample = None
        self.activeFolder = None

    @staticmethod
    def findAllBacktracksInAllFolders(base_backtracks_folder: str, backtrack_folders: list):
        all_results = []
        for m_folder in backtrack_folders:
            backtracks_in_folder = Audio.findAllValidAudioFilesInFolder(base_backtracks_folder, m_folder)
            all_results.append(backtracks_in_folder)
        return all_results

    @staticmethod
    def findBacktracksFolders(path: str) -> list:
        """
        Return a list containing folders in path passed in parameter. It includes empty folders
        :param path:
        :type path:
        :return:
        :rtype:
        """
        return [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]

    @staticmethod
    def findAllValidAudioFilesInFolder(base_audio_folder: str, backtrack_folder: str):
        """
        Return a tuple containing the folder to test (the one which is displayed in the UI, and a list containing the path of all wav files)
        :param base_audio_folder:
        :type base_audio_folder:
        :param backtrack_folder:
        :type backtrack_folder:
        :return:
        :rtype:
        """
        file_paths = []
        for root, dirs, files in os.walk(os.path.join(base_audio_folder, backtrack_folder)):
            for name in files:
                file_name, file_extension = os.path.splitext(name)
                if file_extension == '.wav':
                    filepath = os.path.join(root, name)
                    file_paths.append(filepath)
        return backtrack_folder, file_paths

    def getAllBacktracksInAllFolders(self):
        return self.allBacktracksInAllFolders

    @staticmethod
    def initialize():
        pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=1024)
        pygame.mixer.init()
        pygame.init()

    # def convertNewFiles(self):
    #     return
    #     # we try to convert all files put by the user. It is needed because we only want PCM 16 bits
    #     # TODO make test to this to easier implementation
    #     print(self.user_waveDir)
    #     for filename in os.listdir(self.user_waveDir):
    #         filenameFull = os.path.join(self.user_waveDir, filename)
    #         # print("will tyr to convert " , filenameFull)
    #         try:
    #             data, sampleRate = soundfile.read(filenameFull)
    #             outfile = os.path.join(self.processed_waveDir, filename)
    #             soundfile.write(outfile, data, sampleRate, subtype="PCM_16")
    #             print("done")
    #         except Exception as e:
    #             print("error during conversion", filename)
    #             logging.exception(e)

    def loadTick(self):
        pygame.mixer.music.load(self.metroTick)

    @staticmethod
    def playTick():
        pygame.mixer.music.play()

    def simplePlay(self, audio_file_path: str):
        self.stopPlay()
        try:
            pygame.mixer.music.load(audio_file_path)
            sound = pygame.mixer.Sound(audio_file_path)
            # pygame.mixer.music.set_pos(0)
            # we keep trace of the current file if we want to retreive it for the lick recording
            self.currentFile = audio_file_path
            self.currentFileLength = sound.get_length()
            print("Current audio file is ... :",
                  sound.get_length(), " ms, ", self.currentFile)
            # _thread.start_new_thread(self.testLatency, (time.time(),))
            pygame.mixer.music.play(loops=-1, fade_ms=200)
            self.isPlaying = True
        except Exception as e:
            logging.exception(e)
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

    @staticmethod
    def getBusy():
        return pygame.mixer.get_busy()

    def playRealMetro(self, bpm_asked):
        # the metro is handle a little differently than files it is considered as a sound (and not a music)
        # the sample is created and loop indefinitely.
        self.stopPlay()
        self.unloadAudio()
        bpm = float(bpm_asked)  # just for example
        # we must first calculate the length of 1 bar / 4 (1 tick + 1 space)
        tick_duration = 60.0 / bpm  # this value is in seconds
        # we must calculate the total length of the buffer according to audio
        # 1 sec = 44100 samples  * 2 channels => 88200 samples
        # we then determine the number of samples needed
        samples_needed = tick_duration * 44100 * 2 * 2

        bpmTick = pygame.mixer.Sound(file=self.metroTick)
        raw_array = bpmTick.get_raw()
        tick_sample_length = len(raw_array)
        if tick_sample_length < samples_needed:
            how_many_samples_missing = int(samples_needed - tick_sample_length)
            print('missing samples ', how_many_samples_missing)
            empty_bytes = bytes(how_many_samples_missing)
            raw_array += empty_bytes
            # we must have a pair number of bytes to suppress any glitch sound
            if len(raw_array) % 2 != 0 :
                raw_array += b'\x00'

        # here we can construct 1 bar
        raw_array += raw_array  # (2ticks)
        raw_array += raw_array  # (4 ticks)
        # and a second bar
        raw_array += raw_array  # (8 ticks)
        # double again
        raw_array += raw_array  # (8 ticks)
        # and again
        raw_array += raw_array  # (8 ticks)
        self.realMetro = pygame.mixer.Sound(buffer=raw_array)
        self.isPlaying = True
        print("PLAYING METRO, VOLUME: ", self.audioVolume)
        self.setVolume(self.audioVolume)
        self.realMetro.play(-1)

    def stopPlay(self):
        self.isPlaying = False
        pygame.mixer.music.stop()
        if self.realMetro is not None:
            try:
                self.realMetro.stop()
            except Exception as e:
                logging.exception(e)

    # def convertToWav(self, filename):
    #     sound = AudioSegment.from_file(filename, format="wav")
    #     sound.set_frame_rate
    #     baseName = os.path.basename(filename)
    #     exportName = os.path.splitext(baseName)[0]
    #     exportName = "out.wav"
    #     print("outname ", exportName)
    #     sound.export(os.path.join(self.waveDir, exportName),
    #                  format="wav", bitrate="16k")
    #
    #     return exportName

    def getIsPlaying(self) -> bool:
        return self.isPlaying

    @staticmethod
    def unloadAudio():
        print("try unload ....")
        pygame.mixer.music.unload()

    @staticmethod
    def getVolume():
        actualVol = pygame.mixer.music.get_volume()
        print('Getting actual volume ...', actualVol)
        return actualVol

    def setVolume(self, value):
        self.audioVolume = value
        print("Updating sound volume ...", self.audioVolume)
        pygame.mixer.music.set_volume(self.audioVolume)
        if self.realMetro is not None:
            try:
                self.realMetro.set_volume(self.audioVolume)
            except Exception as e:
                logging.exception(e)
                print('cannot change volume of metronome')

    # def setMetroVolume(value):
    # self.realMetro.set_volume(value)

    def getCurrentTrack(self):
        return self.currentFile, self.currentFileLength

    @staticmethod
    def getTimePlayed():
        return pygame.mixer.music.get_pos() / 1000

    def prepareBacktrackForRecord(self, backtrackFile):
        # print(backtrackFile)
        pygame.mixer.music.stop()
        pygame.mixer.music.load(backtrackFile)

    @staticmethod
    def playBacktrackForRecord(nbOfLoops):
        pygame.mixer.music.play(loops=nbOfLoops)

        # start a thread

    def stopBacktrackForRecord(self):
        pass

    @staticmethod
    def checkIsPlayingMusic():
        return pygame.mixer.music.get_busy()
