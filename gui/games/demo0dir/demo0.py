import time
import threading
import random
from threading import Timer
import mido
import simpleaudio as sa


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

        # define input and ouput USB midi
        self.outport= mido.open_output('USB-MIDI:USB-MIDI MIDI 1 24:0')
        self.inport= mido.open_input('USB-MIDI:USB-MIDI MIDI 1 24:0')
        self.inport.callback = None
        self.inport.poll()

        #try to clear pending notes
        print("TRY TO CLEAR ==========")
        self.inport._queue._queue.mutex.acquire()
        self.inport._queue._queue.queue.clear()
        self.inport._queue._queue.all_tasks_done.notify_all()
        self.inport._queue._queue.unfinished_tasks=0
        self.inport._queue._queue.mutex.release()
        print("END ==========")

        #for msg in self.inport.iter_pending():
        #    print("pending : ", msg)
        self.showIOPorts()
        self.outport.panic()
        self.outport.reset()
        self.inport.callback = self.handleMIDIInput

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

    def showIOPorts(self):
        print(80*"=")
        # ['Midi Through:Midi Through Port-0 14:0', 'USB-MIDI:USB-MIDI MIDI 1 24:0']
        print( "Availables inputs: ", mido.get_input_names())
        print( "Availables outputs: ", mido.get_output_names())
        print("<== Selected input is {}".format(self.inport))
        print("==> Selected output is {}".format(self.outport))
        print(80*"=")

    def __del__(self):
        print( "destroy")

    def destroy(self):
        print("destroy in class")
        # send midi panic to be sure that there is no note off
        self.isListening = False
        self.inport.callback = None
        self.outport.panic()
        # close ports
        self.outport.close()
        self.inport.close()
        # print("is closed output? : ",self.outport.closed)
        # print("is closed input? : ",self.inport.closed)
        del self.inport
        del self.outport
        # delete WantingNotes
        del self.waitingNotes
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
            self.waitingNotes.append( self.WaitingNote(i, self))

    # callback launched when the timer is at 0
    def noteOff(self,note):
        if self.isListening == False:
            return

        print("[+] sending note off on ", note)
        msgOff = mido.Message('note_off', note=note)
        self.outport.send(msgOff)

    # prepare the future midi noteOff it is stored in waitingNotes list
    def prepareNoteOut(self, mNote, offset=0):
        if self.gameState == "waitingUserInput":
            self.changeGameState("listen")
        elif self.gameState == "listen":
            self.changeGameState("waitingUserAnswer")
        print("preparing")
        # creation of midi message
        msg = mido.Message( 'note_on', note = mNote)
        # send note on
        self.outport.send(msg)
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
                self.questionNote = self.QuestionNote(questionNote, self, .8)
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
            self.parent.label2[ "text"] = "correct ;-)\n{}".format(self.formatOutputInterval(self.questionNote.note - self.startingNote))
            self.parent.label2["bg"] = "green"
            if self.questionNote.isFirstTry:
                self.score = self.score + 1
            # TODO: make a try excerpt because may be the sound could not be loaded
            sound_object = self.success_sound.play()
            sound_object.wait_done()
            self.changeGameState("waitingUserInput") # if we gave the good answer, we want a new note
        else:
            self.parent.label2["text"]= "incorrect\nA: {}".format(self.formatOutputInterval(self.questionNote.note - self.startingNote))
            self.questionNote.isFirstTry= False
            self.parent.label2["bg"] = "red"
            sound_object = self.error_sound.play()
            sound_object.wait_done()
            # TODO if we don't find we must replay the note
            self.replayNote = self.QuestionNote(self.startingNote, self, .2) # i want to replay both notes
            self.replayNote = self.QuestionNote(self.questionNote.note, self, .8) # i want to replay both notes
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
        

        
    def formatOutputInterval(self, mInterval):
        #TODO: Extend to other responses
        interval = abs(mInterval)
        if interval == 1: return "min 2nd"
        elif interval == 2: return "maj 2nd"
        elif interval == 3 : return "min 3rd"
        elif interval == 4: return "maj 3rd"
        elif interval == 5: return "perf 4th"
        elif interval == 6 : return "dim 5th"
        elif interval == 7 : return "perf 5th"
        elif interval ==8 : return "min 6th"
        elif interval ==9: return "maj 6th"
        elif interval ==10: return "min 7th"
        elif interval == 11 : return "maj 7th"
        elif interval == 12: return "octave"
        elif interval == 13: return "min 9th"
        elif interval == 14: return "maj 9th"
        elif interval == 15: return "min 10th"
        elif interval == 16: return "maj 10th"
        elif interval == 17: return "perf 11th"
        else: return ""
 
    # Inner class for storing in large liste all the timers corresponding to noteCCValue
    class WaitingNote:
        noteOffDelay = 1

        def __init__(self, note, parent):
            self.parent = parent
            self.note = note
            self.timer = Timer(self.noteOffDelay, lambda: self.parent.noteOff(self.note))


        # if we received at midi note we reset the timer so that the noteOff don't overlap
        def resetTimer(self, offset):
            self.timer.cancel()
            self.timer = Timer(self.noteOffDelay, lambda: self.parent.noteOff(self.note))
            self.timer.start()

        # at the end of the timer the noteoff will be send
        def startTimer(self):
            self.timer.start()
        
    # Inner class to play a noteOn with a delay. It is used for the note the user must guess
    class QuestionNote:

        def __init__(self, note, parent, delay):
            self.noteOnDelay = delay
            self.isFirstTry = True
            self.parent = parent
            self.note = note
            self.timer = Timer(self.noteOnDelay, lambda: self.parent.prepareNoteOut(self.note))
            self.timer.start()

