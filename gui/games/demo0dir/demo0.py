import time
import threading
import random
from threading import Timer
import mido
import simpleaudio as sa

from games.utils.waitingNote import WaitingNote
from games.utils.questionNote import QuestionNote
from games.utils.midiIO import MidiIO
from games.utils.utilFunctions import formatOutputInterval

class Game:

    def __init__(self, parent):
        self.loadSounds()
        self.parent = parent
        self.isListening = False

        # variable for user score
        self.counter=0
        self.score=0

        print( "launchin MIDI program... \n")
        debug=True
        self.stopGame = False
        self.waitingNotes= []
        self.initMIDIArray(128)

        # TODO : in this MidiIo class, allow user to select between available usb ports
        self.midiIO = MidiIO() # open connections and ports
        self.midiIO.setCallback(self.handleMIDIInput)

        # gamestate is used to know when the user is guessing
        self.gameState = "notStarted"

        # startGame
        self.startGame()
        self.startingNote = -1

    def loadSounds(self):
        # success sound
        success_sound = "/home/pi/raspiKeys/gui/games/demo0dir/wav/success.wav"
        self.success_sound = sa.WaveObject.from_wave_file(success_sound)
        # error sound
        error_sound = "/home/pi/raspiKeys/gui/games/demo0dir/wav/error.wav"
        self.error_sound= sa.WaveObject.from_wave_file(error_sound)
        #play_obj_success = wave_obj_success.play()
        #play_obj_success.wait_done()

    def startGame(self):
        self.changeGameState("waitingUserInput")
        self.parent["bg"] = "black"
        self.changeAllBg("black")

    def destroy(self):
        print("destroy in class")
        self.isListening = False
        self.midiIO.destroy() # delete everything in midiIO class
        del self.waitingNotes # delete WantingNotes
        del self

    def changeGameState(self, newstate):
        if newstate == "notStarted":
            pass
        elif newstate == "waitingUserInput":
            self.parent.label1["text"] = "Pick a starting Note"
            self.gameState = "waitingUserInput"
            percentage = int((self.score / self.counter) * 100) if(self.counter != 0) else 0
            self.parent.label3["text"] = "{}/{} ({}%)".format(self.score, self.counter, percentage)
        elif newstate == "listen":
            #self.parent["bg"] = "orange"
            #self.changeAllBg("orange")
            self.parent.label2["bg"]= "black"
            self.parent.label1["text"] = "Listen ..."
            self.parent.label2["text"] = ""
            self.gameState = "listen"
            self.isListening = False
        elif newstate == "waitingUserAnswer":
            self.isListening= True
            #self.parent["bg"] = "blue"
            #self.changeAllBg("blue")
            self.parent.label1["text"] = "What is your answer ?"
            self.gameState= "waitingUserAnswer"
        

    # init a 128 array of WaitingNote in order to store all the timers
    def initMIDIArray(self, maxNote):
        for i in range (maxNote):
            self.waitingNotes.append(WaitingNote(i, self))

    # callback launched when the timer is at 0
    def noteOff(self,note):
        if self.isListening == False:
            return
        self.midiIO.sendOut("note_off", note)
        

    # prepare the future midi noteOff it is stored in waitingNotes list
    def prepareNoteOut(self, mNote, offset=0):
        if self.gameState == "waitingUserInput":
            self.changeGameState("listen")
        elif self.gameState == "listen":
            self.changeGameState("waitingUserAnswer")
        print("preparing")
        self.midiIO.sendOut("note_on", mNote) # send note on
        currentNote = self.waitingNotes[mNote]
        currentNote.resetTimer(offset)

    def handleMIDIInput(self,msg):
        # Needed because we still receive signals even if the class is destroyed
        if(self.isListening == False):
            print("[--] Ignoring queue message...", msg, self.isListening)
            return
        
        print("[-]receiving something", msg, self.isListening)
        if( msg.type == "note_on"):
            #we test according to the gamestate

            if self.gameState == "waitingUserInput":
                self.startingNote = msg.note
                #pick a random note
                questionNote = self.pickNewNote(self.startingNote)
                self.questionNote = QuestionNote(questionNote, self, .8)
                self.changeGameState("listen")

            elif self.gameState == "waitingUserAnswer":
                # we want to ignore the starting note for the user.
                if msg.note == self.startingNote:
                    return
                # we check the answer
                self.checkAnswer(msg.note)

    def checkAnswer(self, answer):
        print(answer, self.questionNote.note)
        if answer == self.questionNote.note:
            self.parent.label2[ "text"] = "correct ;-)\n{}".format(formatOutputInterval(self.questionNote.note - self.startingNote))
            self.parent.label2["bg"] = "green"
            if self.questionNote.isFirstTry:
                self.score = self.score + 1
            # TODO: make a try excerpt because may be the sound could not be loaded
            sound_object = self.success_sound.play()
            sound_object.wait_done()
            self.changeGameState("waitingUserInput") # if we gave the good answer, we want a new note
        else:
            self.parent.label2["text"]= "incorrect\nA: {}".format(formatOutputInterval(self.questionNote.note - self.startingNote))
            self.questionNote.isFirstTry= False
            self.parent.label2["bg"] = "red"
            sound_object = self.error_sound.play()
            sound_object.wait_done()
            # TODO if we don't find we must replay the note
            self.replayNote = QuestionNote(self.startingNote, self, .2) # i want to replay both notes
            self.replayNote = QuestionNote(self.questionNote.note, self, .8) # i want to replay both notes
            self.changeGameState("listen")

    def pickNewNote(self, startingNote):
        self.counter = self.counter+1
        #TODO : make the max interval customizable
        maxInterval = 14
        offset = 0
        while offset == 0: # we dont want the same note than the starting note
            offset = random.randint(-maxInterval, maxInterval)
        return startingNote + offset

    def handleQuestionNote(self, mNote):
        self.prepareNoteOut

    def changeAllBg(self, newColor):
        self.parent.label1["bg"] = newColor
        self.parent.label2["bg"] = newColor
        self.parent.label3["bg"] = newColor
        self.parent.label1["fg"] = "white"
        self.parent.label2["fg"] = "white"
        self.parent.label3["fg"] = "white"
        

        
 
