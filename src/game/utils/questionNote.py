from threading import Timer

from src.game.autoload import MidiIO

NOTE_ON = "note_on"
NOTE_OFF = "note_off"


def playWinMelody(midi_instance: MidiIO, velocity: int, callback_before_melody=None, callback_after_melody=None):
    CustomNote(midi_instance, note=50, delay_on=.0, note_duration=.09, velocity=velocity, callback_before_note_on=callback_before_melody)
    CustomNote(midi_instance, note=53, delay_on=.1, note_duration=.09, velocity=velocity)
    CustomNote(midi_instance, note=58, delay_on=.2, note_duration=.09, velocity=velocity, callback_after_note_off=callback_after_melody)


def playLooseMelody(self):
    CustomNote(self.view, 30, .0, .05)
    CustomNote(self.view, 30, .1, .05)
    CustomNote(self.view, 31, .2, .05)
    CustomNote(self.view, 30, .3, .05)


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
    def __init__(self,
                 midi_instance: MidiIO,
                 note: int,
                 delay_on: float,
                 note_type=None,
                 note_duration: float = None,
                 velocity: int = 100,
                 callback_before_note_on=None,
                 callback_after_note_on=None,
                 callback_before_note_off=None,
                 callback_after_note_off=None):
        # because we don't want to have note_duration and note_type at the same time, if we have both or none, we raise an exception
        if note_duration is not None and note_type is not None:
            raise Exception("CustomNote can't have note_duration and note_type at the same time")
        if note_duration is None and note_type is None:
            raise Exception("CustomNote must have at least note_duration or note_type")
        print("TRIGGER CUSTOM .................", callback_before_note_on, callback_after_note_on, callback_before_note_off, callback_after_note_off)
        self.midiIO = midi_instance
        self.delayBeforeOn = delay_on
        self.noteDuration = note_duration
        self.note = note
        self.timer = None
        if note_type is None:
            self.timer = Timer(
                self.delayBeforeOn,
                lambda: self.prepareNoteOn(self.note, velocity,
                                           callback_before_note_on=callback_before_note_on,
                                           callback_after_note_on=callback_after_note_on,
                                           callback_before_note_off=callback_before_note_off,
                                           callback_after_note_off=callback_after_note_off)
            )
        # these 2 next conditionals are only for practise licks mode, because notes are explicitly note_on or note_off
        elif note_type == NOTE_ON:
            self.timer = Timer(
                self.delayBeforeOn,
                lambda: self.prepareNoteOn(self.note, velocity, callback_before_note_on=callback_before_note_on, callback_after_note_on=callback_after_note_on)
            )
        elif note_type == NOTE_OFF:
            self.timer = Timer(
                self.delayBeforeOn,
                lambda: self.prepareNoteOut(note, callback_before_note_off=callback_before_note_off, callback_after_note_off=callback_after_note_off)
            )
        self.timer.start()

    def prepareNoteOn(self, note: int, velocity: int, callback_before_note_on=None, callback_after_note_on=None, callback_before_note_off=None, callback_after_note_off=None):
        if callback_before_note_on is not None:
            print("BEFORE NOTE ON")
            callback_before_note_on()
        self.midiIO.sendOut("note_on", note, velocity)
        if callback_after_note_on is not None:
            print("AFTER NOTE ON")
            callback_after_note_on()
        if self.noteDuration is not None:
            tout = Timer(
                self.noteDuration,
                lambda: self.prepareNoteOut(note, callback_before_note_off, callback_after_note_off)
            )
            tout.start()

    def prepareNoteOut(self, note, callback_before_note_off=None, callback_after_note_off=None):
        if callback_before_note_off is not None:
            print("BEFORE NOTE OFF")
            callback_before_note_off()
        self.midiIO.sendOut("note_off", note)
        if callback_after_note_off is not None:
            print("AFTER NOTE OFF")
            callback_after_note_off()
