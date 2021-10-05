import tkinter as tk
from game.autoload import Autoload

from game.mode2.recordChordsGui import RecordChordsGui

from game.utils.midiToNotenames import noteName
from game.utils.utilFunctions import getChordInterval
from game.utils.utilFunctions import formatOutputInterval

from game.utils.customElements.buttons import *
from game.utils.customElements.labels import *


class RecordSetupGui:
    def __init__(self, globalRoot, backtrackFile, backtrackDuration, nbOfLoops, app):
        self.app = app
        self.globalRoot = globalRoot
        self.midiIO = Autoload().getInstance()
        self.midiIO.setCallback(self.handleMIDIInput)
        self.backtrackFile = backtrackFile
        self.backtrackDuration = backtrackDuration
        self.nbOfLoops = nbOfLoops
        self.isRecording = False

        print("backtrack : ", backtrackFile, backtrackDuration, nbOfLoops)

        self.window = tk.Toplevel(self.globalRoot)
        self.window.config(cursor="none")
        self.window.geometry("320x480")
        self.window.attributes("-fullscreen", True)
        self.window["bg"] = "black"
        # creation of 2 labels and 2 buttons
        self.window.lbl1 = MyLabel12(self.window, text="Insert Bass reference note and click on chord type.", wraplength=280)

        # show window the detected bass
        self.window.lbl2 = MyLabel18(self.window, text="?")
        self.window.lbl2.config(foreground="red")
        # lable which show the bass entered by the user
        self.window.lblBass = MyLabel18(self.window, text="?")
        self.window.lblBass.config(foreground="red")
        # buttons minor and major
        self.window.btnMinor = BtnBlack12(self.window, text="Minor")
        self.window.btnMinor.config(command=lambda: self.setChordQuality("minor"))
        self.window.btnMajor = BtnBlack12(self.window, text="Major")
        self.window.btnMajor.config(command=lambda: self.setChordQuality("major"))
        self.window.btndom7 = BtnBlack12(self.window, text="Dom7")
        self.window.btndom7.config(command=lambda: self.setChordQuality("dom7"))
        # slider
        self.window.bpmScale = tk.Scale(self.window, from_=40, to=140, resolution=1, orient=tk.HORIZONTAL, showvalue=0)
        self.window.bpmScale.config(command=self.updateBpmValue)
        self.window.bpmScale.config(background="black", foreground="white", sliderlength=80, width=90, bd=0)
        self.window.bpmScale.set(60)  # default value for bpm record
        # custom progression
        self.window.btnCustom = BtnBlack12(self.window, text="OK", wraplength=130)
        self.window.btnCustom.config(command=self.validateBeforeShowingWindow)
        # Button cancel
        self.window.btnCancel = BtnBlack12(self.window, text="Cancel")
        self.window.btnCancel.config(command=self.cancel)

        # ----Placement------
        yplacement = 10
        self.window.lbl1.place(x=0, y=yplacement, width=320, height=60)
        yplacement += 70
        self.window.lblBass.place(x=80, y=yplacement, width=60, height=60)
        self.window.lbl2.place(x=150, y=yplacement, width=100, height=60)

        yplacement += 80
        self.window.btnMinor.place(x=25, y=yplacement, width=90, height=60)
        self.window.btnMajor.place(x=115, y=yplacement, width=90, height=60)
        self.window.btndom7.place(x=205, y=yplacement, width=90, height=60)
        # self.window.bpmScale.place(x=40, y=260, width=240, height=90)

        yplacement += 100
        self.window.btnCustom.place(x=25, y=yplacement, width=270, height=60)
        yplacement += 70
        self.window.btnCancel.place(x=25, y=yplacement, width=270, height=60)

        self.bassNote = 0  # reinitilisation of the bassnote
        self.chordQuality = "-"
        # self.bassNote=60 # reinitilisation of the bassnote
        # self.chordQuality="major"

    def updateBpmValue(self, value):
        self.recordBpm = value

    def setChordQuality(self, quality):
        self.chordQuality = quality
        self.window.lbl1.config(text="Choosen Key :")
        self.window.lbl2.config(foreground="white", text=self.chordQuality, font=("Courier", 24, "bold"))

    def validateBeforeShowingWindow(self):
        print(self.bassNote, self.chordQuality)
        if self.bassNote == 0 or self.chordQuality == "-":  # check if user done the inputs
            self.window.lbl1.configure(foreground="red")
            self.window.lbl1.configure(text="Error, you need a valid bass note and valid chord quality!")

        else:
            # self.parent.recordingBassLick=False # desactivate the listen of user Bass
            self.window.destroy()
            # TODO use the same "temp window"  in global root for all (try delete it first)
            self.globalRoot.showRecordCustomChordWindow = RecordChordsGui(
                self.globalRoot, self.bassNote, self.chordQuality, self.backtrackFile, self.backtrackDuration, self.nbOfLoops, self.app
            )

    def handleMIDIInput(self, msg):
        if msg.type == "note_on":
            # print(msg.velocity)
            self.bassNote = msg.note
            # self.recordSetupWindow.bassNote= msg.note
            self.window.lblBass.config(text=noteName(self.bassNote), foreground="white", font=("Courier", 24, "bold"))
            # self.recordSetupWindow.window.lblBass.config(font=("Courier", 40, "bold"))
            # self.recordSetupWindow.window.lbl2.config(text=noteName(self.bassNote), foreground="white")
            # self.recordWindow.lbl2.config(text="Choosen Key : {} {}".format( noteName(self.bassNote), str(self.chordQuality)))
            # print(bassNote)

    def cancel(self):
        self.window.destroy()
        self.app.new_window(2)
