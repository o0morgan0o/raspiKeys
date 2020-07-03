import tkinter as tk
import time
import datetime
import json

from autoload import Autoload
from utils.canvasThread import MyThread
from utils.bpm import Bpm
from utils.midiToNotenames import noteName
from utils.customElements.buttons import *
from utils.customElements.labels import *

class RecordNotesGui:
    def __init__(self,root,parent,choosenBpm, bassNote, chordQuality, backtrack, backtrackDuration, nbOfLoops):
        self.root = root
        self.parent = parent
        self.audioInstance = Autoload().getInstanceAudio()
        self.backtrack = backtrack
        self.backtrackDuration = backtrackDuration
        self.nbOfLoops=nbOfLoops
        self.choosenBpm =choosenBpm
        self.chordQuality=chordQuality
        self.bassNote = bassNote
        self.window = tk.Toplevel(self.root)
        self.window.attributes('-fullscreen', True)
        self.window.geometry("320x480")
        self.window["bg"]="black"
        print("backtrack gui:", self.backtrack)

        self.window.lbl1 = MyLabel12(self.window, text="Please record now...", wraplength=280)
        self.stringNotes=""
        self.window.lbl2=MyLabel40(self.window,text="{} {}".format(noteName(self.bassNote), self.chordQuality))
        self.window.lbl3 = MyLabel24(self.window, text="Notes : " + self.stringNotes, wraplength=280)
        self.window.lblRec = MyLabel18(self.window, text="")

        # Buttons
        self.window.btnCancel = BtnBlack12(self.window, text="Cancel", command=self.cancel)
        self.window.btnRetry = BtnBlack12(self.window,text="Retry", command= self.retry)
        self.window.btnSave = BtnBlack12(self.window, text="Save", command=lambda: self.saveMidi())

        self.window.canvas = tk.Canvas(self.window)


        self.parent.precountTimer = Bpm(self.choosenBpm, self.backtrack, self.backtrackDuration,self.nbOfLoops, lambda: self.activateRecordingNotes())


        self.window.lbl1.place(x=0,y=40,width=320, height=80)
        self.window.lbl2.place(x=0,y=120,width=320, height=60)
        self.window.lbl3.place(x=0, y=180, width=320, height=60)
        self.window.lblRec.place(x=20,y=250, width=280, height=40)
        self.window.btnCancel.place(x=20,y=310, width=100, height=130)
        self.window.btnRetry.place(x=120,y=310,width=80,height=130)
        self.window.btnSave.place(x=200,y=310,width=100,height=130)

        self.window.canvas.place(x=20, y=290,width=280, height=30)


    def cancel(self):
        self.parent.cancelThreads()
        self.window.destroy()
        self.parent.reloadMidiFiles()

    def retry(self):
        self.parent.cancelThreads()
        self.parent.startingTime=0
        self.parent.recordedNotes=[]
        self.parent.stringNotes =""
        self.window.lbl3.config(text="Notes : ")
        self.parent.precountTimer = Bpm(self.choosenBpm, self.backtrack, self.backtrackDuration,self.nbOfLoops, lambda: self.activateRecordingNotes())
        self.window.lblRec.config(background="black", text="")

    def saveMidi(self):
        self.parent.createJson(self.bassNote, self.chordQuality, self.backtrack, self.backtrackDuration,self.nbOfLoops)
        self.window.destroy()

    def activateRecordingNotes(self):
        self.parent.startingTime = int(round(time.time()*1000))
        self.parent.playChord(self.bassNote, self.chordQuality) # in order to play the chord when the user record
        self.window.lblRec.config(background="red", foreground="white", text="REC.")
        self.thread = MyThread(0,"thread-canvas", self.window.canvas, self.audioInstance,self.backtrackDuration * self.nbOfLoops, self)
        self.thread.start()
        self.parent.recordingNotes = True


    def endRecording(self):
        self.parent.recordingNotes=False
        self.window.lblRec.config(background="black", foreground="white", text="Finished!")
        self.window.canvas.delete("all")

    def destroy(self):
        self.window.destroy()
