import tkinter as tk
import threading
import time
import pygame

from game.autoload import Autoload
from game.utils.canvasThread import MyThread

from game.utils.midiToNotenames import noteName

from game.utils.bpm import Bpm
from game.utils.customElements.buttons import *
from game.utils.customElements.labels import *

from game.mode2.recordNotesGui import RecordNotesGui


class RecordChordsGui:
    def __init__(self, globalRoot, bassNote, chordQuality, backtrack, backtrackDuration, nbOfLoops, app):
        self.app = app
        self.globalRoot = globalRoot
        self.midiIO = Autoload().getInstance()
        self.midiIO.setCallback(self.handleMIDIInput)
        self.audioInstance = Autoload().getInstanceAudio()
        self.backtrack = backtrack
        self.backtrackDuration = backtrackDuration
        self.nbOfLoops = nbOfLoops
        self.chordQuality = chordQuality
        self.bassNote = bassNote
        self.choosenBpm = 90

        self.sound = Autoload().getInstanceAudio()
        self.window = tk.Toplevel(self.globalRoot, cursor="none")
        self.window.attributes("-fullscreen", True)
        self.window.geometry("320x480")
        self.window["bg"] = "black"
        self.window.lblMessage = MyLabel12(self.window, text="Wait for the preparation of the backtrack")
        self.window.lblMessage.config(wraplength=280)
        self.window.lblBass = MyLabel40(self.window, text="Key")
        # self.window.btnRetry=BtnBlack12(self.window, text="Retry")
        self.window.btnCancel = BtnBlack12(self.window, text="Cancel")
        self.window.btnCancel.config(command=self.cancel)
        self.window.btnOK = BtnBlack12(self.window, text="OK")
        self.window.btnOK.config(command=self.nextWindow, state="disabled")

        self.window.lblRec = MyLabel18(self.window, text="")
        self.window.lblRec.config(background="black")

        self.window.canvas = tk.Canvas(self.window)

        # placement
        self.window.lblMessage.place(x=0, y=20, width=320, height=80)
        self.window.lblBass.place(x=0, y=120, width=320, height=50)
        self.window.lblRec.place(x=30, y=200, width=260, height=40)
        self.window.canvas.place(x=30, y=240, width=260, height=30)
        self.window.btnCancel.place(x=20, y=280, width=140, height=160)
        # self.window.btnRetry.place(x=120, y=360, width=80, height=80)
        self.window.btnOK.place(x=160, y=280, width=140, height=160)
        self.threads = []

        self.window.lblBass.config(text="{} {}".format(noteName(self.bassNote), self.chordQuality))
        # we want to launch a thread, it will activate recording after count-in
        # self.parent.precountTimer = Bpm(self.choosenBpm, self.backtrack, self.backtrackDuration, self.nbOfLoops,  lambda: self.activateRecordingChords())

        self.sound.prepareBacktrackForRecord(self.backtrack)  # load the backtrack file in pygame
        self.window.lblMessage.config(text="READY ! Start when you play a note")
        self.chordNotes = []
        self.isRecording = True
        self.startingTime = 0

    def nextWindow(self):
        self.window.destroy()
        self.globalRoot.recordWindow = RecordNotesGui(self.globalRoot, self.choosenBpm, self.bassNote, self.chordQuality, self.backtrack, self.backtrackDuration, self.nbOfLoops, self.chordNotes, self.app)
        self.destroy()

    def customChordRetry(self):
        self.startingTime = 0
        self.recordedCustomChords = []

    def customChordCancel(self):
        self.recordingCustomChords = False
        self.window.destroy()

    def activateRecordingChords(self):
        # self.parent.startingTime=0 # in order to start at the first note
        self.window.lblRec.config(text="REC.", background="red", foreground="white")
        print("nbOfLoops :", self.nbOfLoops)
        pygame.mixer.music.stop()
        self.sound.playBacktrackForRecord(self.nbOfLoops)
        self.thread = MyThread("thread-canvas", self.window.canvas, self.audioInstance, self.backtrackDuration * self.nbOfLoops, self)
        self.thread.start()

    def endRecording(self):
        # self.parent.recordingCustomChords=False
        self.isRecording = False
        self.window.lblRec.config(text="Finished!", background="black", foreground="white")
        self.window.btnOK.config(state="normal")
        self.window.canvas.delete("all")
        self.window.canvas.place_forget()

    def cancel(self):
        self.window.destroy()
        try:
            self.thread.isAlive = False
        except Exception as e:
            print(e)
        pygame.mixer.music.stop()
        self.app.new_window(2)
        del self
        # self.parent.cancelThreads()
        # self.parent.record

    def handleMIDIInput(self, msg):
        if self.isRecording == True:
            if self.startingTime == 0:
                print("should start recording")
                self.activateRecordingChords()
                self.startingTime = int(round(time.time() * 1000))
                # print("first starting TIme trigger", self.startingTime)
            mTime = self.getTimeFromStart()
            dictionnary = {"type": msg.type, "note": msg.note, "velocity": msg.velocity, "time": mTime}
            self.chordNotes.append(dictionnary)

    def getTimeFromStart(self):
        return int(round(time.time() * 1000)) - self.startingTime

    def destroy(self):
        self.thread.isAlive = False
        del self.thread
        del self
        pass
