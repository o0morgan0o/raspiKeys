from enum import Enum
from random import choice

from src.game.autoload import Autoload
from src.game.utils.config import getNoteDelay, getMaxIntervalQuestionNote, updateEarTrainingNoteMaxInterval, updateEarTrainingNoteDelay, getMidiVolume
from src.game.utils.midiToNotenames import noteNameFull
from src.game.utils.questionNote import CustomNote
from src.game.utils.questionNote import playWinMelody
from src.game.utils.utilFunctions import *


class GameStates(Enum):
    GAME_NOT_STARTED = "game_not_started"
    GAME_INITIALIZATION = "game_initialization"
    GAME_WAITING_USER_INPUT = "game_waiting_user_input"
    GAME_SET_NOTE_QUESTION = "game_set_note_question"
    GAME_WAITING_USER_ANSWER = "game_waiting_user_answer"
    GAME_CPU_PLAY_NOTE = "cpu_play_note"
    GAME_SHOWING_RESULT = "game_showing_result"


class WaitingInput(Enum):
    WAITING_INPUT_COMING_FROM_START_GAME = "coming_from_start_game"
    WAITING_INPUT_COMING_FROM_WIN = "coming_from_win"
    WAITING_INPUT_COMING_FROM_LOOSE = "coming_from_loose"
    WAITING_INPUT_COMING_FROM_SKIP = "coming_from_skip"


class EarTrainingNoteViewModel:
    def __init__(self, view):
        self.view = view
        self.midiIO = Autoload.get_instance().getMidiInstance()
        self.midiIO.setCallback(self.handleMIDIInput)

        self.intervalMax = getMaxIntervalQuestionNote()
        self.delay = getNoteDelay()
        self.velocity = 100

        # variable for user score
        self.counter = 0
        self.score = 0

        self.questionCustomNote = None
        self.originNoteMidiNumber = None
        self.questionMidiNumber = None
        self.questionInterval = None

        # gameState is used to know when the user is guessing
        self.gameState = GameStates.GAME_NOT_STARTED.value

        # startGame
        self.startGame()

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
        self.view.updateLblMaxInterval(new_value)

    # noinspection PyUnusedLocal
    def updateSliderDelayCallback(self, event):
        new_value = self.view.slDelay.get()
        self.delay = new_value
        updateEarTrainingNoteDelay(new_value)
        self.view.updateLblNoteDelay(new_value)

    def skipQuestionCallback(self):
        self.changeGameState(GameStates.GAME_INITIALIZATION.value, coming_from=WaitingInput.WAITING_INPUT_COMING_FROM_SKIP.value)

    def startGame(self):
        self.midiIO.setListening(True)
        self.changeGameState(GameStates.GAME_INITIALIZATION.value, coming_from=WaitingInput.WAITING_INPUT_COMING_FROM_START_GAME.value)

    def changeGameState(self, new_state: str, note_received: int = None, coming_from: str = None):
        print("SWITCHING GAME_STATE TO {}".format(new_state), note_received)
        self.gameState = new_state
        if new_state == GameStates.GAME_NOT_STARTED.value:
            pass

        if new_state == GameStates.GAME_INITIALIZATION.value:

            if coming_from == WaitingInput.WAITING_INPUT_COMING_FROM_START_GAME.value:
                # This should be triggered juste once
                # We set here the interval of the question. We will later get the question note from the user input
                self.questionInterval = self.pickQuestionInterval(self.view.slInterval.get())
                self.view.reinitializeUi()
                self.changeGameState(GameStates.GAME_WAITING_USER_INPUT.value)
            elif coming_from == WaitingInput.WAITING_INPUT_COMING_FROM_WIN.value:
                self.questionInterval = self.pickQuestionInterval(self.view.slInterval.get())
                self.changeGameState(GameStates.GAME_WAITING_USER_INPUT.value)
            elif coming_from == WaitingInput.WAITING_INPUT_COMING_FROM_LOOSE.value:
                pass
            elif coming_from == WaitingInput.WAITING_INPUT_COMING_FROM_SKIP.value:
                if self.questionMidiNumber is None or self.originNoteMidiNumber is None:
                    return self.changeGameState(GameStates.GAME_WAITING_USER_INPUT.value)
                intervalReadableText = formatOutputInterval(self.questionMidiNumber - self.originNoteMidiNumber)
                self.questionInterval = self.pickQuestionInterval(self.view.slInterval.get())
                self.view.setUiStateSkippedQuestion(noteNameFull(self.questionMidiNumber), intervalReadableText)
                self.changeGameState(GameStates.GAME_WAITING_USER_INPUT.value)
            else:
                raise BaseException("Error in Waiting User Input state, No coming_from value set.")

        elif new_state == GameStates.GAME_WAITING_USER_INPUT.value:
            # When in this game state, a midi input will trigger the change to the next game state
            pass

        elif new_state == GameStates.GAME_SET_NOTE_QUESTION.value:
            self.originNoteMidiNumber = note_received
            self.view.setUiStateSetNoteQuestion(noteNameFull(self.originNoteMidiNumber))
            self.questionMidiNumber = self.getNewQuestionNote(note_received, self.questionInterval)
            self.changeGameState(GameStates.GAME_CPU_PLAY_NOTE.value)

        elif new_state == GameStates.GAME_CPU_PLAY_NOTE.value:
            delay_before_on = float(self.delay)
            note_duration = 0.4
            self.questionCustomNote = CustomNote(self.midiIO,
                                                 note=self.questionMidiNumber,
                                                 delay_on=delay_before_on,
                                                 note_duration=note_duration,
                                                 velocity=self.velocity,
                                                 callback_after_note_off=lambda: self.changeGameState(GameStates.GAME_WAITING_USER_ANSWER.value)
                                                 )

        elif new_state == GameStates.GAME_WAITING_USER_ANSWER.value:
            self.view.setUiStateWaitingAnswer()
            # When in this game state, a midi input will trigger the change to the next game state

        elif new_state == GameStates.GAME_SHOWING_RESULT.value:
            self.view.setUiStateShowingResult(noteNameFull(note_received))
            difference = self.checkAnswer(note_received, self.questionMidiNumber)
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
        intervalReadableText = formatOutputInterval(self.questionMidiNumber - self.originNoteMidiNumber)
        self.view.setUiStateWin(noteNameFull(self.questionMidiNumber), intervalReadableText)

    def processWin(self):
        print('SHOULD PLAY WIN')
        playWinMelody(self.midiIO, self.velocity,
                      callback_after_melody=self.changeGameState(
                          GameStates.GAME_INITIALIZATION.value,
                          coming_from=WaitingInput.WAITING_INPUT_COMING_FROM_WIN.value)
                      )

    def showLooseUi(self, note_received: int):
        intervalReadableText = formatOutputInterval(note_received - self.originNoteMidiNumber)
        self.view.setUiStateLoose(noteNameFull(note_received), intervalReadableText)

    def processLoose(self):
        self.changeGameState(GameStates.GAME_SET_NOTE_QUESTION.value, self.originNoteMidiNumber)
        pass

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
            print("[--] ignoring queue message...", msg)
            return
        print("[-]receiving something", msg)

        if self.gameState == GameStates.GAME_WAITING_USER_INPUT.value:
            if msg.type == "note_on" and msg.velocity > 10:
                self.changeGameState(GameStates.GAME_SET_NOTE_QUESTION.value, msg.note)

        if self.gameState == GameStates.GAME_WAITING_USER_ANSWER.value:
            # we allow the player to replay the origin note freely
            if msg.note == self.originNoteMidiNumber:
                return
            if msg.type == "note_on" and msg.velocity > 10:
                self.changeGameState(GameStates.GAME_SHOWING_RESULT.value, msg.note)

    def destroyViewModel(self):
        print('Delete EarTrainingNoteViewModel')
        self.midiIO.setCallback(None)
        self.midiIO.setListening(False)
        if self.questionCustomNote is not None:
            self.questionCustomNote.timer.cancel()

