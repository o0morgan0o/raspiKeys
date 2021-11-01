from threading import Timer


# Inner class for storing in large list all the timers corresponding to noteCCValue
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

    # at the end of the timer the note-off will be send
    def startTimer(self):
        self.timer.start()

# Inner class to play a noteOn with a delay. It is used for the note the user must guess
