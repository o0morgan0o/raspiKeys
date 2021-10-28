import threading
from threading import Timer
from src.game.autoload import MidiIO


def playWinMelody(midi_instance : MidiIO, velocity:int, callback_before_melody=None, callback_after_melody=None):
    CustomNote(midi_instance, note=50, delay_on=.0, note_duration=.09, velocity=velocity, callback_before_note_on=callback_before_melody)
    CustomNote(midi_instance, note=53, delay_on=.1, note_duration=.09, velocity=velocity)
    CustomNote(midi_instance, note=58, delay_on=.2, note_duration=.09, velocity=velocity, callback_after_note_off=callback_after_melody)
    # CustomNote(midi_instance, 53, .1, .09, velocity)
    # CustomNote(midi_instance, 58, .2, .09, velocity)


def playLooseMelody(self):
    CustomNote(self.parent, 30, .0, .05)
    CustomNote(self.parent, 30, .1, .05)
    CustomNote(self.parent, 31, .2, .05)
    CustomNote(self.parent, 30, .3, .05)


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
    def __init__(self, midi_instance: MidiIO, note: int, delay_on: float, note_duration: float, velocity: int = 100,
                 callback_before_note_on = None,
                 callback_after_note_on = None,
                 callback_before_note_off=None,
                 callback_after_note_off = None):
        print("TRIGGER CUSTOM .................", callback_before_note_on, callback_after_note_on, callback_before_note_off, callback_after_note_off)
        self.midiIO = midi_instance
        self.delayBeforeOn = delay_on
        self.noteDuration = note_duration
        self.note = note
        self.timer = Timer(self.delayBeforeOn, lambda: self.prepareNoteOn(
            self.note, velocity, callback_before_note_on, callback_after_note_on, callback_before_note_off, callback_after_note_off))
        self.timer.start()

    def prepareNoteOn(self, note: int, velocity:int,callback_before_note_on,  callback_after_note_on, callback_before_note_off, callback_after_note_off):
        # print("prepare note in")
        if callback_before_note_on is not None:
            print("BEFORE NOTE ON")
            callback_before_note_on()
        self.midiIO.sendOut("note_on", note, velocity)
        if callback_after_note_on is not None:
            print("AFTER NOTE ON")
            callback_after_note_on()
        tout = Timer(self.noteDuration, lambda: self.prepareNoteOut(note,callback_before_note_off, callback_after_note_off))
        tout.start()

    def prepareNoteOut(self, note, callback_before_note_off, callback_after_note_off):
        if callback_before_note_off is not None:
            print("BEFORE NOTE OFF")
            callback_before_note_off()
        self.midiIO.sendOut("note_off", note)
        if callback_after_note_off is not None:
            print("AFTER NOTE OFF")
            callback_after_note_off()





class CustomSignal:
    def __init__(self, parent, noteType, note, velocity, delayOn):
        self.parent = parent
        try:
            if noteType == "note_on":
                self.timer = Timer(delayOn / 1000, lambda: self.parent.midiIO.sendOut("note_on", note, velocity))
                self.timer.start()
            elif noteType == "note_off":
                self.timer = Timer(delayOn / 1000, lambda: self.parent.midiIO.sendOut("note_off", note, velocity))
                self.timer.start()
            else:
                print("note type unknown", note.type)
        except RuntimeError as f:
            print(f'Failed at {len(threading.enumerate())} threads in')
            print(str(f))

    def cancel(self):
        self.timer.cancel()
