import os
import random
import threading
from enum import Enum

from src.game.autoload import Autoload
from src.game.utils.config import getMetroBpm, getAudioVolume, updateMetroBpm


class BacktracksConstants(Enum):
    TEMPO_MIN_BPM = 10
    TEMPO_MAX_BPM = 190


class GameStatesNames(Enum):
    GAME_STATE_BACKTRACK_MODE_ACTIVE = "game_state_backtrack_mode_active"
    GAME_STATE_METRO_MODE_ACTIVE = "game_state_metro_mode_active"


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
        self.view.setUiUpdateProgress(0.0)
        print("PROGRESS THREAD FINISHED")


class BacktracksViewModel:
    def __init__(self, view):
        self.view = view

        self.midiIO = Autoload.get_instance().getMidiInstance()
        # self.midiIO.setCallback(self.handleMIDIInput)
        self.audioInstance = Autoload.get_instance().getAudioInstance()

        self.tracksWav = None
        self.progressThread = None

        self.tempoMetronome = getMetroBpm()
        self.allBacktracksInAllCategories = self.audioInstance.getAllBacktracksInAllFolders()
        self.currentBacktrack = None

        self.initializeAudio()
        self.initializeBacktracks(self.allBacktracksInAllCategories)

        self.gameState = None

        # DEBUG
        # TODO Remove this
        # self.currentBacktrack = 'D:\\code\\raspiKeys\\src\\res\\backtracks\\processed_wav\\house\\S_L_127_BEATS_30.wav'
        # self.onBtnRecordClick()

    def switchToBacktrackGameMode(self):
        self.stopPlayWithProgressBarReset()
        self.view.setUiShowBacktrackSection()
        self.gameState = GameStatesNames.GAME_STATE_BACKTRACK_MODE_ACTIVE.value

    def switchToMetroGameMode(self):
        if self.gameState != GameStatesNames.GAME_STATE_METRO_MODE_ACTIVE.value:
            self.stopPlayWithProgressBarReset()
            self.view.setUiShowMetronomeSection()
            self.gameState = GameStatesNames.GAME_STATE_METRO_MODE_ACTIVE.value
            return True
        return False

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

    @staticmethod
    def getCategoryByCategoryNameInAllBacktracks(all_backtracks_in_all_categories_tuples, category_name: str):
        for category in all_backtracks_in_all_categories_tuples:
            (_name, _tracks) = category
            if _name == category_name:
                return category
        return None

    def onBtnRecordClick(self):
        self.stopPlayWithProgressBarReset()
        if self.currentBacktrack is not None:
            self.view.setUiSpawnRecordWindow(self.currentBacktrack)

    def onBtnPlayClick(self):
        print("STATE", self.gameState, "IS playing ", self.audioInstance.getIsPlaying())
        if self.audioInstance.getIsPlaying():
            return self.stopPlayWithProgressBarReset()
        if self.gameState == GameStatesNames.GAME_STATE_BACKTRACK_MODE_ACTIVE.value:
            if self.currentBacktrack is None:
                return self.onBtnRandomClick()
            if self.audioInstance.getIsPlaying():
                self.stopPlayWithProgressBarReset()
            else:
                self.playBacktrack(self.currentBacktrack)
        elif self.gameState == GameStatesNames.GAME_STATE_METRO_MODE_ACTIVE.value:
            self.onBtnMetronomeClick()

    def onBtnRandomClick(self):
        self.gameState = GameStatesNames.GAME_STATE_BACKTRACK_MODE_ACTIVE.value
        # TODO: Refactor this section with random choice method
        # we must get only non null categories
        non_empty_categories = []
        for category in self.allBacktracksInAllCategories:
            tuple_chosen, category_tracks = category
            if len(category_tracks) != 0:
                non_empty_categories.append(category)
        # we pick a random category
        random_category_index = random.randint(0, len(non_empty_categories) - 1)
        random_result = non_empty_categories[random_category_index]
        # (category_name, _tracks) = tuple_chosen
        self.onBtnCategoryClick(random_result[0])

    def onBtnCategoryClick(self, category_name: str):
        self.gameState = GameStatesNames.GAME_STATE_BACKTRACK_MODE_ACTIVE.value
        # TODO should display somewhere the number of files in the category and the index
        category_tuple_clicked = self.getCategoryByCategoryNameInAllBacktracks(self.allBacktracksInAllCategories, category_name)
        category_name, category_backtracks = category_tuple_clicked
        if len(category_backtracks) <= 0:
            print("Empty backtrack list in category", category_name)
            return
        # we pick  a random track in the tuple selected
        random_index = random.randint(0, len(category_backtracks) - 1)
        random_backtrack = category_backtracks[random_index]
        self.currentBacktrack = random_backtrack
        filename = os.path.basename(random_backtrack)
        print("next_audio_file: ", self.currentBacktrack)
        self.view.setUiCurrentBacktrack(category_name, filename, random_index, len(category_backtracks))
        self.playBacktrack(self.currentBacktrack)

    def onBtnMetronomeClick(self):
        hasChangedState = self.switchToMetroGameMode()
        if hasChangedState:
            self.audioInstance.playRealMetro(self.tempoMetronome)
            self.view.setUiChangePlayingIcons(is_playing=True)
            return
        if self.audioInstance.getIsPlaying():
            self.audioInstance.stopPlay()
            self.view.setUiChangePlayingIcons(is_playing=False)
        else:
            self.audioInstance.playRealMetro(self.tempoMetronome)
            self.view.setUiChangePlayingIcons(is_playing=True)

    def onBtnBpmPlusClick(self):
        self.modifyMetroBpm(+10)

    def onBtnBpmMinusClick(self):
        self.modifyMetroBpm(-10)

    def onSliderTempoMoved(self, event):
        new_value = self.view.slTempo.get()
        self.tempoMetronome = new_value
        self.view.setUiLblMetronome(self.tempoMetronome)
        self.restartMetronome()
        updateMetroBpm(self.tempoMetronome)

    def restartMetronome(self):
        self.stopPlayWithProgressBarReset()
        self.onBtnMetronomeClick()

    def modifyMetroBpm(self, variation: int):
        minBpm = BacktracksConstants.TEMPO_MIN_BPM.value
        maxBpm = BacktracksConstants.TEMPO_MAX_BPM.value
        self.tempoMetronome += variation
        if self.tempoMetronome <= minBpm:  # 10 is the minimum tempo
            self.tempoMetronome = minBpm
        if self.tempoMetronome >= maxBpm:
            self.tempoMetronome = maxBpm
        self.view.setUiLblMetronome(self.tempoMetronome)
        self.restartMetronome()
        updateMetroBpm(self.tempoMetronome)

    def playBacktrack(self, current_track: str):
        self.view.setUiShowBacktrackSection()
        if self.progressThread is not None and self.progressThread.isAlive():
            # we cancel previous progress thread
            self.progressThread.progressThreadAlive = False
        self.audioInstance.simplePlay(current_track)
        self.view.setUiChangePlayingIcons(is_playing=True)

        self.progressThread = ProgressThread(self.view, self.audioInstance)
        self.progressThread.start()

    def stopPlayWithProgressBarReset(self):
        self.audioInstance.stopPlay()
        self.view.setUiChangePlayingIcons(is_playing=False)
        self.view.resetProgressBar()

    def destroy(self):
        self.audioInstance.stopPlay()
        self.view.setUiChangePlayingIcons(is_playing=False)
