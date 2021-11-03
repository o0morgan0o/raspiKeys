import threading
from enum import Enum
import time
import pygame

from src.game.autoload import Autoload
from src.game.utils.audio import Audio
from src.game.utils.midiToNotenames import noteNameFull
from src.game.utils.licksUtils import createJsonMidiLickFromNotes, writeJsonLick


class RecordNotesModes(Enum):
    RECORD_ONLY_CHORDS = "record_only_chords"
    RECORD_CHORDS_WITH_ADDITIONAL_LICK = "record_chord_with_additional_lick"


class GameState(Enum):
    GAME_WAITING_FOR_USER_LICK_KEY = "game_waiting_for_user_lick_key"
    GAME_READY_FOR_RECORDING_CHORDS = "game_ready_for_recording_chords"
    GAME_RECORDING_STARTED = "game_recording_started"
    GAME_RECORDING_FINISHED = "game_recording_finished"


MUSIC_FINISHED = pygame.USEREVENT + 1


class ProgressRecordingThread(threading.Thread):
    def __init__(self, master, view, audio_instance, audio_file_path, number_of_loops):
        threading.Thread.__init__(self)
        self.view = view
        self.master = master
        self.audioInstance = audio_instance
        self.audioFilePath = audio_file_path
        self.numberOfLoops = number_of_loops
        self.progressThreadAlive = True
        self.innerTest = False

    def run(self):
        while self.progressThreadAlive:
            # calculate the percentage played
            total_length = Audio.getAudioFileLength(self.audioFilePath) * self.numberOfLoops
            percentage_played_full = self.audioInstance.getTimePlayed() / total_length
            percentage_played = percentage_played_full % 1
            self.view.setUiUpdateProgress(percentage_played * 100)
            for event in pygame.event.get():
                if event.type == MUSIC_FINISHED:
                    self.progressThreadAlive = False
        self.master.finishedRecording()
        print("PROGRESS THREAD FINISHED")


class RecordLickViewModel:
    def __init__(self, view, backtrack_file: str):
        self.view = view
        self.backtrackFile = backtrack_file
        self.audioInstance = Autoload.get_instance().getAudioInstance()
        self.midiIO = Autoload.get_instance().getMidiInstance()
        self.midiIO.setCallback(self.handleMIDIInput)
        self.midiIO.setListening(True)

        self.gameState = GameState.GAME_WAITING_FOR_USER_LICK_KEY.value

        self.lickKey: int = -1
        self.recordingType = None
        self.numberOfLoopsRecording = 2
        self.progressThread = None

        self.startingTime = 0
        self.chordNotes = []
        self.damper = []
        self.damperIsActive = False

        self.view.setUiInitializeView(self.backtrackFile, self.numberOfLoopsRecording)

    def onBtnReadyForRecordingClick(self):
        """ function triggered when the user validate the Key choose for the lick. """
        # first we check if the key is not null
        if self.lickKey == -1:
            return self.view.setUiShowError("KEY MUST BE SET !")
        self.gameState = GameState.GAME_READY_FOR_RECORDING_CHORDS.value
        self.view.resetLblError()
        self.view.showUiFrameReadyForRecordingChords()

    def onBtnMinusNumberOfLoopsClick(self):
        self.numberOfLoopsRecording += -1
        if self.numberOfLoopsRecording <= 1:
            self.numberOfLoopsRecording = 1
        self.view.setUiInitializeView(self.backtrackFile, self.numberOfLoopsRecording)

    def onBtnPlusNumberOfLoopsClick(self):
        self.numberOfLoopsRecording += 1
        self.view.setUiInitializeView(self.backtrackFile, self.numberOfLoopsRecording)

    def onBtnSaveClick(self):
        lick_id, json = createJsonMidiLickFromNotes(
            lick_name='',
            lick_key= self.lickKey,
            backtrack_file=self.backtrackFile,
            number_of_loops=self.numberOfLoopsRecording,
            chord_notes=self.chordNotes,
        )
        # TODO make an interface for the user for naming file
        writeSuccess = writeJsonLick(json, lick_id)
        if writeSuccess:
            self.view.setUiShowMessage(message_string="FILE SAVED SUCCESS")
        else:
            self.view.setUiShowError(error_string="ERROR WHILE SAVING THE FILE")

    def onBtnCancelClick(self):
        self.audioInstance.stopPlay()
        if self.progressThread is not None and self.progressThread.isAlive():
            self.progressThread.progressThreadAlive = False
        self.view.recordFrame.destroy()

    def startRecording(self):
        if self.progressThread is not None and self.progressThread.isAlive():
            # we cancel previous progress thread
            self.progressThread.progressThreadAlive = False
        self.progressThread = ProgressRecordingThread(
            master=self,
            view=self.view,
            audio_instance=self.audioInstance,
            audio_file_path=self.backtrackFile,
            number_of_loops=self.numberOfLoopsRecording)

        # we launch the backtrack
        self.gameState = GameState.GAME_RECORDING_STARTED.value
        self.startingTime = int(round(time.time() * 1000))
        # print("first starting Time trigger", self.startingTime)
        self.audioInstance.simplePlay(self.backtrackFile, loops=self.numberOfLoopsRecording)
        self.progressThread.start()
        self.view.setUiFrameRecordingStarted()
        pygame.mixer.music.set_endevent(MUSIC_FINISHED)

    def finishedRecording(self):
        self.gameState = GameState.GAME_RECORDING_FINISHED.value
        self.view.showUiFrameFinishedRecording()
        print(self.chordNotes)

    def getTimeFromStart(self):
        return int(round(time.time() * 1000)) - self.startingTime

    def handleMIDIInput(self, msg):
        # check if user has midi listen
        if not self.midiIO.getListeningState():
            print("[--] ignoring queue message...", msg)
            return
        print("[-]receiving something", msg)

        if self.gameState == GameState.GAME_WAITING_FOR_USER_LICK_KEY.value:
            if msg.type == "note_on" and msg.velocity > 10:
                self.lickKey = msg.note
                self.view.setUiShowLickKey(noteNameFull(self.lickKey))
        elif self.gameState == GameState.GAME_READY_FOR_RECORDING_CHORDS.value:
            if msg.type == "note_on":
                self.startRecording()
        elif self.gameState == GameState.GAME_RECORDING_STARTED.value:
            # here all the notes are recorded
            self.handleMIDIInputDuringRecording(msg)

    def handleMIDIInputDuringRecording(self, msg):
        if msg.type == "control_change":
            if msg.control == 64 and msg.value > 64:
                self.damperIsActive = True
            if msg.control == 64 and msg.value <= 64:
                self.damperIsActive = False
                print("release damper", self.damper)
                for dampenedNote in self.damper:
                    mTime = self.getTimeFromStart()
                    note_dict = {"type": "note_off", "note": dampenedNote, "velocity": 127, "time": mTime}
                self.damper = []
        else:
            if self.damperIsActive and msg.type == "note_off":
                self.damper.append(msg.note)
                return
            else:
                mTime = self.getTimeFromStart()
                note_dict = {"type": msg.type, "note": msg.note, "velocity": msg.velocity, "time": mTime}
                self.chordNotes.append(note_dict)

    # def destroy(self):
    #     self.view.destroy()
