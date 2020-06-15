from threading import Timer

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

