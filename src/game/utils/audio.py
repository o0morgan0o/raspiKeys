import logging
import subprocess
import os
import threading

import pygame

from src.game import env
from src.game.utils.colors import Colors


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

    def buildBacktrackWithModifiedSpeed(self, speed_variation, origin_file):
        """ Spawn a rubberband-cli in order to convert backtrack to another tempo """
        if speed_variation == 0:
            return origin_file
        # map the value of speed variation from [-1, 1] to [0.5, 2]
        interpolater = self.make_interpolater(-1, 1, 0.5, 2)
        speed_multiplier = interpolater(speed_variation)
        print('will make interpolation to value: ', speed_multiplier)

        out_file_path = self.getFilePathFromTempWavFolder(file_name='modifiedSpeedWav_tmp.wav')
        in_file_path = origin_file
        stretch_command = 'rubberband "{}" "{}" -T {} --realtime --quiet'.format(in_file_path, out_file_path, speed_multiplier)
        print(stretch_command)
        stretchingSpeedProcess = subprocess.Popen(stretch_command, shell=True, stdout=subprocess.PIPE)
        stretchingSpeedProcess.wait()
        stretchingResult = stretchingSpeedProcess.returncode
        if stretchingResult != 0:
            print("ERROR During rubberband process")
        else:
            print('File converted to {}'.format(out_file_path))
        return out_file_path, speed_multiplier

    @staticmethod
    def make_interpolater(left_min, left_max, right_min, right_max):
        # Figure out how 'wide' each range is
        leftSpan = left_max - left_min
        rightSpan = right_max - right_min
        # Compute the scale factor between left and right values
        scaleFactor = float(rightSpan) / float(leftSpan)
        print('scaleFactor: ', scaleFactor)

        # create interpolation function using pre-calculated scaleFactor
        def interp_fn(value):
            return right_min + (value - left_min) * scaleFactor

        return interp_fn

    @staticmethod
    def getFilePathFromTempPngFolder(file_name):
        return os.path.join(env.TEMP_FOLDER_FOR_WAVEFORM_TIMELINE_PNG, file_name)

    @staticmethod
    def getFilePathFromTempWavFolder(file_name):
        return os.path.join(env.TEMP_FOLDER_FOR_MODIFIED_SPEED_BACKTRACK, file_name)

    def getCurrentFileLength(self):
        return self.currentFileLength

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
        all_folders = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]
        all_folders.sort()
        return all_folders

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

    def loadTick(self):
        pygame.mixer.music.load(self.metroTick)

    @staticmethod
    def playTick():
        pygame.mixer.music.play()

    @staticmethod
    def generateWaveformTimelineForFile(audio_file_path: str, audio_length, callback):
        print('Audiowaveform png creation', 'audio length', audio_length)
        png_outfile_path = Audio.getFilePathFromTempPngFolder(file_name='waveform-timeline.png')
        audiowaveform_cmd = 'audiowaveform -i "{}" -o "{}" -e {} --no-axis-labels --background-color {} --waveform-color {} -q'.format(
            audio_file_path, png_outfile_path, audio_length, Colors.WAVEFORM_BACKGROUND_COLOR[1:], Colors.WAVEFORM_FOREGROUND_COLOR[1:])
        pngWaveformCreationProcess = subprocess.Popen(audiowaveform_cmd, shell=True, stdout=subprocess.PIPE)
        pngWaveformCreationProcess.wait()
        pngResult = pngWaveformCreationProcess.returncode
        if pngResult != 0:
            print("ERROR During rubberband process")
        else:
            print('File converted to {}'.format(png_outfile_path))
        callback(png_outfile_path)

    def simplePlay(self, audio_file_path: str, loops: int = -1, fade_in=200, callback_after_waveform_creation=None):
        self.stopPlay()
        try:
            pygame.mixer.music.load(audio_file_path)
            sound = pygame.mixer.Sound(audio_file_path)
            # we keep trace of the current file if we want to retrieve it for the lick recording
            self.currentFile = audio_file_path
            self.currentFileLength = sound.get_length()
            # if we have a callback for waveform creation, we create the waveform (audiowaveform C++ library)
            if callback_after_waveform_creation is not None:
                threading.Thread(target=self.generateWaveformTimelineForFile, args=(audio_file_path, self.currentFileLength, callback_after_waveform_creation)).start()

            print("Current audio file is ... :",
                  sound.get_length(), " ms, ", self.currentFile)
            # _thread.start_new_thread(self.testLatency, (time.time(),))
            pygame.mixer.music.play(loops=loops, fade_ms=fade_in)
            self.isPlaying = True
        except Exception as e:
            logging.exception(e)
            print("can't play file !!")

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
            if len(raw_array) % 2 != 0:
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
        print("PLAYING METRO, VOLUME: ", self.audioVolume)
        self.setVolume(self.audioVolume)
        self.isPlaying = True
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

    def getCurrentTrack(self):
        return self.currentFile, self.currentFileLength

    @staticmethod
    def getAudioFileLength(audio_file_path: str):
        return pygame.mixer.Sound(audio_file_path).get_length()

    @staticmethod
    def getTimePlayed():
        return pygame.mixer.music.get_pos() / 1000

    @staticmethod
    def prepareBacktrackForRecord(backtrack_file):
        pygame.mixer.music.stop()
        pygame.mixer.music.load(backtrack_file)

    @staticmethod
    def playBacktrackForRecord(number_of_loops):
        pygame.mixer.music.play(loops=number_of_loops)

    def stopBacktrackForRecord(self):
        pass

    @staticmethod
    def checkIsPlayingMusic():
        return pygame.mixer.music.get_busy()
