import time
import threading
import random
from threading import Timer
import mido
import simpleaudio as sa

from src.game.utils.waitingNote import WaitingNote
from src.game.utils.questionNote import QuestionNote
from src.game.utils.midiIO import MidiIO
from src.game.utils.utilFunctions import formatOutputInterval
from src.game.utils.midiChords import MidiChords
from src.game.utils.questionNote import CustomNote
from src.game.utils.questionNote import Melody
from src.game.utils.questionNote import CustomSignal

from src.game.autoload import Autoload

from src.game.utils.midiToNotenames import noteNameFull
from src.game.utils.midiToNotenames import noteName

""" the mode 1 is for eartraining on a CHORD INTERVAL
"""


class Game:
    def __init__(self, parent, config):
        self.questionArray = []
        self.config = config
        self.delay = float(self.config["question_delay"]) / 100
        self.parent = parent
        self.isListening = False

        # variable for user score
        self.counter = 0
        self.score = 0
        self.globalIsListening = True

        debug = True
        self.stopGame = False
        self.waitingNotes = []

        self.midiIO = Autoload.get_instance().getMidiInstance()  # open connections and ports
        self.midiIO.setCallback(self.handleMIDIInput)

        # gamestate is used to know when the user is guessing
        self.gameState = "notStarted"

        # startGame
        self.startGame()
        self.startingNote = -1

        self.parent.btnSkip.configure(command=self.skip)

        self.melodies = Melody(self)

    def toggleGlobalListen(self):
        if self.globalIsListening == True:
            self.globalIsListening = False
            self.parent.btnListen.configure(text="ListenOFF")
        else:
            self.globalIsListening = True
            self.parent.btnListen.configure(text="ListenON")

    def skip(self):
        try:
            notesAnswer = ""
            for note in self.questionArray:
                notesAnswer += noteName(note) + "-"
            self.parent.lblNote.config(font=("Courier", 18, "bold"))
            self.parent.lblNote["text"] = "It was\n{}".format(notesAnswer)
            # .format(formatOutputInterval(self.questionNote.note - self.startingNote))
            self.parent.lblNote["bg"] = "orange"
            self.changeGameState("waitingUserInput")  # if we gave the good answer, we want a new note
        except Exception as e:
            print("Impossible to skip question", e)

    def startGame(self):
        self.changeGameState("waitingUserInput")
        self.parent["bg"] = "black"
        self.changeAllBg("black")

    def destroy(self):
        self.isListening = False
        self.midiIO.destroy()  # delete everything in midiIO class
        del self.waitingNotes  # delete WantingNotes
        del self

    def changeGameState(self, newstate):
        if newstate == "notStarted":
            pass
        elif newstate == "waitingUserInput":
            self.parent.label1["text"] = "Pick a starting Note"
            self.gameState = "waitingUserInput"
            percentage = int((self.score / self.counter) * 100) if (self.counter != 0) else 0
            self.parent.label3["text"] = "{}/{} ({}%)".format(self.score, self.counter, percentage)
        elif newstate == "listen":
            self.parent.label2["bg"] = "black"
            self.parent.label1["text"] = "Listen ..."
            self.parent.label2["text"] = ""
            self.gameState = "listen"
            self.isListening = False
        elif newstate == "waitingUserAnswer":
            self.isListening = True
            self.parent.label1["text"] = "Your turn !"
            self.gameState = "waitingUserAnswer"
        else:
            print("ERROR : new state not defined", newstate)

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
            if self.canvasCounter == len(self.questionChord) - 1:
                print("changing state...")
                self.changeGameState("waitingUserAnswer")

        self.midiIO.sendOut("note_on", mNote)  # send note on
        currentNote = self.waitingNotes[mNote]
        currentNote.resetTimer(offset)
        # draw on the canvas little rectangle to symbolyze the node
        rw = 2 * self.calcRectWidthOnCanvas()  # rw est 2 largeur de rectgangle
        self.parent.canvas.create_rectangle(rw + self.canvasCounter * rw, 40, rw + self.canvasCounter * rw + rw / 2, 80, fill="white")
        self.canvasCounter = self.canvasCounter + 1

    def drawAndPlayAnswer(self):
        self.parent.canvas.delete("all")
        self.timers = []
        counter = 0

        for note in self.questionArray:
            print(note + self.startingNote)
            # self.timers.append(Timer(1, lambda: self.midiIO.sendOut("note_on", self.startingNote+note, 100)))
            isLast = False
            if counter == len(self.questionArray) - 1:
                isLast = True
            # minimum delay ?
            self.timers.append(Timer(1 + counter * self.delay, self.sendOut, ["note_on", self.startingNote + note, 100, isLast],).start())
            self.timers.append(Timer(3 + counter * self.delay, self.sendOut, ["note_off", self.startingNote + note, 100]).start())
            counter += 1

    def sendOut(self, mType, note, velocity, isLast=False):
        if mType == "note_on":
            self.midiIO.sendOut("note_on", note)
            rw = 2 * self.calcRectWidthOnCanvas()  # rw est 2 largeur de rectgangle
            self.parent.canvas.create_rectangle(rw + self.canvasCounter * rw, 40, rw + self.canvasCounter * rw + rw / 2, 80, fill="white")
            self.canvasCounter = self.canvasCounter + 1
            if isLast == True:
                self.changeGameState("waitingUserAnswer")
        elif mType == "note_off":
            self.midiIO.sendOut("note_off", note)

    def resetQuestion(self):
        self.parent.canvas.delete("all")
        self.changeGameState("listen")
        self.parent.label2["text"] = "incorrect"
        self.parent.label2["bg"] = "red"
        self.drawAndPlayAnswer()
        self.answerBools = []
        self.allIsCorrect = True
        self.parent.canvas.delete("all")
        self.answerIndex = -1
        self.canvasCounter = 0
        self.isFirstTry = False
        self.midiIO.panic()  # TODO : there is still a bug with first note ringing
        # affichage score
        self.parent.canvas.delete("all")

    def checkAnswer(self, userAnswer, correctAnswer):

        # print(answer, self.questionNote.note)
        rw = 2 * self.calcRectWidthOnCanvas()  # rw est 2 largeur de rectgangle
        if userAnswer == correctAnswer:

            # ok one answer is
            self.answerBools.append(True)
            self.parent.canvas.create_rectangle(rw + self.answerIndex * rw, 0, rw + self.answerIndex * rw + rw / 2, 40, fill="green")
        else:
            # we made a mistake on one note
            time.sleep(0.2)
            self.parent.label2["text"] = "incorrect"
            self.parent.label2["bg"] = "red"
            time.sleep(0.4)

            self.answerBools.append(False)
            self.allIsCorrect = False
            self.parent.canvas.create_rectangle(rw + self.answerIndex * rw, 0, rw + self.answerIndex * rw + rw / 2, 40, fill="red")
            self.resetQuestion()

        if self.answerIndex == len(self.questionArray) - 1:

            self.isListening = False
            if self.allIsCorrect == False:
                pass
            #                self.changeGameState( "listen")
            #
            #
            #                for note in self.questionChord:
            #                    print("resetting a timer")
            #                    note.resetTimer()
            #                self.answerBools = []
            #                self.allIsCorrect= True
            #                self.parent.canvas.delete("all")
            #                self.answerIndex=-1
            #                self.canvasCounter = 0
            #                self.isFirstTry= False
            #
            else:
                # We won
                self.parent.lblNote.config(font=("Courier", 18, "bold"))
                self.parent.lblNote["text"] = "correct ;-)\n{}".format(self.chordName)
                self.parent.lblNote["bg"] = "green"
                if self.isFirstTry:
                    self.score = self.score + 1
                self.changeGameState("waitingUserInput")

                time.sleep(1)
                self.melodies.playWinMelody()
                time.sleep(1)
                self.isListening = True

            self.midiIO.panic()  # TODO : there is still a bug with first note ringing
            self.parent
            self.parent.canvas.delete("all")

    def pickNewChord(self, startingNote):
        # TODO : pick random intervals
        chordsInit = MidiChords()
        chord = chordsInit.pickRandom()
        self.chordName = chord[0]
        self.chordNotes = chord[1]
        return chord

    def changeAllBg(self, newColor):
        self.parent.label1["bg"] = newColor
        self.parent.label2["bg"] = newColor
        self.parent.label3["bg"] = newColor
        self.parent.label1["fg"] = "white"
        self.parent.label2["fg"] = "white"
        self.parent.label3["fg"] = "white"

    def calcRectWidthOnCanvas(self):
        canvasW = 200
        nbRects = len(self.questionArray)
        # calcul savant !
        w = 2 * nbRects + 3
        return canvasW / w

    def handleMIDIInput(self, msg):
        if Autoload.get_instance().getMidiInstance().isListening == False:
            return
        if self.globalIsListening == False:
            return
        # Needed because we still receive signals even if the class is destroyed
        if self.isListening == False:
            print("[--] Ignoring queue message...", msg, self.isListening)
            return

        print("[-]receiving something", msg, self.isListening)
        if msg.type == "note_on" and msg.velocity> 10:
            # we test according to the gamestate

            if self.gameState == "waitingUserInput":
                self.isListening = False  # we will reactivate listening after all notes have been played
                self.startingNote = msg.note
                self.parent.lblNote["bg"] = "black"
                self.parent.lblNote.config(font=("Courier", 30, "bold"))
                self.parent.lblNote["text"] = noteNameFull(self.startingNote)
                # pick a random chord intervals
                self.question = self.pickNewChord(self.startingNote)
                self.questionArray = self.question[1]

                self.drawAndPlayAnswer()

                self.allIsCorrect = True  # var to know if we make a mistake in the answrs
                self.isFirstTry = True
                self.counter = self.counter + 1
                self.answerChord = []  # we initialize an answer chord
                self.answerBools = []
                # we initialize some vars and clear the canvas
                self.answerIndex = 0
                self.canvasCounter = 0

            elif self.gameState == "waitingUserAnswer":
                correctNote = self.questionArray[self.answerIndex] + self.startingNote
                self.checkAnswer(msg.note, correctNote)
                self.answerIndex = self.answerIndex + 1
                # we muste check all the notes of the chord.
                # we trace the current note with self.answerIndex
