import tkinter as tk
import env
import time
import datetime
import json
import os
import pygame

from utils.questionNote import CustomSignal
from autoload import Autoload
from utils.canvasThread import MyThread
from utils.bpm import Bpm
from utils.midiToNotenames import noteName
from utils.customElements.buttons import *
from utils.customElements.labels import *

class RecordNotesGui:
    def __init__(self,globalRoot,choosenBpm, bassNote, chordQuality, backtrack, backtrackDuration, nbOfLoops, chordNotes, app):
        self.app = app
        self.globalRoot = globalRoot
        self.midiIO= Autoload().getInstance()
        self.midiIO.setCallback(self.handleMIDIInput)
        self.audioInstance = Autoload().getInstanceAudio()
        self.backtrack = backtrack
        self.backtrackDuration = backtrackDuration
        self.nbOfLoops=nbOfLoops
        self.choosenBpm =choosenBpm
        self.chordQuality=chordQuality
        self.bassNote = bassNote
        self.window = tk.Toplevel(self.globalRoot)
        self.window.attributes('-fullscreen', True)
        self.window.geometry("320x480")
        self.window["bg"]="black"
        print("backtrack gui:", self.backtrack)
        self.chordNotes=chordNotes
        self.melodyNotes=[]
        self.customSignals=[]

        self.window.lbl1 = MyLabel12(self.window, text="Please record now...", wraplength=280)
        self.stringNotes=""
        self.window.lbl2=MyLabel40(self.window,text="{} {}".format(noteName(self.bassNote), self.chordQuality))
        self.window.lbl3 = MyLabel24(self.window, text="Notes : " + self.stringNotes, wraplength=280)
        self.window.lblRec = MyLabel18(self.window, text="")

        # Buttons
        self.window.btnCancel = BtnBlack12(self.window, text="Cancel", command=self.cancel)
        self.window.btnRetry = BtnBlack12(self.window,text="Retry", command= self.retry)
        self.window.btnSave = BtnBlack12(self.window, text="Save", command=lambda: self.saveMidi())
        # self.window.btnSave.config(state="disabled")

        self.window.canvas = tk.Canvas(self.window)

        self.window.lbl1.place(x=0,y=40,width=320, height=80)
        self.window.lbl2.place(x=0,y=120,width=320, height=60)
        self.window.lbl3.place(x=0, y=180, width=320, height=60)
        self.window.lblRec.place(x=20,y=250, width=280, height=40)
        self.window.btnCancel.place(x=20,y=310, width=100, height=130)
        self.window.btnRetry.place(x=120,y=310,width=80,height=130)
        self.window.btnSave.place(x=200,y=310,width=100,height=130)

        self.window.canvas.place(x=20, y=290,width=280, height=30)


        self.isRecording = False
        self.precountTimer = Bpm(self.choosenBpm, self.backtrack, self.backtrackDuration, self.nbOfLoops,  lambda: self.activateRecording())
        self.startingTime =0


    def cancel(self):
        self.window.destroy()
        self.thread.isAlive = False
        pygame.mixer.music.stop()
        self.app.new_window(3)
        del self

    def retry(self):
        pass
        # self.parent.cancelThreads()
        # self.parent.startingTime=0
        # self.parent.recordedNotes=[]
        # self.parent.stringNotes =""
        # self.window.lbl3.config(text="Notes : ")
        # self.parent.precountTimer = Bpm(self.choosenBpm, self.backtrack, self.backtrackDuration,self.nbOfLoops, lambda: self.activateRecordingNotes())
        # self.window.lblRec.config(background="black", text="")

    def saveMidi(self):
        # self.parent.createJson(self.bassNote, self.chordQuality, self.backtrack, self.backtrackDuration,self.nbOfLoops)
        self.cancelThreads()
        self.saveLickAsJsonFile()
        # self.cancelRecorgindThreads()
        self.window.destroy()
        self.app.new_window(3) # recreation of window 3

    def cancelThreads(self):
        self.precountTimer.cancel()
        try:
            self.thread.isAlive=False
        except Exception as e:
            print(e)
        for signal in self.customSignals:
            signal.cancel()
        self.customSignals =[]
        pygame.mixer.music.stop()
        # self.saveMidi()

    def saveLickAsJsonFile(self):
        volume = pygame.mixer.music.get_volume()
        obj = {
                "bass": self.bassNote,
                "type": self.chordQuality,
                "backtrack":self.backtrack,
                "backtrackDuration":self.backtrackDuration,
                "nbOfLoops":self.nbOfLoops,
                "chord_notes": self.chordNotes,
                "notes": self.melodyNotes,
                "volumeBacktrack": volume
                }
        # creation d'un objet json
        json_object = json.dumps(obj, indent=4)
        # sauvegarde json dans un objet
        # TODO : Make try excerpt
        now_string=str(int(round(time.time())*1000))
        outfile = os.path.join(env.MIDI_FOLDER, now_string+".json")
        # TODO : increase counter if file exists
        print("saving : ", outfile, "data :" ,json_object)
        with open(outfile, "w+") as outfile:
            outfile.write(json_object)
        # print("file saved") # TODO : maku user info for this
        self.recordedNotes = []
        self.startingTime = 0
        self.recordingNotes = False
        self.recordingBassLick = False
        # self.reloadMidiFiles()
        # self.currentLickIndex=len(self.midiFiles)-1
        # self.currentLick=self.midiFiles[self.currentLickIndex]
        # self.loadSelectedItem(self.currentLick)
        # self.recordNotes.destroy() # close windwo
        # self.currentLickIndex=len(self.midiFiles)-1
        # self.currentLick = self.midiFiles[self.currentLickIndex]
        # self.loadSelectedItem(self.currentLick)

    def activateRecording(self):
        # pass
        self.startingTime = int(round(time.time()*1000))
        # self.playChord(self.bassNote, self.chordQuality) # in order to play the chord when the user recc
        for note in self.chordNotes:
            self.customSignals.append(CustomSignal(self, note["type"], note["note"], note["velocity"], note["time"]))
        self.isRecording=True
        self.window.lblRec.config(background="red", foreground="white", text="REC.")
        self.thread = MyThread("thread-canvas", self.window.canvas, self.audioInstance,self.backtrackDuration * self.nbOfLoops, self)
        self.thread.start()
        # self.parent.recordingNotes = True


    def endRecording(self):
        # self.parent.recordingNotes=False
        self.window.lblRec.config(background="black", foreground="white", text="Finished!")
        self.window.canvas.delete("all")
        # self.window.btnSave.config(state="normal")
        self.window.canvas.place_forget()

    def destroy(self):
        self.window.destroy()


    def handleMIDIInput(self, msg):
        if self.isRecording == True:
            # if self.startingTime == 0: # it means it is the first played note
                # self.startingTime = int(round(time.time()*1000))

            #TODO pass recordingNotes to False when one of the button is clicked
            mTime = self.getTimeFromStart()
            dictionnary={
                "type":msg.type,
                "note":msg.note,
                "velocity":msg.velocity,
                "time":mTime
            }
            print("adding note ", dictionnary)
            self.melodyNotes.append(dictionnary)
            # self.recordNotes.window.lbl3.config(text="Notes : " +noteName(msg.note))

    def getTimeFromStart(self):
        return int(round(time.time()*1000)) - self.startingTime

    def destroy(self):
        print("destroying last record windows")
        self.thread.isAlive = False
        for timer in self.customSignals:
            try:
                timer.cancel()
            except Exception as e:
                print(e)

        del self.thread
