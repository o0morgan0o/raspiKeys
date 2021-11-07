import random
import threading
from enum import Enum

import pygame
from PIL import Image, ImageTk

from src.game import env
from src.game.autoload import Autoload
from src.game.utils.licksUtils import getAllMidiLicksFiles, getJsonDataFromFile, JsonLickFields
from src.game.utils.midiToNotenames import noteNameFull
from src.game.utils.questionNote import CustomNote

MUSIC_FINISHED = pygame.USEREVENT + 1
MUSIC_CANCELED = pygame.USEREVENT + 2


class TranspositionMode(Enum):
    TRANSPOSE_RANDOM = "transpose_random"
    TRANSPOSE_SEQUENTIAL = "transpose_sequential"


class ProgressThread(threading.Thread):
    def __init__(self, view, audio_instance, number_of_loops, number_of_cycles_each_transpose, callback, cycle_counter):
        threading.Thread.__init__(self)
        self.view = view
        self.audioInstance = audio_instance
        self.numberOfLoops = number_of_loops
        self.cycleCounter = cycle_counter
        self.numberOfCyclesEachTranspose = number_of_cycles_each_transpose
        self.callback = callback
        self.progressThreadAlive = True
        self.innerTest = False

    def run(self):
        while self.progressThreadAlive:
            # calculate the percentage played
            total_length = self.audioInstance.getCurrentFileLength() * self.numberOfLoops * self.numberOfCyclesEachTranspose
            percentage_played_full = (self.audioInstance.getTimePlayed()) / total_length
            percentage_played = percentage_played_full + (self.cycleCounter / self.numberOfCyclesEachTranspose)
            self.view.setUiUpdateProgress(percentage_played * 100)
            for event in pygame.event.get():
                if event.type == MUSIC_FINISHED:
                    print("BACKTRACK FINISHED")
                    self.progressThreadAlive = False
                    self.callback()
                if event.type == MUSIC_CANCELED:
                    self.progressThreadAlive = False
        self.view.setUiUpdateProgress(0.0)
        print("PROGRESS THREAD FINISHED")


class ViewImages:
    def __init__(self):
        self.playImage = ImageTk.PhotoImage(Image.open(env.PLAY_IMAGE))
        self.pauseImage = ImageTk.PhotoImage(Image.open(env.PAUSE_IMAGE))
        self.shuffleImage = ImageTk.PhotoImage(Image.open(env.SHUFFLE_IMAGE))


class PractiseLicksViewModel:
    def __init__(self, view):
        self.view = view
        self.midiIO = Autoload.get_instance().getMidiInstance()
        self.audioInstance = Autoload.get_instance().getAudioInstance()

        self.images = ViewImages()
        self.progressThread = None

        # Default path
        self.midiRepository = env.MIDI_FOLDER

        self.customNotesList = []

        self.lick_midi_key = None
        self.backtrack_file = None
        self.number_of_loops_recording = None
        self.chord_notes = None
        self.melody_notes = None

        self.transpositionMode = TranspositionMode.TRANSPOSE_RANDOM.value
        self.cyclesCounter = 0
        self.currentTranspose = 0

        self.numberOfCyclesForEachTranspose = 2

        self.allMidiLicksFilePaths = getAllMidiLicksFiles()
        self.currentLickData = None
        self.allLicksData = self.getAllLicksData(self.allMidiLicksFilePaths)
        self.allLicksDataForTreeView = self.extractLicksDataForTreeView(self.allLicksData)
        self.initializeTreeView(self.allLicksDataForTreeView)

    def initializeTreeView(self, all_list_data_for_tree_view: list):
        self.view.setUiInitializeTreeView(all_list_data_for_tree_view)
        first_item = self.view.getFirstTreeViewItem()
        if first_item is not None:
            self.view.setTreeViewSelectItem(first_item)

    def reloadLicks(self):
        self.view.clearTreeView()
        self.allMidiLicksFilePaths = getAllMidiLicksFiles()
        self.currentLickData = None
        self.allLicksData = self.getAllLicksData(self.allMidiLicksFilePaths)
        self.allLicksDataForTreeView = self.extractLicksDataForTreeView(self.allLicksData)
        self.initializeTreeView(self.allLicksDataForTreeView)

    def playCycle(self):
        nextTranspose = None
        self.view.setUiResetLblNextKeyIndication()
        if self.cyclesCounter == self.numberOfCyclesForEachTranspose - 1:
            nextTranspose = self.getNextTransposeOffset(transposition_mode=self.transpositionMode, current_transpose=self.currentTranspose)
            humanReadableNextTranspose = noteNameFull(nextTranspose)[:-1]
            self.view.setUiUpdateLblNextKeyIndication(next_key=humanReadableNextTranspose)
        if self.cyclesCounter == self.numberOfCyclesForEachTranspose:
            self.cyclesCounter = 0

        new_readable_key = noteNameFull(self.lick_midi_key + self.currentTranspose)[:-1]  # we remove the octave
        self.view.setUiUpdateLblForLickSelected(lick_key=new_readable_key)

        self.audioInstance.simplePlay(self.backtrack_file, loops=self.number_of_loops_recording, fade_in=0)
        self.progressThread = ProgressThread(self.view,
                                             audio_instance=self.audioInstance,
                                             number_of_loops=self.number_of_loops_recording,
                                             number_of_cycles_each_transpose=self.numberOfCyclesForEachTranspose,
                                             callback=self.cycleFinished,
                                             cycle_counter=self.cyclesCounter,
                                             )
        self.playChordNotes(self.chord_notes, transpose=self.currentTranspose)
        self.progressThread.start()
        self.cyclesCounter += 1
        if nextTranspose is not None:
            self.currentTranspose = nextTranspose

    def cancelPlayingThread(self):
        pygame.mixer.music.set_endevent(MUSIC_CANCELED)
        self.cyclesCounter = 0
        self.currentTranspose = 0
        self.audioInstance.stopPlay()
        noteList = self.customNotesList
        if len(noteList) != 0:
            for custom_note in noteList:
                custom_note.timer.cancel()
        self.midiIO.panic()

    def cycleFinished(self):
        print("CYCLE CALLBACK !!")
        self.playCycle()

    def onBtnPlayClick(self):
        if self.audioInstance.getIsPlaying():
            self.cancelPlayingThread()
            return
        self.cancelPlayingThread()
        # print(self.currentLickData)
        if self.currentLickData is None:
            return print("No lick data found")
        self.lick_midi_key = self.currentLickData[JsonLickFields.FIELD_LICK_KEY.value]
        self.backtrack_file = self.currentLickData[JsonLickFields.FIELD_BACKTRACK_FILE.value]
        self.number_of_loops_recording = self.currentLickData[JsonLickFields.FIELD_NUMBER_OF_LOOPS.value]
        self.chord_notes = self.currentLickData[JsonLickFields.FIELD_CHORD_NOTES.value]
        self.melody_notes = self.currentLickData[JsonLickFields.FIELD_MELODY_NOTES.value]

        self.playCycle()
        pygame.mixer.music.set_endevent(MUSIC_FINISHED)

    @staticmethod
    def getNextTransposeOffset(transposition_mode, current_transpose: int) -> int:
        # we have 3 modes here, random, or regular transposition
        if transposition_mode == TranspositionMode.TRANSPOSE_RANDOM.value:
            return random.choice([i for i in range(-5, 6) if i not in [current_transpose]])
        elif transposition_mode == TranspositionMode.TRANSPOSE_SEQUENTIAL.value:
            pass
        else:
            raise Exception("Unknown transposition mode")

    def onLickSelectedInTreeView(self, values: dict):
        print('selected', values)
        (lick_uuid, lick_key, lick_description, lick_date) = values
        # we retrieve the complete original midi data
        self.view.setUiUpdateLblForLickSelected(lick_key=lick_key)
        self.currentLickData = self.findLickDataFromLickUuid(lick_uuid)

    def playChordNotes(self, chord_notes: list, transpose: int):
        self.customNotesList = []
        for note_data in chord_notes:
            print(note_data)
            self.customNotesList.append(
                CustomNote(
                    midi_instance=self.midiIO,
                    note=note_data['note'] + transpose,
                    delay_on=note_data['time'] / 1000,
                    note_type=note_data['type'],
                    velocity=note_data['velocity']
                ))

    def findLickDataFromLickUuid(self, lick_uuid: str):
        for lick in self.allLicksData:
            if lick['lick_id'] == lick_uuid:
                return lick

    @staticmethod
    def getAllLicksData(all_licks_files: list):
        all_licks_data = []
        for m_file in all_licks_files:
            all_licks_data.append(getJsonDataFromFile(m_file))
        return all_licks_data

    @staticmethod
    def extractLicksDataForTreeView(all_licks_data: list):
        if len(all_licks_data) == 0:
            return
        all_licks_data_short = []
        for lick in all_licks_data:
            element = {JsonLickFields.FIELD_LICK_ID.value: lick[JsonLickFields.FIELD_LICK_ID.value],
                       JsonLickFields.FIELD_LICK_DATE.value: lick[JsonLickFields.FIELD_LICK_DATE.value],
                       JsonLickFields.FIELD_LICK_NAME.value: lick[JsonLickFields.FIELD_LICK_NAME.value],
                       JsonLickFields.FIELD_LICK_KEY.value: lick[JsonLickFields.FIELD_LICK_KEY.value]}
            all_licks_data_short.append(element)
        return all_licks_data_short
