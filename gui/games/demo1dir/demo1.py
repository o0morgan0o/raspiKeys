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
from games.utils.sounds import Sound
from games.utils.midiChords import MidiChords

""" the mode 1 is for eartraining on a CHORD INTERVAL
"""
class Game:

    def __init__(self, parent):
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

        self.sounds = Sound() 
        self.sounds.loadEffectSounds() # load success and error sounds

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
            print( "waiting user input", self.score)
            self.parent.label1["text"] = "Pick a starting Note"
            self.gameState = "waitingUserInput"
            percentage = int((self.score / self.counter) * 100) if(self.counter != 0) else 0
            self.parent.label3["text"] = "{}/{} ({}%)".format(self.score, self.counter, percentage)
        elif newstate == "listen":
            print("LISTENNNNNN")
            self.parent.label2["bg"]= "black"
            self.parent.label1["text"] = "Listen ..."
            self.parent.label2["text"] = ""
            self.gameState = "listen"
            self.isListening = False
        elif newstate == "waitingUserAnswer":
            self.isListening= True
            self.parent.label1["text"] = "Your turn !"
            self.gameState= "waitingUserAnswer"
        else : 
            print( "ERROR : new state not defined", newstate)
        

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
            if self.canvasCounter == len(self.questionChord)-1:
                print("changing state...") 
                self.changeGameState("waitingUserAnswer")

        print("preparing")
        self.midiIO.sendOut("note_on", mNote) # send note on
        currentNote = self.waitingNotes[mNote]
        currentNote.resetTimer(offset)
        # draw on the canvas little rectangle to symbolyze the node
        rw= 2 * self.calcRectWidthOnCanvas() # rw est 2 largeur de rectgangle
        self.parent.canvas.create_rectangle(  rw+ self.canvasCounter*rw , 40 , rw+  self.canvasCounter*rw + rw/2 , 80, fill="white") 
        self.canvasCounter = self.canvasCounter + 1


    def handleMIDIInput(self,msg):
        # Needed because we still receive signals even if the class is destroyed
        if(self.isListening == False):
            print("[--] Ignoring queue message...", msg, self.isListening)
            return
        
        print("[-]receiving something", msg, self.isListening)
        if( msg.type == "note_on"):
            #we test according to the gamestate

            if self.gameState == "waitingUserInput":
                self.isListening = False # we will reactivate listening after all notes have been played
                self.startingNote = msg.note
                #pick a random chord intervals
                self.questionArray = self.pickNewChord(self.startingNote)
                # we want a array of QuestionNots
                arr = []
                counter = 1
                for note in self.questionArray:
                    # TODO : make a way to custom the harmonic delay between notes
                    arr.append(QuestionNote(note,self, .8* counter))
                    counter = counter + 1 
                self.allIsCorrect = True # var to know if we make a mistake in the answrs
                self.isFirstTry = True
                self.counter = self.counter + 1
                self.questionChord = arr
                print("size of question: " ,  len(self.questionChord))
                self.answerChord =[] # we initialize an answer chord
                self.answerBools = []
                # we initialize some vars and clear the canvas
                self.parent.canvas.delete("all")
                self.answerIndex=0
                self.canvasCounter=0


            elif self.gameState == "waitingUserAnswer":
                print("answer: ", self.answerIndex, self.canvasCounter)
                # we muste check all the notes of the chord.
                # we trace the current note with self.answerIndex
                correctNote = self.questionChord[self.answerIndex]
                print("correct note in array is ", correctNote.note, msg.note, self.answerIndex)
                self.checkAnswer(msg.note, correctNote) # we check the answer
                self.answerIndex = self.answerIndex + 1

    def checkAnswer(self, userAnswer, correctAnswer):

        #print(answer, self.questionNote.note)
        rw= 2 * self.calcRectWidthOnCanvas() # rw est 2 largeur de rectgangle
        if userAnswer == correctAnswer.note: 
            # ok one answer is 
            self.answerBools.append(True)
            self.parent.canvas.create_rectangle(  rw+ self.answerIndex*rw , 0 , rw+  self.answerIndex*rw + rw/2 , 40, fill="green") 
        else:
            self.answerBools.append(False)
            self.allIsCorrect = False
            self.parent.canvas.create_rectangle(  rw+ self.answerIndex*rw , 0 , rw+  self.answerIndex*rw + rw/2 , 40, fill="red") 

        if self.answerIndex == len(self.questionChord) -1:
            
            self.isListening= False
            print("WE CAN RETURN")
            print("WIN ? ", self.allIsCorrect)
            if self.allIsCorrect == False:
                self.changeGameState( "listen")
                self.parent.label2["text"]= "incorrect"
                self.parent.label2["bg"] = "red"
                # TODO : must play sound victory

                for note in self.questionChord:
                    print("resetting a timer")
                    note.resetTimer()
                self.answerBools = []
                self.allIsCorrect= True
                self.parent.canvas.delete("all") 
                self.answerIndex=-1
                self.canvasCounter = 0
                self.isFirstTry= False




            else :
            # We won
                self.parent.label2["text"] = "correct ;-)\n{}".format(self.chordName)
                self.parent.label2["bg"] = "green"
                print("first try" , self.isFirstTry)
                if self.isFirstTry:
                    self.score = self.score + 1
                self.changeGameState("waitingUserInput")
                self.isListening= True
    #            self.sounds.play_sound_success() # play success sound
                
            # affichage score
            self.parent
            self.parent.canvas.delete("all") 



    def pickNewChord(self, startingNote):
        # TODO : pick random intervals
        chordsInit = MidiChords()
        chord = chordsInit.pickRandom()
        self.chordName = chord[0]
        #return [startingNote,  startingNote + 3,startingNote +  7,startingNote +  12]
        # we must add the starting note
        returnChord = []
        for note in chord[1]:
            returnChord.append(note + self.startingNote)
        return returnChord
    


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
        
    def calcRectWidthOnCanvas(self):
        canvasW = 200
        nbRects = len(self.questionChord)
        # calcul savant !
        w = 2*nbRects + 3
        return canvasW / w
        
 
