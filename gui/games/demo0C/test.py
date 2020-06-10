import mido
import time
import threading
from threading import Timer

class Game:

    def __init__(self, parent):
        self.parent = parent

        self.stopGame = False
        print( "launchin program... \n")
        self.waitingNotes= []

        debug=True
        self.initMIDIArray(128)

        # define input and ouput USB midi
        self.inport= mido.open_input('USB-MIDI:USB-MIDI MIDI 1 24:0')
        self.inport.callback = self.handleMIDIInput
        self.outport= mido.open_output('USB-MIDI:USB-MIDI MIDI 1 24:0')
        self.showIOPorts()

        #just to test
        self.counter=0

        # start the main loop
        self.startGame()


    def showIOPorts(self):
        print(80*"=")
        # ['Midi Through:Midi Through Port-0 14:0', 'USB-MIDI:USB-MIDI MIDI 1 24:0']
        print( "Availables inputs: ", mido.get_input_names())
        print( "Availables outputs: ", mido.get_output_names())
        print("<== Selected input is {}".format(self.inport))
        print("==> Selected output is {}".format(self.outport))
        print(80*"=")


    # create and start the main thread
    def startGame(self):
        print("game thread starting")
        self.t1= threading.Thread(target=self.gameLoop)
        self.t1.start()

    def destroy(self):
        print("destroying thread !!!!")
        self.stopGame=True

    # Empty gameLoop just for listening the callbacks of midiIn and midiOut
    def gameLoop(self):
        while(self.stopGame == False):
            # The update of the UI is here
            self.counter = self.counter+1
            #may be there can be error handling here
            self.parent.button1["text"]=self.counter
            if(self.counter > 1500):
                self.parent.button1["bg"]="red"
            pass
        print("ended !!!")

    # init a 128 array of WaitingNote in order to store all the timers
    def initMIDIArray(self, maxNote):
        for i in range (maxNote):
            self.waitingNotes.append( self.WaitingNote(i, self))

    # callback launched when the timer is at 0
    def noteOff(self,note):
        print("[+] sending note off on ", note)
        msgOff = mido.Message('note_off', note=note)
        self.outport.send(msgOff)

    # prepare the future midi noteOff it is stored in waitingNotes list
    def prepareNoteOut(self, mNote):
        # creation of midi message
        msg = mido.Message( 'note_on', note = mNote)
        # send note on
        self.outport.send(msg)
        currentNote = self.waitingNotes[mNote]
        currentNote.resetTimer()
        

    def handleMIDIInput(self,msg):
        print("[-]receiving something", msg)
        if( msg.type == "note_on"):
            # just for test we send note if we receive keyboard signal
            self.prepareNoteOut(msg.note)


 
    # Inner class for storing in large liste all the timers corresponding to noteCCValue
    class WaitingNote:
        noteOffDelay = 1

        def __init__(self, note, parent):
            self.parent = parent
            self.note = note
            self.timer = Timer(self.noteOffDelay, lambda: self.parent.noteOff(self.note))


        # if we received at midi note we reset the timer so that the noteOff don't overlap
        def resetTimer(self):
            self.timer.cancel()
            self.timer = Timer(self.noteOffDelay, lambda: self.parent.noteOff(self.note))
            self.timer.start()

        # at the end of the timer the noteoff will be send
        def startTimer(self):
            self.timer.start()
        
