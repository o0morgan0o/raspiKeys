import tkinter as tk

from utils.midiToNotenames import noteName

from utils.bpm import Bpm
from utils.customElements.buttons import BtnDefault
from utils.customElements.buttons import BtnSettings
from utils.customElements.labels import LblDefault
from utils.customElements.labels import LblSettings

from utils.customElements.labels import MyLabel8
from utils.customElements.labels import MyLabel12
from utils.customElements.labels import MyLabel18
from utils.customElements.labels import MyLabel24
from utils.customElements.labels import MyLabel30
from utils.customElements.labels import MyLabel40
from utils.customElements.buttons import BtnBlack12
from utils.customElements.buttons import BtnBlack20

from mode3.recordNotesGui import RecordNotesGui

class RecordChordsGui:
    def __init__(self, root, parent, choosenBpm, bassNote, chordQuality):
        self.chordQuality = chordQuality
        self.bassNote = bassNote
        self.choosenBpm = choosenBpm
        self.root = root
        self.parent= parent
        self.customChordWindow=tk.Toplevel(self.root)
        self.customChordWindow.attributes('-fullscreen', True)
        self.customChordWindow.geometry("320x480")
        self.customChordWindow["bg"]="black"
        self.customChordWindow.lblMessage = MyLabel12(self.customChordWindow, text="Record your progression,\nRecord start when you press a key...")
        self.customChordWindow.lblMessage.config(wraplength=280)
        self.customChordWindow.lblBass =MyLabel40(self.customChordWindow, text="Key")
        # self.customChordWindow.btnRetry=BtnBlack12(self.customChordWindow, text="Retry")
        self.customChordWindow.btnCancel=BtnBlack12(self.customChordWindow, text="Cancel")
        self.customChordWindow.btnCancel.config(command=self.cancel)
        self.customChordWindow.btnOK=BtnBlack12(self.customChordWindow, text="OK")
        self.customChordWindow.btnOK.config(command=self.customChordSave)

        self.customChordWindow.lblRec = MyLabel18(self.customChordWindow, text="")
        self.customChordWindow.lblRec.config(background="black")


        # placement
        self.customChordWindow.lblMessage.place(x=0, y=20, width=320, height=80)
        self.customChordWindow.lblRec.place(x=30,y=200, width=260,height=40)
        self.customChordWindow.lblBass.place(x=0, y=120, width=320, height=50)
        self.customChordWindow.btnCancel.place(x=20, y=280, width=140, height=160)
        # self.customChordWindow.btnRetry.place(x=120, y=360, width=80, height=80)
        self.customChordWindow.btnOK.place(x=160, y=280, width=140, height=160)



        self.customChordWindow.lblBass.config(text="{} {}".format(noteName(self.bassNote), self.chordQuality))
        # we want to launch a thread, it will activate recording after count-in
        self.parent.precountTimer = Bpm(self.choosenBpm, lambda: self.activateRecordingChords())

    def customChordSave(self):
        # print(self.recordedCustomChords)
        self.recordingCustomChords=False
        self.customChordWindow.destroy()
        self.showRecordWindow()

    def customChordRetry(self):
        self.startingTime=0
        self.recordedCustomChords=[]
    
    def customChordCancel(self):
        self.recordingCustomChords=False
        self.customChordWindow.destroy()

    def activateRecordingChords(self):
        # self.parent.startingTime=0 # in order to start at the first note
        self.customChordWindow.lblRec.config(text="REC.", background="red", foreground="white")
        self.parent.recordingCustomChords=True

    def showRecordWindow(self):
        self.parent.recordingCustomChords=False
        self.parent.recordNotes = RecordNotesGui(self.root, self.parent, self.choosenBpm, self.bassNote, self.chordQuality)
    
    def destroy(self):
        pass

    def cancel(self):
        self.customChordWindow.destroy()
        self.parent.cancelThreads()
        # self.parent.record