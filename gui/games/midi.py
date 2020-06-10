import mido
import time
from threading import Timer



class WaitingNote:
    noteOffDelay = 1

    def __init__(self, note):
        self.note = note
        self.timer = Timer(self.noteOffDelay, lambda: noteOff(self.note))

    def resetTimer(self):
        self.timer.cancel()
        self.timer = Timer(self.noteOffDelay, lambda: noteOff(self.note))
        self.timer.start()
        

    def startTimer(self):
        self.timer.start()
    
    

def initMIDIArray(maxNote):
    for i in range (maxNote):
        waitingNotes.append( WaitingNote(i))

def noteOff(note):
    print("[+] sending note off on ", note)
    msgOff = mido.Message('note_off', note=note)
    outport.send(msgOff)
    

def handleMIDIInput(msg):
    print("[-]receiving something", msg)
    if( msg.type == "note_on"):
        # just for test we send note if we receive keyboard signal
        sendNoteOut(msg.note)




def sendNoteOut(mNote):
    # creation of midi message
    msg = mido.Message( 'note_on', note = mNote)
    # send note on
    outport.send(msg)

    currentNote = waitingNotes[mNote]
    currentNote.resetTimer()

class Game:
    def __init__(self):

        print( "launchin program... \n")
        # ['Midi Through:Midi Through Port-0 14:0', 'USB-MIDI:USB-MIDI MIDI 1 24:0']
        print(80*"=")
        print( "Availables inputs: ", mido.get_input_names())
        print( "Availables outputs: ", mido.get_output_names())
        print(80*"=")
        self.waitingNotes= []
        



waitingNotes = []

debug=True

initMIDIArray(128)

# define input and ouput USB midi
inport= mido.open_input('USB-MIDI:USB-MIDI MIDI 1 24:0')
inport.callback = handleMIDIInput
outport= mido.open_output('USB-MIDI:USB-MIDI MIDI 1 24:0')
print("<== Selected input is {}".format(inport))
print("==> Selected output is {}".format(outport))

while True:
    pass







    


