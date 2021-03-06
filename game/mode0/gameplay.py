import time
import threading
import random
from threading import Timer
import mido
import simpleaudio as sa

from game.utils.waitingNote import WaitingNote
from game.utils.questionNote import QuestionNote
from game.utils.midiIO import MidiIO
from game.utils.utilFunctions import formatOutputInterval
from game.autoload import Autoload

from game.utils.audio import Audio

from game.utils.questionNote import CustomNote
from game.utils.questionNote import Melody
from game.utils.midiToNotenames import noteName
from game.utils.midiToNotenames import noteNameFull


""" the mode 0 is for eartraining on a SINGLE INTERVAL """


class Game:
    def __init__(self, parent, config):
        self.config = config
        self.parent = parent
        # print("config mode 0 ",config)
        self.delay = float(config["question_delay"]) / 100
        self.isListening = False

        # variable for user score
        self.counter = 0
        self.score = 0
        self.globalIsListening = True

        debug = True
        self.stopGame = False
        self.waitingNotes = []
        self.initMIDIArray(128)

        self.midiIO = Autoload().getInstance()
        self.midiIO.setCallback(self.handleMIDIInput)

        # gamestate is used to know when the user is guessing
        self.gameState = "notStarted"

        # startGame
        self.startGame()
        self.startingNote = -1

        self.changeAllBg("black")
        self.parent.btnSkip.configure(command=self.skip)

        self.maxInterval = 12

    def toggleGlobalListen(self):
        if self.globalIsListening == True:
            self.globalIsListening = False
            self.parent.btnListen.configure(text="ListenOFF")
        else:
            self.globalIsListening = True
            self.parent.btnListen.configure(text="ListenON")

    def skip(self):
        try:
            self.parent.label2["text"] = "It was ;-)\n{}".format(formatOutputInterval(self.questionNote.note - self.startingNote))
            self.parent.label2["bg"] = "orange"
            # if we gave the good answer, we want a new note
            self.changeGameState("waitingUserInput")
        except:
            print("impossible to skip question")

    def startGame(self):
        self.changeGameState("waitingUserInput")
        self.melodies = Melody(self)

    def destroy(self):
        # print("destroying...")
        # self.isListening = False
        # self.midiIO.destroy() # delete everything in midiIO class
        self.midiIO.setCallback(None)

        # del self.waitingNotes # delete WantingNotes
        # del self

    def changeGameState(self, newstate):
        if newstate == "notStarted":
            pass
        elif newstate == "waitingUserInput":
            self.parent.label1["text"] = "Pick a starting Note"
            self.gameState = "waitingUserInput"
            percentage = int((self.score / self.counter) * 100) if (self.counter != 0) else 0
            self.parent.label3["text"] = "{}/{} ({}%)".format(self.score, self.counter, percentage)
        elif newstate == "listen":
            # self.parent["bg"] = "orange"
            # self.changeAllBg("orange")
            self.parent.label1["text"] = "Listen ..."
            self.parent.label2["text"] = ""
            self.parent.label2["bg"] = "black"
            self.parent.lblNoteUser["text"] = ""
            self.gameState = "listen"
            self.isListening = False
        elif newstate == "waitingUserAnswer":
            self.isListening = True
            # self.parent["bg"] = "blue"
            # self.changeAllBg("blue")
            self.parent.label1["text"] = "What is your answer ?"
            self.gameState = "waitingUserAnswer"

    # init a 128 array of WaitingNote in order to store all the timers

    def initMIDIArray(self, maxNote):
        for i in range(maxNote):
            self.waitingNotes.append(WaitingNote(i, self))

    # callback launched when the timer is at 0
    def noteOff(self, note):
        if self.isListening == False:
            return
        self.midiIO.sendOut("note_off", note)

    # prepare the future midi noteOff it is stored in waitingNotes list

    def prepareNoteOut(self, mNote, offset=0):
        if self.gameState == "waitingUserInput":
            self.changeGameState("listen")
        elif self.gameState == "listen":
            self.changeGameState("waitingUserAnswer")
        self.midiIO.sendOut("note_on", mNote)  # send note on
        currentNote = self.waitingNotes[mNote]
        currentNote.resetTimer(offset)

    def checkAnswer(self, answer):
        if answer == self.questionNote.note:
            self.parent.label2["text"] = "correct ;-)\n{}".format(formatOutputInterval(self.questionNote.note - self.startingNote))
            self.parent.label2["bg"] = "green"
            self.parent.lblNoteUser["text"] = noteNameFull(answer)
            self.parent.lblNoteUser["fg"] = "green"
            if self.questionNote.isFirstTry:
                self.score = self.score + 1

            # TODO : is it really the best way to do time.sleep here ?
            # if we gave the good answer, we want a new note
            self.changeGameState("waitingUserInput")
            time.sleep(0.4)
            self.melodies.playWinMelody()
            time.sleep(0.4)
        else:
            self.parent.label2["text"] = "incorrect\nA: {}".format(formatOutputInterval(answer - self.startingNote))
            self.questionNote.isFirstTry = False
            self.parent.label2["bg"] = "red"
            self.parent.lblNoteUser["text"] = noteNameFull(answer)
            self.parent.lblNoteUser["fg"] = "red"

            # time.sleep(1)
            # self.melodies.playLooseMelody()
            # time.sleep(1)
            # we replay the interval if the user didnt find the correct answer
            time.sleep(0.4)
            self.changeGameState("listen")
            # i want to replay both notes
            self.replayNote = QuestionNote(self.startingNote, self, 0)
            # i want to replay both notes
            self.replayNote = QuestionNote(self.questionNote.note, self, 0 + self.delay)

        self.midiIO.panic()

    def pickNewNote(self, startingNote):
        self.counter = self.counter + 1
        # TODO : make the max interval customizable
        maxInterval = self.maxInterval
        offset = 0
        while offset == 0:  # we dont want the same note than the starting note
            offset = random.randint(-maxInterval, maxInterval)
        return startingNote + offset

    def handleQuestionNote(self, mNote):
        self.prepareNoteOut

    def changeAllBg(self, newColor):
        self.parent.label1["bg"] = newColor
        self.parent.label2["bg"] = newColor
        self.parent.label3["bg"] = newColor
        self.parent.lblNote["bg"] = newColor
        self.parent.lblNote["fg"] = "white"
        self.parent.label1["fg"] = "white"
        self.parent.label2["fg"] = "white"
        self.parent.label3["fg"] = "white"

    def handleMIDIInput(self, msg):
        # used for the midiListening button
        if Autoload().getInstance().isListening == False:  # check if user has midi  listen
            return
        if self.globalIsListening == False:
            return
        # Needed because we still receive signals even if the class is destroyed
        if self.isListening == False:
            print("[--] Ignoring queue message...", msg, self.isListening)
            return

        print("[-]receiving something", msg, self.isListening)
        if msg.type == "note_on" and msg.velocity > 10:
            # we test according to the gamestate

            if self.gameState == "waitingUserInput":
                self.changeGameState("listen")
                self.startingNote = msg.note
                # pick a random note
                questionNote = self.pickNewNote(self.startingNote)
                self.questionNote = QuestionNote(questionNote, self, self.delay)
                # show the note on the ui
                self.lblUserShow = noteNameFull(self.startingNote) + "-> "
                self.parent.lblNote.config(text=self.lblUserShow)

            elif self.gameState == "waitingUserAnswer":
                if msg.note == self.startingNote:
                    # we want to ignore the starting note for the user.
                    return
                self.checkAnswer(msg.note)  # we check the answer
