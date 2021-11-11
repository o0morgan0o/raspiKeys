from enum import Enum

from src.game.autoload import Autoload
from src.game.utils.config import getMidiVolume, getNoteDuration, updateEarTrainingNoteDuration
from src.game.utils.midiChords import MidiChords
from src.game.utils.midiToNotenames import noteNameFull
from src.game.utils.questionNote import CustomNote, playWinMelody
from src.game.utils.config import updateEarTrainingNoteDelay, getNoteDelay


class GameStates(Enum):
    GAME_NOT_STARTED = "game_not_started"
    GAME_INITIALIZATION = "game_initialization"
    GAME_WAITING_USER_INPUT = "game_waiting_user_input"
    GAME_SET_CHORD_QUESTION = "game_set_note_question"
    GAME_WAITING_USER_ANSWER = "game_waiting_user_answer"
    GAME_CPU_PLAY_CHORD = "cpu_play_note"
    GAME_SHOWING_RESULT = "game_showing_result"


class WaitingInput(Enum):
    WAITING_INPUT_COMING_FROM_START_GAME = "coming_from_start_game"
    WAITING_INPUT_COMING_FROM_WIN = "coming_from_win"
    WAITING_INPUT_COMING_FROM_LOOSE = "coming_from_loose"
    WAITING_INPUT_COMING_FROM_SKIP = "coming_from_skip"


class EarTrainingChordViewModel:
    def __init__(self, view):
        self.view = view
        self.midiIO = Autoload.get_instance().getMidiInstance()
        self.midiIO.setCallback(self.handleMIDIInput)

        # variable for user score
        self.counter = 0
        self.score = 0

        self.originNote = None
        self.velocity = 100

        self.noteDelay = getNoteDelay()
        self.noteDuration = getNoteDuration()
        print('NOTE DURATION', self.noteDuration)

        self.questionChord = None
        self.questionQualityChord = None
        self.userNotesAnswer = []

        # gameState is used to know when the user is guessing
        self.gameState = GameStates.GAME_NOT_STARTED.value

        # startGame
        self.startGame()

        self.initializeNoteDelaySlider()
        self.initializeNoteDurationSlider()

    # def skip(self):
    #     try:
    #         notesAnswer = ""
    #         for note in self.questionArray:
    #             notesAnswer += noteName(note) + "-"
    #         self.view.lblNote.config(font=("Courier", 18, "bold"))
    #         self.view.lblNote["text"] = "It was\n{}".format(notesAnswer)
    #         # .format(formatOutputInterval(self.questionNote.note - self.startingNote))
    #         self.view.lblNote["bg"] = "orange"
    #         self.changeGameState("waitingUserInput")  # if we gave the good answer, we want a new note
    #     except Exception as e:
    #         print("Impossible to skip question", e)

    def initializeNoteDelaySlider(self):
        self.view.slDelay.set(self.noteDelay)
        self.view.updateLblNoteDelay(self.noteDelay)

    def initializeNoteDurationSlider(self):
        self.view.slDuration.set(self.noteDuration)
        self.view.updateLblNoteDuration(self.noteDuration)

    def getQuestionChordNotes(self) -> list:
        chord_quality, origin_note, notes = self.questionChord
        return notes

    def getQuestionChordQuality(self) -> str:
        chord_quality, origin_note, notes = self.questionChord
        return chord_quality

    def getQuestionChordNotesHumanReadable(self) -> list:
        question_notes = self.getQuestionChordNotes()
        human_readable_notes = []
        for note in question_notes:
            human_readable_notes.append(noteNameFull(note))
        return human_readable_notes

    def onSliderDelayMoved(self, event):
        self.noteDelay = self.view.slDelay.get()
        updateEarTrainingNoteDelay(new_value=self.noteDelay)
        self.view.updateLblNoteDelay(self.noteDelay)

    def onSliderDurationMoved(self, event):
        self.noteDuration = self.view.slDuration.get()
        updateEarTrainingNoteDuration(new_value=self.noteDuration)
        self.view.updateLblNoteDuration(self.noteDuration)

    def startGame(self):
        self.midiIO.setListening(True)
        self.changeGameState(GameStates.GAME_INITIALIZATION.value, coming_from=WaitingInput.WAITING_INPUT_COMING_FROM_START_GAME.value)

    def changeGameState(self, new_state: str, note_received: int = None, coming_from: str = None):
        print("SWITCHING GAME_STATE TO {}".format(new_state), note_received)
        self.gameState = new_state
        if new_state == GameStates.GAME_NOT_STARTED.value:
            pass

        elif new_state == GameStates.GAME_INITIALIZATION.value:
            if coming_from == WaitingInput.WAITING_INPUT_COMING_FROM_START_GAME.value:
                # This should be triggered juste once
                # We set here the interval of the question. We will later get the question note from the user input
                self.questionQualityChord = self.pickNewChordQuestion()
                self.view.reinitializeUi()
                self.changeGameState(GameStates.GAME_WAITING_USER_INPUT.value)
            elif coming_from == WaitingInput.WAITING_INPUT_COMING_FROM_WIN.value:
                self.questionQualityChord = self.pickNewChordQuestion()
                self.changeGameState(GameStates.GAME_WAITING_USER_INPUT.value)
            elif coming_from == WaitingInput.WAITING_INPUT_COMING_FROM_SKIP.value:
                pass
            else:
                raise BaseException("Error in Waiting User Input state, No coming_from value set.")

        elif new_state == GameStates.GAME_WAITING_USER_INPUT.value:
            # When in this game state, a midi input will trigger the change to the next game state
            pass
        elif new_state == GameStates.GAME_SET_CHORD_QUESTION.value:
            self.userNotesAnswer = []
            self.originNote = note_received
            self.view.setUiStateChordQuestion(noteNameFull(self.originNote))
            self.questionChord = self.generateQuestionNotesFromQualityChord(self.originNote, self.questionQualityChord)
            print('question note', self.questionChord)
            self.changeGameState(GameStates.GAME_CPU_PLAY_CHORD.value)
        elif new_state == GameStates.GAME_CPU_PLAY_CHORD.value:
            # additional delay to be more convenient and enjoyable for the user
            additional_delay_before_playing_question = 0.8
            delay_before_on = self.noteDelay
            note_duration = self.noteDuration
            notes = self.getQuestionChordNotes()
            for i in range(0, len(notes)):
                note = notes[i]
                if i == len(notes) - 1:
                    CustomNote(self.midiIO,
                               note=note,
                               delay_on=additional_delay_before_playing_question + delay_before_on * i,
                               note_duration=note_duration,
                               velocity=self.velocity,
                               callback_after_note_off=lambda: self.changeGameState(GameStates.GAME_WAITING_USER_ANSWER.value)
                               )
                else:
                    CustomNote(self.midiIO,
                               note=note,
                               delay_on=additional_delay_before_playing_question + delay_before_on * i,
                               note_duration=note_duration,
                               velocity=self.velocity,
                               )

        elif new_state == GameStates.GAME_WAITING_USER_ANSWER.value:
            self.view.setUiStateWaitingAnswer()
            # When in this game state, a midi input will trigger the recording of the user notes

        elif new_state == GameStates.GAME_SHOWING_RESULT.value:
            areAllNotesCorrect = self.checkAnswer(self.userNotesAnswer, self.getQuestionChordNotes())
            if areAllNotesCorrect:
                # win
                self.showWinUi()
                self.processWin()
            else:
                # loose
                self.showLooseUi()
                self.processLoose()

    def showWinUi(self):
        self.view.setUiStateWin(noteNameFull(self.originNote), self.getQuestionChordQuality(), self.getQuestionChordNotesHumanReadable())

    def processWin(self):
        playWinMelody(self.midiIO, self.velocity,
                      callback_after_melody=self.changeGameState(
                          GameStates.GAME_INITIALIZATION.value,
                          coming_from=WaitingInput.WAITING_INPUT_COMING_FROM_WIN.value)
                      )

    def showLooseUi(self):
        self.view.setUiStateLoose()

    def processLoose(self):
        self.changeGameState(GameStates.GAME_SET_CHORD_QUESTION.value, self.originNote)

    @staticmethod
    def checkAnswer(user_answer: list, correct_answer: list):
        if len(user_answer) != len(correct_answer):
            raise Exception("Length of user answer is different from length of all the questions !")
        error_found = False
        for i in range(0, len(user_answer)):
            if user_answer[i] != correct_answer[i]:
                error_found = True
        if error_found:
            return False
        return True

    @staticmethod
    def pickNewChordQuestion() -> tuple:
        """ Return a tuple containing the readable name of the chord quality, and the intervals corresponding to the chord"""
        return MidiChords().pickRandom()

    @staticmethod
    def generateQuestionNotesFromQualityChord(starting_note: int, chord_tuple: tuple):
        chord_name, chord_notes = chord_tuple
        midi_converted_notes = []
        for note in chord_notes:
            midi_converted_notes.append(starting_note + note)
        return chord_name, starting_note, midi_converted_notes

    def handleMIDIInput(self, msg):
        if not self.midiIO.getListeningState():
            print("[--] Ignoring queue message...", msg)
            return
        print("[-]receiving something", msg)

        if self.gameState == GameStates.GAME_WAITING_USER_INPUT.value:
            if msg.type == "note_on" and msg.velocity > 10:
                self.changeGameState(GameStates.GAME_SET_CHORD_QUESTION.value, msg.note)

        elif self.gameState == GameStates.GAME_WAITING_USER_ANSWER.value:
            if msg.type == "note_on" and msg.velocity > 10:
                isUserAnswerComplete = self.addNoteToUserAnswer(msg.note)
                if isUserAnswerComplete:
                    self.changeGameState(GameStates.GAME_SHOWING_RESULT.value)

    def addNoteToUserAnswer(self, note) -> bool:
        self.userNotesAnswer.append(note)
        print('question', self.getQuestionChordNotes(), 'current answer : ', self.userNotesAnswer)
        # if we get the correct number of notes, we return True
        return len(self.userNotesAnswer) >= len(self.getQuestionChordNotes())

    def destroyViewModel(self):
        print('Delete EarTrainingChordViewModel')
        self.midiIO.cancelCallback()
        self.midiIO.setListening(False)
