import tkinter as tk
import threading

from autoload import Autoload
from utils.canvasThread import MyThread

from utils.midiToNotenames import noteName

from utils.bpm import Bpm
from utils.customElements.buttons import *
from utils.customElements.labels import *

from mode3.recordNotesGui import RecordNotesGui

class RecordChordsGui:
    def __init__(self, root, parent, choosenBpm, bassNote, chordQuality, backtrack, backtrackDuration, nbOfLoops):
        self.root = root
        self.audioInstance = Autoload().getInstanceAudio()
        self.backtrack=backtrack
        self.backtrackDuration = backtrackDuration
        self.nbOfLoops = nbOfLoops
        self.chordQuality = chordQuality
        self.bassNote = bassNote
        self.choosenBpm = choosenBpm
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
        self.customChordWindow.btnOK.config(command=self.nextWindow)

        self.customChordWindow.lblRec = MyLabel18(self.customChordWindow, text="")
        self.customChordWindow.lblRec.config(background="black")

        self.customChordWindow.canvas = tk.Canvas(self.customChordWindow)


        # placement
        self.customChordWindow.lblMessage.place(x=0, y=20, width=320, height=80)
        self.customChordWindow.lblBass.place(x=0, y=120, width=320, height=50)
        self.customChordWindow.lblRec.place(x=30,y=200, width=260,height=40)
        self.customChordWindow.canvas.place(x=30,y=240,width=260,height=30)
        self.customChordWindow.btnCancel.place(x=20, y=280, width=140, height=160)
        # self.customChordWindow.btnRetry.place(x=120, y=360, width=80, height=80)
        self.customChordWindow.btnOK.place(x=160, y=280, width=140, height=160)
        



        self.customChordWindow.lblBass.config(text="{} {}".format(noteName(self.bassNote), self.chordQuality))
        # we want to launch a thread, it will activate recording after count-in
        self.parent.precountTimer = Bpm(self.choosenBpm, self.backtrack, self.backtrackDuration, self.nbOfLoops,  lambda: self.activateRecordingChords())

    def nextWindow(self):
        # print(self.recordedCustomChords)
        self.customChordWindow.destroy()
        self.parent.showRecordNotesWindow(self.choosenBpm, self.bassNote, self.chordQuality, self.backtrack, self.backtrackDuration, self.nbOfLoops)

    def customChordRetry(self):
        self.startingTime=0
        self.recordedCustomChords=[]
    
    def customChordCancel(self):
        self.recordingCustomChords=False
        self.customChordWindow.destroy()

    def activateRecordingChords(self):
        # self.parent.startingTime=0 # in order to start at the first note
        self.customChordWindow.lblRec.config(text="REC.", background="red", foreground="white")
        self.thread = MyThread(0,"thread-canvas", self.customChordWindow.canvas, self.audioInstance ,self.backtrackDuration * self.nbOfLoops, self )
        self.thread.start()
        self.parent.recordingCustomChords=True

    def endRecording(self):
        self.parent.recordingCustomChords=False
        self.customChordWindow.lblRec.config(text="Finished!", background="black", foreground="white")
        self.customChordWindow.canvas.delete("all")

    
    def destroy(self):
        pass

    def cancel(self):
        self.customChordWindow.destroy()
        self.parent.cancelThreads()
        # self.parent.record
