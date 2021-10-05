import time
import threading
from game import env
import random
from threading import Timer

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
    def __init__(self, parentLeft,parentRight, config):
        self.config = config
        self.parentLeft = parentLeft
        self.parentRight = parentRight
        # print("config mode 0 ",config)
        self.delay = float(config["question_delay"]) / 100
        self.isListening = False
        self.velocity = 100

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
        self.parentRight.btnSkip.configure(command=self.skip)
        self.parentLeft.slInterval.configure(command=self.changeIntervalSize)
        self.parentLeft.slMidiVolume.configure(command=self.changeMidiVolume)

        self.maxInterval = 12

    def changeIntervalSize(self, value):
        newValue = int(value)
        self.parentLeft.lblInterval.config(text="Interval Size : +-%s" % newValue)
        self.maxInterval = newValue

    def changeMidiVolume(self, value):
        newValue = int(value)
        self.parentLeft.lblMidiVolume.config(text="Midi Volume : %s" % newValue)
        self.velocity=newValue


    def toggleGlobalListen(self):
        if self.globalIsListening == True:
            self.globalIsListening = False
            self.parentRight.btnListen.configure(text="ListenOFF")
        else:
            self.globalIsListening = True
            self.parentRight.btnListen.configure(text="ListenON")

    def skip(self):
        try:
            self.parentRight.result["text"] = "It was ;-)\n{}".format(formatOutputInterval(self.questionNote.note - self.startingNote))
            self.parentRight.result["bg"] = "orange"
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
            self.parentRight.pickNote["text"] = "Pick a starting Note"
            self.gameState = "waitingUserInput"
            percentage = int((self.score / self.counter) * 100) if (self.counter != 0) else 0
            self.parentRight.score["text"] = "{}/{} ({}%)".format(self.score, self.counter, percentage)
        elif newstate == "listen":
            # self.parentRight["bg"] = "orange"
            # self.changeAllBg("orange")
            self.parentRight.pickNote["text"] = "Listen ..."
            self.parentRight.result["text"] = ""
            self.parentRight.result["bg"] = "black"
            self.parentRight.lblNoteUser["text"] = ""
            self.gameState = "listen"
            self.isListening = False
        elif newstate == "waitingUserAnswer":
            self.isListening = True
            # self.parentRight["bg"] = "blue"
            # self.changeAllBg("blue")
            self.parentRight.pickNote["text"] = "What is your answer ?"
            self.gameState = "waitingUserAnswer"

    # init a 128 array of WaitingNote in order to store all the timers

    def initMIDIArray(self, maxNote):
        for i in range(maxNote):
            self.waitingNotes.append(WaitingNote(i, self))

    # callback launched when the timer is at 0
    def noteOff(self, note):
        if self.isListening == False:
            return
        self.midiIO.sendOut("note_off", note, self.velocity)

    # prepare the future midi noteOff it is stored in waitingNotes list

    def prepareNoteOut(self, mNote, offset=0,):
        if self.gameState == "waitingUserInput":
            self.changeGameState("listen")
        elif self.gameState == "listen":
            self.changeGameState("waitingUserAnswer")
        self.midiIO.sendOut("note_on", mNote, self.velocity)  # send note on
        currentNote = self.waitingNotes[mNote]
        currentNote.resetTimer(offset)

    def checkAnswer(self, answer):
        self.parentRight.lblNoteUser.lift()
        if answer == self.questionNote.note:
            self.parentRight.result["text"] = "correct ;-)\n{}".format(formatOutputInterval(self.questionNote.note - self.startingNote))
            self.parentRight.result["bg"] = "green"
            self.parentRight.lblNoteUser["text"] = noteNameFull(answer)
            self.parentRight.lblNoteUser["fg"] = "green"
            if self.questionNote.isFirstTry:
                self.score = self.score + 1

            # TODO : is it really the best way to do time.sleep here ?
            # if we gave the good answer, we want a new note
            self.changeGameState("waitingUserInput")
            time.sleep(0.4)
            self.melodies.playWinMelody()
            time.sleep(0.4)
        else:
            self.parentRight.result["text"] = "incorrect\nA: {}".format(formatOutputInterval(answer - self.startingNote))
            self.questionNote.isFirstTry = False
            self.parentRight.result["bg"] = "red"
            self.parentRight.lblNoteUser["text"] = noteNameFull(answer)
            self.parentRight.lblNoteUser["fg"] = "red"

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
        # self.parentRight.result.place(x=20, y=210, width=env.RIG)
        self.parentRight.lblNoteUser.lower()
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
        self.parentRight.result["bg"] = newColor
        self.parentRight.score["bg"] = newColor
        self.parentRight.lblNote["bg"] = newColor
        self.parentRight.lblNote["fg"] = "white"
        self.parentRight.result["fg"] = "white"
        self.parentRight.score["fg"] = "white"

        self.parentRight.pickNote["bg"] = newColor
        self.parentRight.pickNote["fg"] = "white"

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
                self.lblUserShow = noteNameFull(self.startingNote) 
                self.parentRight.lblNote.config(text=self.lblUserShow)

            elif self.gameState == "waitingUserAnswer":
                if msg.note == self.startingNote:
                    # we want to ignore the starting note for the user.
                    return
                self.checkAnswer(msg.note)  # we check the answer
