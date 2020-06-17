from threading import Timer
from games.utils.midiIO import MidiIO

class QuestionNote:

    def __init__(self, note, parent, delay):
        self.noteOnDelay = delay
        self.isFirstTry = True
        self.parent = parent
        self.note = note
        self.timer = Timer(self.noteOnDelay, lambda: self.parent.prepareNoteOut(self.note))
        self.timer.start()

    def resetTimer(self):
        self.timer = Timer(self.noteOnDelay, lambda: self.parent.prepareNoteOut(self.note))
        self.timer.start()


class CustomNote:
    def __init__(self,  parent, note, delayOn, noteDuration):
        print("TRIGGER CUSTOM .................")
        self.noteOnDelay = delayOn
        self.noteOffDelay= noteDuration
        self.parent = parent
        self.note = note
        self.timer = Timer(self.noteOnDelay, lambda: self.prepareNoteIn(self.note))

        self.timer.start()

    def prepareNoteIn(self, note):
        print("prepare note in")
        self.parent.midiIO.sendOut("note_on", self.note)
        tout = Timer(self.noteOffDelay, lambda: self.prepareNoteOut(self.note))
        tout.start()


    def prepareNoteOut(self, note):
        self.parent.midiIO.sendOut("note_off", self.note)
        print("send note off")


        
class Melody:
    def __init__(self, parent):
        self.parent = parent

    def playWinMelody(self):
        CustomNote(self.parent, 50, .0,.09)
        CustomNote(self.parent, 53, .1,.09)
        CustomNote(self.parent, 58, .2,.09)


    def playLooseMelody(self):
        CustomNote(self.parent, 30,.0,.05)
        CustomNote(self.parent, 30,.1,.05)
        CustomNote(self.parent, 31,.2,.05)
        CustomNote(self.parent, 30,.3,.05)


class CustomSignal:
    def __init__(self, parent,noteType, note,delayOn):
        self.parent =parent
        print("CUSTOM SIGNAL")
        if noteType == "note_on":
            self.timer= Timer(delayOn/1000,lambda: self.parent.midiIO.sendOut("note_on", note))
            self.timer.start()
        elif noteType == "note_off": 
            print("sending note off timer", delayOn/1000)
            self.timer= Timer(delayOn/1000,lambda: self.parent.midiIO.sendOut("note_off", note))
            self.timer.start()
        else: 

            print("note type unknown", note.type)

