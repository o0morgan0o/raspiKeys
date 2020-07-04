import datetime
import random
import pygame
from utils.bpm import Bpm
from threading import Timer
import threading
import random
import os
import env
import time
import tkinter as tk
import json
from tkinter import ttk as ttk
import mido
from utils.midiIO import MidiIO
from mode3.recordSetupGui import RecordSetupGui
from mode3.recordNotesGui import RecordNotesGui
from mode3.recordChordsGui import RecordChordsGui
from autoload import Autoload
from utils.questionNote import CustomSignal
from utils.midiToNotenames import noteName
from utils.utilFunctions import getChordInterval
from utils.utilFunctions import formatOutputInterval
from mode3.recordWithBacktrack import RecordWithBacktrack

from utils.customElements.buttons import *
from utils.customElements.labels import *

class Game:

    def __init__(self,globalRoot, root,config, app):

        self.isPlaying = False
        self.config= config
        self.globalRoot = globalRoot
        self.root=root
        self.app = app

        # Default path
        self.midiRepository =env.MIDI_FOLDER
        self.recordBpm = 90

        # Callbacks for buttons
        self.root.btnRecord.config(command=self.showWithOrWithoutBacktrackWindow)
        self.root.btnPractiseLick.config(command=self.playOneLick) 
        self.root.btnPractiseAll.config(command=self.playAll) 
        self.root.btnDeleteSelected.config(command=self.deleteLick)
        self.root.btnPrev.config(command=self.previousLick)
        self.root.btnNext.config(command=self.nextLick)

        self.midiFiles =[]
        self.reloadMidiFiles()
        self.fileIndex=0
        self.recordNotes = None

        self.midiIO = Autoload().getInstance()
        self.audioInstance = Autoload().getInstanceAudio()
        # self.midiIO.setCallback(self.handleMIDIInput)

        self.recordingBassLick = False
        self.recordingNotes = False
        self.recordingCustomChords=False
        self.recordedNotes =[]
        self.recordedCustomChords=[]
        self.bassNote=0
        self.chordQuality="-"
        self.transpose=0
        self.activeCustomSignals=[]
        self.lickRepetitionCounter=1
        self.lickMaxRepetition=self.config["times_each_transpose"]
        self.playOnlyChord= False

        self.currentLickIndex=0
        self.currentLick =None

        self.practiseAllLicks = False
        self.lastTranspose=0
        self.futureTranspose=0

        self.playBacktrackThread = None
        self.audioThread = None
        
        self.bass=None
        self.mType=None
        self.notes=None

        self.loadASample(len(self.midiFiles)-1)

        # we need the number of licks in order to show the user
    
    def loadASample(self, index):
        nbOfSamples = len(self.midiFiles) 
        if nbOfSamples == 0:
            self.root.lblNotes.config(text="No lick, record one first !")
        else:
            # we load last sample
            self.currentLickIndex=index
            self.loadSelectedItem(self.midiFiles[self.currentLickIndex])
            self.root.lblMessage.config(text="Lick {} / {} loaded.".format(index+1,len(self.midiFiles)))



    def reloadMidiFiles(self):
        counter=0
        midiFiles=[]
        for filename in os.listdir(self.midiRepository):
            # get only json files
            if os.path.splitext(filename)[1] == ".json":
                mFile = os.path.join(self.midiRepository, filename)
                midiFiles.append(mFile)
                counter+=1
        
        self.midiFiles = midiFiles
        self.midiFiles.sort(reverse=True)
        print("reloading ", len(self.midiFiles))
       
    def loadSelectedItem(self, name):
        self.loadFile( os.path.join(self.midiRepository, name))


    def showUserInfo(self, transpose, counter=-1, nbBeforeTranspose=-1):
        self.userMessage=""
        for note in self.notes:
            # print(note)
            if note["type"]=="note_on":
                if len(self.userMessage) > 30:
                    self.userMessage = self.userMessage[:28]+"..."
                else:
                    self.userMessage += noteName(note["note"] + transpose)+" "
        self.root.lblKey.config(foreground="white")
        self.root.lblKey.config(text="{} {}".format(noteName(self.bass + transpose), self.mType))
        self.root.lblNotes.config(foreground="white")
        self.root.lblNotes.config(text=self.userMessage)
        self.root.lblMessage.config(text="Lick {} / {} loaded.".format(self.currentLickIndex+1,len(self.midiFiles)))
        if counter != -1:
            self.root.lblFollowing.config(text="{} / {} before transpose...".format(str(counter), str(nbBeforeTranspose)), foreground="white")
        else :
            self.root.lblFollowing.config(text="")


    def showUserInfoNextTranspose(self, oldTranspose, newTranspose):
        beforeKey = noteName(self.bass + oldTranspose)
        afterKey = noteName(self.bass + newTranspose)
        self.root.lblKey.config(foreground="orange", text="{}=>{}".format(beforeKey, afterKey + self.mType))
        self.root.lblNotes.config(foreground="orange", text=formatOutputInterval(newTranspose - oldTranspose))
        self.root.lblFollowing.config(foreground="orange", text="Transpose next loop...")
        

    def loadFile(self, mFile):
        try:
            with open(mFile, 'r') as f:
                datastore = json.load(f)
                self.currentLick = mFile
                self.bass = datastore["bass"]
                self.notes=datastore["notes"]
                self.mType = datastore["type"]
                self.showUserInfo(0)
        except Exception as e:
            print("problem loading file :", mFile, e)
            return

    def showWithOrWithoutBacktrackWindow(self):
        self.cancelThreads()
        try :
            del self.globalRoot.recordWindow
        except Exception as e:
            print(e)
        self.root.destroy()
        self.destroy()
        self.globalRoot.recordWindow= RecordWithBacktrack(self.globalRoot, self.app)

    def playChords(self, transpose):
        for note in self.chord_notes:
            self.activeCustomSignals.append(CustomSignal(
                self,
                note["type"],
                note["note"] + transpose,
                note["velocity"],
                note["time"]
            ))

    def playMelody(self, transpose):
        for note in self.melodyNotes:
            self.activeCustomSignals.append(CustomSignal(
                self,
                note["type"],
                note["note"] + transpose,
                note["velocity"],
                note["time"]
            ))
        

    def activateAudioThread(self,completeTraining):
        
        # self.cancelThreads()
        with open(self.currentLick, "r") as jsonfile:
            jsonLick = json.load(jsonfile)
        self.key = jsonLick["bass"]
        self.mType= jsonLick["type"]
        self.melodyNotes = jsonLick["notes"]
        self.chord_notes= jsonLick["chord_notes"]
        self.nbOfLoops = jsonLick["nbOfLoops"]
        self.backtrack = jsonLick["backtrack"]
        self.duration=jsonLick["backtrackDuration"] * self.nbOfLoops

        self.audioThread = BackTrackThread(self,self.backtrack, self.nbOfLoops,completeTraining)
        self.audioThread.start()
    
    def previousLick(self):
        self.cancelThreads()
        pygame.mixer.music.stop()
        self.currentLickIndex += -1
        if self.currentLickIndex < 0 :
            self.currentLickIndex = len(self.midiFiles) -1
        self.loadFile(self.midiFiles[self.currentLickIndex])
        self.showUserInfo(0)

    def nextLick(self):
        self.cancelThreads()
        pygame.mixer.music.stop()
        self.currentLickIndex += 1
        if self.currentLickIndex >= len(self.midiFiles) :
            self.currentLickIndex = 0
        self.loadFile(self.midiFiles[self.currentLickIndex])
        self.showUserInfo(0)


    def playOneLick(self, completeTraining=False):
        if self.isPlaying == False:
            self.root.btnPractiseLick.config(text="STOP")
            self.isPlaying=True
            self.activateAudioThread(completeTraining)
        else:
            print("should destroy")
            self.root.btnPractiseLick.config(text="Practise Lick")
            self.audioThread.isAlive=False
            # del self.audioThread
            self.isPlaying =False
            self.cancelThreads()
            return

    def playAll(self):
        # load a new random sample
        self.loadASample(random.randint(0,len(self.midiFiles)-1))
        self.playOneLick(completeTraining=True)
        

    def deleteLick(self):
        self.cancelThreads()
        pygame.mixer.music.stop()
        try:
            print("-->try to delete lick :", self.currentLick)
            os.remove(self.currentLick)
            self.reloadMidiFiles()
            self.currentLickIndex=0
            if len(self.midiFiles)>0:
                self.currentLick = self.midiFiles[self.currentLickIndex]
                self.loadSelectedItem(self.currentLick)
            else:
                self.root.lblNotes.config(text="No lick, record one first !")
                self.root.lblKey.config(text="")
                self.root.lblFollowing.config(text="")
                self.root.lblMessage.config(text="")
        except Exception as e:
            print("Error trying to delete lick", self.currentLick, e)





    def cancelThreads(self):
        try:
            self.root.btnPractiseLick.config(text="Practise Lick")
        except:
            print("can't update screen")
        self.isPlaying =False
        try:
            self.audioThread.isAlive=False
        except Exception as e:
            print("no threads to cancel", e)
        # we try to kill all notes no already played
        for signal in self.activeCustomSignals:
            signal.timer.cancel()
        del self.activeCustomSignals
        self.activeCustomSignals = []
        self.midiIO.panic()



    def destroy(self):
        self.cancelThreads()
        pygame.mixer.music.stop()
        try:
            del self.silenceIntervalTimer
            del self.nextLoopTimer
            del self.activeCustomSignals
            del self.precountTimer
        except:
            print("tried delete")
        del self


class BackTrackThread(threading.Thread):
    def __init__(self, parent,backtrack, nbOfLoops, completeTraining):
        self.parent= parent
        threading.Thread.__init__(self)
        self.backtrack = backtrack
        self.isAlive = True
        self.nbOfLoops=nbOfLoops
        pygame.mixer.music.stop()
        pygame.event.clear()
        self.MUSIC_END= pygame.USEREVENT+1
        pygame.mixer.music.set_endevent(self.MUSIC_END)
        pygame.mixer.music.load(self.backtrack)
        # pygame.mixer.set_endevent("test")
        self.parent.playChords(0)
        self.parent.playMelody(0)
        pygame.mixer.music.play(loops=self.nbOfLoops)
        self.counter = 0
        self.transpose= 0
        print("initialisation AUDIO THREAD")
        self.nbBeforeTranspose = 4
        self.parent.showUserInfo(self.transpose,self.counter+1, self.nbBeforeTranspose)

    def run(self):
        print("runing thread...")
        while self.isAlive == True:
            for event in pygame.event.get():
                print(event.type)
                if event.type == self.MUSIC_END:
            # if pygame.mixer.music.get_busy() == False: # means it is not playing => reload a new loop
                    self.counter+=1
                    self.parent.showUserInfo(self.transpose, self.counter+1, self.nbBeforeTranspose)
                    print("relaunching backtrack loop ", self.counter, self.transpose)
                    pygame.mixer.music.play(self.nbOfLoops)
                    # self.parent.replayLick()
                    self.parent.playChords(self.transpose)
                    if self.counter % 2 == 0: # play melody one time on 2
                        self.parent.playMelody(self.transpose)

                    if self.counter == self.nbBeforeTranspose -1:
                        newTranspose= random.randint(-7,6)
                        print("transposing next loop ..." , self.transpose)
                        self.parent.showUserInfoNextTranspose(self.transpose,newTranspose)
                        self.transpose = newTranspose
                        self.counter =-1
        
        pygame.mixer.music.stop()




