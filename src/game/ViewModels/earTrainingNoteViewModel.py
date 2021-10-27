import random
import time

from src.game.autoload import Autoload
from src.game.utils.midiToNotenames import noteNameFull
from src.game.utils.questionNote import Melody
from src.game.utils.questionNote import QuestionNote
from src.game.utils.utilFunctions import *
from src.game.utils.waitingNote import WaitingNote
from src.game.utils.config import getNoteDelay, getMaxIntervalQuestionNote, updateEarTrainingNoteMaxInterval, updateEarTrainingNoteDelay, getMidiVolume
from enum import Enum


class GameStates(Enum):
    GAME_NOT_STARTED = "game_not_started"
    GAME_WAITING_USER_INPUT = "game_waiting_user_input"

    class ViewStrings(Enum):
        CURRENT_MIDI_IN: str = "MIDI in: "
        CURRENT_MIDI_OUT: str = "MIDI out: "

    GAME_WAITING_USER_ANSWER = "game_waiting_user_answer"
    GAME_CPU_PLAYING_NOTE = "cpu_is_playing_note"


class GameStrings(Enum):
    LABEL_PICK_NOTE = "Pick a starting note"
    LABEL_LISTEN = "Listen ..."
    LABEL_WHAT_IS_YOUR_ANSWER = "What is your answer ?"


class EarTrainingNoteViewModel:
    def __init__(self, view):
        self.melodies = Melody(self)
        self.view = view

        self.midiIO = Autoload.get_instance().getMidiInstance()
        self.midiIO.setCallback(self.handleMIDIInput)

        self.intervalMax = getMaxIntervalQuestionNote()
        self.delay = getNoteDelay()

        # variable for user score
        self.counter = 0
        self.score = 0
        self.globalIsListening = True

        self.questionNote = None
        self.stopGame = False
        self.waitingNotes = []
        self.initMIDIArray(128)

        # gameState is used to know when the user is guessing
        self.gameState = GameStates.GAME_NOT_STARTED.value

        # startGame
        self.startingNote = -1
        self.startGame()

        self.changeAllBg("black")
        # self.parentRight.btnSkip.configure(command=self.skip)
        self.initializeIntervalSlider()
        self.initializeNoteDelaySlider()

    def initializeIntervalSlider(self):
        self.view.slInterval.set(self.intervalMax)

    def initializeNoteDelaySlider(self):
        self.view.slDelay.set(self.delay)

    def updateSliderIntervalCallback(self, event):
        new_value = self.view.slInterval.get()
        self.intervalMax = new_value
        updateEarTrainingNoteMaxInterval(new_value)

    def updateSliderDelayCallback(self, event):
        new_value = self.view.slDelay.get()
        self.delay = new_value
        updateEarTrainingNoteDelay(new_value)

    # def toggleGlobalListen(self):
    #     if self.globalIsListening == True:
    #         self.globalIsListening = False
    #         self.parentRight.btnListen.configure(text="ListenOFF")
    #     else:
    #         self.globalIsListening = True
    #         self.parentRight.btnListen.configure(text="ListenON")

    def skip(self):
        try:
            self.view.result["text"] = "It was ;-)\n{}".format(formatOutputInterval(self.questionNote.note - self.startingNote))
            self.view.result["bg"] = "orange"
            # if we gave the good answer, we want a new note
            self.changeGameState(GameStates.GAME_WAITING_USER_INPUT.value)
        except BaseException as e:
            print("impossible to skip question", e)

    def startGame(self):
        self.changeGameState(GameStates.GAME_WAITING_USER_INPUT.value)
        self.midiIO.setListening(True)

    def changeGameState(self, new_state: str):
        if new_state == GameStates.GAME_NOT_STARTED.value:
            pass
        elif new_state == GameStates.GAME_WAITING_USER_INPUT.value:
            self.view.pickNote.config(text=GameStrings.LABEL_PICK_NOTE.value)
            self.gameState = GameStates.GAME_WAITING_USER_INPUT.value
            percentage = int((self.score / self.counter) * 100) if (self.counter != 0) else 0
            # self.parentRight.score["text"] = "{}/{} ({}%)".format(self.score, self.counter, percentage)
        elif new_state == GameStates.GAME_CPU_PLAYING_NOTE.value:
            # self.parentRight["bg"] = "orange"
            # self.changeAllBg("orange")
            self.view.pickNote.config(text=GameStrings.LABEL_LISTEN)
            self.view.result.config(text="", bg="black")
            self.view.lblNoteUser.config(text="")
            self.gameState = GameStates.GAME_CPU_PLAYING_NOTE.value
            self.isListening = False
        elif new_state == GameStates.GAME_WAITING_USER_ANSWER.value:
            self.isListening = True
            # self.parentRight["bg"] = "blue"
            # self.changeAllBg("blue")
            self.view.pickNote.config(text=GameStrings.LABEL_WHAT_IS_YOUR_ANSWER.value)
            self.gameState = GameStates.GAME_WAITING_USER_ANSWER.value

    # init a 128 array of WaitingNote in order to store all the timers
    def initMIDIArray(self, max_note: int):
        for i in range(max_note):
            self.waitingNotes.append(WaitingNote(i, self))

    # callback launched when the timer is at 0
    def noteOff(self, note):
        if not self.midiIO.getListeningState():
            return
        # WARNING !! check if it works because i dont know if at sendOut we must have the same MIDI volume of sendOn
        self.midiIO.sendOut("note_off", note, getMidiVolume())

    # prepare the future midi noteOff it is stored in waitingNotes list
    def prepareNoteOut(self, m_note: int, offset: int = 0):
        if self.gameState == GameStates.GAME_WAITING_USER_INPUT.value:
            self.changeGameState(GameStates.GAME_CPU_PLAYING_NOTE.value)
        elif self.gameState == GameStates.GAME_CPU_PLAYING_NOTE.value:
            self.changeGameState(GameStates.GAME_WAITING_USER_ANSWER.value)
        self.midiIO.sendOut("note_on", m_note, getMidiVolume())  # send note on
        currentNote = self.waitingNotes[m_note]
        currentNote.resetTimer(offset)

    def checkAnswer(self, answer):
        self.view.lblNoteUser.lift()
        if answer == self.questionNote.note:
            self.view.result["text"] = "correct ;-)\n{}".format(
                formatOutputInterval(self.questionNote.note - self.startingNote))
            self.view.result["bg"] = "green"
            self.view.lblNoteUser["text"] = noteNameFull(answer)
            self.view.lblNoteUser["fg"] = "green"
            if self.questionNote.isFirstTry:
                self.score += 1

            # TODO : is it really the best way to do time.sleep here ?
            # if we gave the good answer, we want a new note
            self.changeGameState(GameStates.GAME_WAITING_USER_INPUT.value)
            time.sleep(0.4)
            self.view.lblNote["text"] = ""
            self.melodies.playWinMelody(getMidiVolume())
            time.sleep(0.4)
        else:
            self.view.result["text"] = "incorrect\nA: {}".format(
                formatOutputInterval(answer - self.startingNote))
            self.questionNote.isFirstTry = False
            self.view.result["bg"] = "red"
            self.view.lblNoteUser["text"] = noteNameFull(answer)
            self.view.lblNoteUser["fg"] = "red"

            # time.sleep(1)
            # self.melodies.playLooseMelody()
            # time.sleep(1)
            # we replay the interval if the user didnt find the correct answer
            time.sleep(0.4)
            self.changeGameState(GameStates.GAME_CPU_PLAYING_NOTE.value)
            # i want to replay both notes
            self.replayNote = QuestionNote(self.startingNote, self, 0)

            # i want to replay both notes
            self.replayNote = QuestionNote(self.questionNote.note, self, 0 + self.delay)
            time.sleep(0.4)
        # self.parentRight.result.place(x=20, y=210, width=env.RIG)
        self.parent.lblNoteUser.lower()
        self.midiIO.panic()

    def pickNewNote(self, starting_note: int) -> int:
        self.counter += 1
        # maxInterval = self.maxInterval
        maxInterval = self.intervalMax
        offset = 0
        while offset == 0:  # we dont want the same note than the starting note
            offset = random.randint(-maxInterval, maxInterval)
        return starting_note + offset

    def handleQuestionNote(self, m_note: int):
        self.prepareNoteOut(m_note)

    def changeAllBg(self, newColor):
        pass
        # self.parentRight.result["bg"] = newColor
        # self.parentRight.score["bg"] = newColor
        # self.parentRight.lblNote["bg"] = newColor
        # self.parentRight.lblNote["fg"] = "white"
        # self.parentRight.result["fg"] = "white"
        # self.parentRight.score["fg"] = "white"
        #
        # self.parentRight.pickNote["bg"] = newColor
        # self.parentRight.pickNote["fg"] = "white"

    def handleMIDIInput(self, msg):
        # check if user has midi  listen
        if not self.midiIO.getListeningState():
            print("[--] Ignoring queue message...", msg)
            return
        # if self.globalIsListening == False:
        #     return

        print("[-]receiving something", msg)
        if msg.type == "note_on" and msg.velocity > 10:
            # we test according to the gameState

            if self.gameState == GameStates.GAME_WAITING_USER_INPUT.value:
                self.changeGameState(GameStates.GAME_CPU_PLAYING_NOTE.value)
                self.startingNote = msg.note
                # pick a random note
                questionNote = self.pickNewNote(self.startingNote)
                self.questionNote = QuestionNote(questionNote, self, self.delay)
                # show the note on the ui
                self.lblUserShow = noteNameFull(self.startingNote)
                self.view.lblNote.config(text=self.lblUserShow)

            elif self.gameState == GameStates.GAME_WAITING_USER_ANSWER.value:
                if msg.note == self.startingNote:
                    # we want to ignore the starting note for the user.
                    return
                self.checkAnswer(msg.note)  # we check the answer

    def destroy(self):
        # print("destroying...")
        # self.isListening = False
        # self.midiIO.destroy() # delete everything in midiIO class
        self.midiIO.setCallback(None)

        # del self.waitingNotes # delete WantingNotes
        # del self
