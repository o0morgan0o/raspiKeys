import os
import random
import threading

from src.game.autoload import Autoload
from src.game.utils.config import getMetroBpm, getAudioVolume, updateMetroBpm


# from src.game.mode2.recordWithBacktrack import RecordWithBacktrack
# from src.game.utils.canvasThread import MyThreadForBacktrackScreen

class ProgressThread(threading.Thread):
    def __init__(self, view, audio_instance):
        threading.Thread.__init__(self)
        self.view = view
        self.audioInstance = audio_instance
        self.progressThreadAlive = True
        self.innerTest = False

    def run(self):
        while self.progressThreadAlive:
            # calculate the percentage played
            percentage_played_full = self.audioInstance.getTimePlayed() / self.audioInstance.currentFileLength
            percentage_played = percentage_played_full % 1
            self.view.setUiUpdateProgress(percentage_played * 100)
        print("PROGRESS THREAD FINISHED")


class BacktracksViewModel:
    def __init__(self, view):
        self.view = view

        self.midiIO = Autoload.get_instance().getMidiInstance()
        self.midiIO.setCallback(self.handleMIDIInput)
        self.audioInstance = Autoload.get_instance().getAudioInstance()

        self.currentTrack = None
        self.tracksWav = None

        self.progressThread = None

        self.tempoMetronome = getMetroBpm()
        self.allBacktracksInAllCategories = self.audioInstance.getAllBacktracksInAllFolders()
        self.currentBacktrack = None

        # recording variables
        # self.recordingBassLick = False
        # self.recordingNotes = False

        # self.recordingCustomChords = False
        # self.recordedNotes = []
        # self.recordedCustomChords = []
        #
        # self.damper = []
        # self.damperActive = False
        self.initializeAudio()
        self.initializeBacktracks(self.allBacktracksInAllCategories)

    def initializeAudio(self):
        volume = getAudioVolume()
        self.audioInstance.setVolume(volume)
        self.view.setUiLblMetronome(self.tempoMetronome)

    def initializeBacktracks(self, all_backtracks_in_all_categories: list):
        category_counter: int = 0
        for category_tuple in all_backtracks_in_all_categories:
            category_name, backtracks_in_category = category_tuple
            nb_of_backtracks_in_category = len(backtracks_in_category)
            self.view.setUiAddBtnCategory(category_counter, category_name, nb_of_backtracks_in_category)
            category_counter += 1

    def onBtnPlayClick(self):
        if self.audioInstance.getIsPlaying():
            self.audioInstance.stopPlay()
        else:
            self.playBacktrack(self.currentBacktrack)

    def onBtnRandom(self):
        random_category_index = random.randint(0, len(self.allBacktracksInAllCategories) - 1)
        self.onBtnCategoryClick(random_category_index)

    def onBtnCategoryClick(self, _id: int):
        #     # TODO should display somewhere the number of files in the category and the index
        category_tuple_clicked = self.allBacktracksInAllCategories[_id]
        category_name, category_backtracks = category_tuple_clicked
        if len(category_backtracks) <= 0:
            print("Empty backtrack list in category", category_name)
            return
        # we pick  a random track in the tuple selected
        random_index = random.randint(0, len(category_backtracks))
        random_backtrack = category_backtracks[random_index]
        self.currentBacktrack = random_backtrack
        filename = os.path.basename(random_backtrack)
        print("next_audio_file: ", self.currentBacktrack)
        self.view.setUiCurrentBacktrack(category_name, filename, random_index, len(category_backtracks))
        self.playBacktrack(self.currentBacktrack)

    def onBtnMetronomeClick(self):
        self.audioInstance.playRealMetro(self.tempoMetronome)

    def onBtnBpmPlusClick(self):
        self.modifyMetroBpm(+10)

    def onBtnBpmMinusClick(self):
        self.modifyMetroBpm(-10)

    def restartMetronome(self):
        self.audioInstance.stopPlay()
        self.audioInstance.playRealMetro(self.tempoMetronome)

    def modifyMetroBpm(self, variation: int):
        minBpm = 10
        maxBpm = 190
        self.tempoMetronome += variation
        if self.tempoMetronome <= minBpm:  # 10 is the minimum tempo
            self.tempoMetronome = minBpm
        if self.tempoMetronome >= maxBpm:
            self.tempoMetronome = maxBpm
        self.view.setUiLblMetronome(self.tempoMetronome)
        self.restartMetronome()
        updateMetroBpm(self.tempoMetronome)

    def showWithOrWithoutBacktrackWindow(self, ):
        self.cancelThreads()
        try:
            del self.parent.recordWindow
        except Exception as e:
            print(e)
        self.parent.destroy()
        self.destroy()
        self.globalRoot.recordWindow = RecordWithBacktrack(self.globalRoot, self.app)

    def playBacktrack(self, current_track: str):
        if self.progressThread is not None and self.progressThread.isAlive():
            # we cancel previous progress thread
            self.progressThread.progressThreadAlive = False
        self.audioInstance.simplePlay(current_track)

        self.progressThread = ProgressThread(self.view, self.audioInstance)
        self.progressThread.start()

    def handleMIDIInput(self, msg):
        print(msg)
        # if msg.type == "control_change":
        #     print("pedal ... : ", msg.control, msg.value)
        #     if msg.control == 64 and msg.value > 64:
        #         self.damperActive = True
        #     if msg.control == 64 and msg.value <= 64:
        #         self.damperActive = False
        #         print(self.damper)
        #         self.damper = []

        # if self.damperActive == True and msg.type == "note_off":
        #     self.damper.append(msg.note)

        # # No handle because we want to ignore the midi input messages
        pass

    def destroy(self):
        self.audioInstance.stopPlay()
