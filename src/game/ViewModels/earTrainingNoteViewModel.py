from random import choice

from src.game.autoload import Autoload
from src.game.utils.midiToNotenames import noteNameFull
from src.game.utils.questionNote import playWinMelody
from src.game.utils.utilFunctions import *
from src.game.utils.waitingNote import WaitingNote
from src.game.utils.questionNote import CustomNote
from src.game.utils.config import getNoteDelay, getMaxIntervalQuestionNote, updateEarTrainingNoteMaxInterval, updateEarTrainingNoteDelay, getMidiVolume
from enum import Enum


class GameStates(Enum):
    GAME_NOT_STARTED = "game_not_started"
    GAME_INITIALIZATION = "game_initialization"
    GAME_WAITING_USER_INPUT = "game_waiting_user_input"
    GAME_SET_NOTE_QUESTION = "game_set_note_question"
    GAME_WAITING_USER_ANSWER = "game_waiting_user_answer"
    GAME_CPU_PLAY_NOTE = "cpu_play_note"
    GAME_SHOWING_RESULT = "game_showing_result"

    class ViewStrings(Enum):
        CURRENT_MIDI_IN: str = "MIDI in: "
        CURRENT_MIDI_OUT: str = "MIDI out: "


class EarTrainingNoteViewModel:
    def __init__(self, view):
        self.view = view

        self.midiIO = Autoload.get_instance().getMidiInstance()
        self.midiIO.setCallback(self.handleMIDIInput)

        self.intervalMax = getMaxIntervalQuestionNote()
        self.delay = getNoteDelay()

        # variable for user score
        self.counter = 0
        self.score = 0

        self.originNote = None
        self.questionNote = None
        self.questionInterval = None

        self.stopGame = False
        self.waitingNotes = []
        self.initMIDIArray(128)

        # gameState is used to know when the user is guessing
        self.gameState = GameStates.GAME_NOT_STARTED.value

        # startGame
        self.startingNote = -1
        self.startGame()

        # self.parentRight.btnSkip.configure(command=self.skip)
        self.initializeIntervalSlider()
        self.initializeNoteDelaySlider()

    def initializeIntervalSlider(self):
        self.view.slInterval.set(self.intervalMax)

    def initializeNoteDelaySlider(self):
        self.view.slDelay.set(self.delay)

    # noinspection PyUnusedLocal
    def updateSliderIntervalCallback(self, event):
        new_value = self.view.slInterval.get()
        self.intervalMax = new_value
        updateEarTrainingNoteMaxInterval(new_value)

    # noinspection PyUnusedLocal
    def updateSliderDelayCallback(self, event):
        new_value = self.view.slDelay.get()
        self.delay = new_value
        updateEarTrainingNoteDelay(new_value)

    # def skip(self):
    #     try:
    #         self.view.result["text"] = "It was ;-)\n{}".format(formatOutputInterval(self.questionNote.note - self.startingNote))
    #         self.view.result["bg"] = "orange"
    #         # if we gave the good answer, we want a new note
    #         self.changeGameState(GameStates.GAME_WAITING_USER_INPUT.value)
    #     except BaseException as e:
    #         print("impossible to skip question", e)

    def startGame(self):
        self.midiIO.setListening(True)
        self.changeGameState(GameStates.GAME_INITIALIZATION.value)

    def changeGameState(self, new_state: str, note_received: int = None):
        print("SWITCHING GAME_STATE TO {}".format(new_state), note_received)
        self.gameState = new_state
        if new_state == GameStates.GAME_NOT_STARTED.value:
            pass

        if new_state == GameStates.GAME_INITIALIZATION.value:
            # We set here the interval of the question. We will later get the question note from the user input
            self.questionInterval = self.pickQuestionInterval(self.view.slInterval.get())
            self.changeGameState(GameStates.GAME_WAITING_USER_INPUT.value)
            self.view.reinitializeUi()

        elif new_state == GameStates.GAME_WAITING_USER_INPUT.value:
            # When in this game state, a midi input will trigger the change to the next game state
            pass

        elif new_state == GameStates.GAME_SET_NOTE_QUESTION.value:
            self.originNote = note_received
            self.view.setUiStateSetNoteQuestion(noteNameFull(self.originNote))
            self.questionNote = self.getNewQuestionNote(note_received, self.questionInterval)
            self.changeGameState(GameStates.GAME_CPU_PLAY_NOTE.value)

        elif new_state == GameStates.GAME_CPU_PLAY_NOTE.value:
            delay_before_on = 0.4
            note_duration = 0.4
            CustomNote(self.midiIO, self.questionNote, delay_before_on, note_duration, getMidiVolume(),
                       callback_after_note_off=lambda: self.changeGameState(GameStates.GAME_WAITING_USER_ANSWER.value)
                       )

        elif new_state == GameStates.GAME_WAITING_USER_ANSWER.value:
            self.view.setUiStateWaitingAnswer()
            # When in this game state, a midi input will trigger the change to the next game state

        elif new_state == GameStates.GAME_SHOWING_RESULT.value:
            self.view.setUiStateShowingResult(noteNameFull(note_received))
            difference = self.checkAnswer(note_received, self.questionNote)
            print("difference ", difference)
            if difference == 0:
                # win
                self.showWinUi()
                self.processWin()
            else:
                # loose
                self.showLooseUi(note_received)
                self.processLoose()

    def showWinUi(self):
        intervalReadableText = formatOutputInterval(self.questionNote - self.originNote)
        self.view.setUiStateWin(noteNameFull(self.questionNote), intervalReadableText)

    def processWin(self):
        midi_win_melody_volume = int(float(getMidiVolume()) * 3 / 4)
        playWinMelody(self.midiIO, midi_win_melody_volume, callback_after_melody=self.changeGameState(GameStates.GAME_INITIALIZATION.value))

    def showLooseUi(self, note_received: int):
        intervalReadableText = formatOutputInterval(note_received - self.originNote)
        self.view.setUiStateLoose(noteNameFull(note_received), intervalReadableText)

    def processLoose(self):
        self.changeGameState(GameStates.GAME_SET_NOTE_QUESTION.value, self.originNote)
        pass

    # init a 128 array of WaitingNote in order to store all the timers
    def initMIDIArray(self, max_note: int):
        for i in range(max_note):
            self.waitingNotes.append(WaitingNote(i, self))

    # def checkAnswerA(self, answer: int):
    # self.view.lblNoteUser.lift()
    # if answer == self.questionNote.note:
    # else:
    # # self.parentRight.result.place(x=20, y=210, width=env.RIG)
    # self.view.lblNoteUser.lower()
    # self.midiIO.panic()
    # pass

    @staticmethod
    def checkAnswer(m_answer: int, m_question: int):
        return m_answer - m_question

    @staticmethod
    def pickQuestionInterval(max_interval: int) -> int:
        return choice([i for i in range(-max_interval, max_interval) if i not in [0]])

    @staticmethod
    def getNewQuestionNote(starting_note: int, question_interval: int) -> int:
        result = starting_note + question_interval
        result = 0 if result <= 0 else result
        result = 127 if result >= 127 else result
        return result

    def handleMIDIInput(self, msg):
        # check if user has midi  listen
        if not self.midiIO.getListeningState():
            print("[--] Ignoring queue message...", msg)
            return
        print("[-]receiving something", msg)

        if self.gameState == GameStates.GAME_WAITING_USER_INPUT.value:
            if msg.type == "note_on" and msg.velocity > 10:
                self.changeGameState(GameStates.GAME_SET_NOTE_QUESTION.value, msg.note)

        if self.gameState == GameStates.GAME_WAITING_USER_ANSWER.value:
            # we allow the player to replay the origin note freely
            if msg.note == self.originNote:
                return
            if msg.type == "note_on" and msg.velocity > 10:
                self.changeGameState(GameStates.GAME_SHOWING_RESULT.value, msg.note)

    def destroy(self):
        self.midiIO.setCallback(None)
