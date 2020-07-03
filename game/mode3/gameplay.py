import datetime
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

    def __init__(self,globalRoot, root,config):

        self.isPlaying = False
        self.config= config
        self.globalRoot = globalRoot
        self.root=root

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

        # we need the number of licks in order to show the user
        nbOfSamples = len(self.midiFiles) 
        if nbOfSamples == 0:
            self.root.lblNotes.config(text="No lick, record one first !")
        else:
            # we load a random sample
            num=random.randint(0,len(self.midiFiles)-1)
            self.currentLickIndex=num
            self.loadSelectedItem(self.midiFiles[self.currentLickIndex])
            self.root.lblMessage.config(text="Lick {} / {} loaded.".format(num+1,len(self.midiFiles)))


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
        print("reloading ", len(self.midiFiles))

       
    def loadSelectedItem(self, name):
        # print("selected is: ", name)
        outFile = os.path.join(self.midiRepository, name)
        # print(outFile)
        self.loadFile( os.path.join(self.midiRepository, name))
        # print( "should be loaded")


    def showUserInfo(self,bass,mType,notes, transpose=0):
        self.userMessage=""
        for note in notes:
            # print(note)
            if note["type"]=="note_on":
                if len(self.userMessage) > 30:
                    self.userMessage = self.userMessage[:28]+"..."
                else:
                    self.userMessage += noteName(note["note"]+transpose)+" "
        self.root.lblKey.config(foreground="white")
        self.root.lblKey.config(text="{} {}".format(noteName(bass+transpose), mType))
        self.root.lblNotes.config(foreground="white")
        self.root.lblNotes.config(text=self.userMessage)
        # print("updateing , " , len(self.midiFiles))
        self.root.lblMessage.config(text="Lick {} / {} loaded.".format(self.currentLickIndex+1,len(self.midiFiles)))
        self.root.lblFollowing.config(text="{} / {} before transpose...".format(self.lickRepetitionCounter, self.lickMaxRepetition), foreground="white")

        

    def loadFile(self, mFile):
        try:
            with open(mFile, 'r') as f:
                datastore = json.load(f)
                self.currentLick = mFile
                bass = datastore["bass"]
                notes=datastore["notes"]
                mType = datastore["type"]
                self.showUserInfo(bass,mType,notes)
        except Exception as e:
            # print("problem loading file :", mFile, e)
            return

    def showWithOrWithoutBacktrackWindow(self):
        self.cancelThreads()
        try :
            del self.globalRoot.recordWindow
        except Exception as e:
            print(e)
        self.root.destroy()
        self.destroy()
        self.globalRoot.recordWindow= RecordWithBacktrack(self.globalRoot)

    def playChords(self):
        for note in self.chord_notes:
            self.activeCustomSignals.append(CustomSignal(
                self,
                note["type"],
                note["note"],
                note["velocity"],
                note["time"]
            ))

    def playMelody(self):
        for note in self.melodyNotes:
            self.activeCustomSignals.append(CustomSignal(
                self,
                note["type"],
                note["note"],
                note["velocity"],
                note["time"]
            ))
        

    def activateAudioThread(self, transpose=0, playOnlyChord=False, lastBeforeTranspose=False, lastBeforeLickChange=False):
        
        self.cancelThreads()
        # if there is no file, we return imediately
        # if len(self.midiFiles) == 0:
        #     # print("no file to load...")
        #     return
        with open(self.currentLick, "r") as jsonfile:
            jsonLick = json.load(jsonfile)
        # self.key = jsonLick["bass"]+transpose
        self.key = jsonLick["bass"]
        self.mType= jsonLick["type"]
        self.melodyNotes = jsonLick["notes"]
        self.chord_notes= jsonLick["chord_notes"]
        self.nbOfLoops = jsonLick["nbOfLoops"]
        self.backtrack = jsonLick["backtrack"]
        self.duration=jsonLick["backtrackDuration"] * self.nbOfLoops

        # we must play the backtrack
        # self.playBacktrackThread = th
        # pygame.mixer.music.play(loops=nbOfLoops)
        self.audioThread = BackTrackThread(self,self.backtrack, self.nbOfLoops)
        self.audioThread.start()

        # if lastBeforeTranspose== False and lastBeforeLickChange==False:
        #     self.showUserInfo(self.jsonLick["bass"],mType,notes, transpose)
        # self.activeCustomSignals=[]
        # if playOnlyChord==False:
        #     for note in notes:
        #     # for note in chord_notes:
        #         # pass
        #         # create a new Note with timer
        #         self.activeCustomSignals.append(CustomSignal(self, note["type"], note["note"]+transpose, note["velocity"], note["time"]))
        # # for note in chord_notes:
        # for note in chord_notes:
        #     # pass
        #     # print("trying to play chord", note["type"], note["note"], note["time"])
        #     self.activeCustomSignals.append(CustomSignal(self, note["type"], note["note"]+transpose, note["velocity"],note["time"]))

        # # we want the lick to replay and loop so we make a thread to midi_off all the notes
        # delayEnd= duration
        # # print("delay" , delayEnd)
        # self.nextLoopTimer = Timer(delayEnd, lambda: self.prepareNewLoop(delayEnd))
        # self.nextLoopTimer.start()
        
    def prepareNewLoop(self, delay):
        # print("SEND PANIC AND WAIT ===================================================")
        self.midiIO.panic()
        if self.practiseAllLicks == True:
            self.prepareNewLoopAllLicks(delay) # if it is full practise of all licks
        else:
            self.prepareNewLoopOneLick(delay)  # if we practise one lick


    def prepareNewLoopOneLick(self,delay):
    # case where we practise one lick
        self.lickRepetitionCounter+=1
        if self.lickRepetitionCounter == self.lickMaxRepetition:
            num = random.randint(-5,6)
            while num ==0:
                num =random.randint(-5,6)
                
            self.futureTranspose=num
            self.root.lblFollowing.config(text="Last loop before transpose...", foreground="orange")
            newKey = noteName(self.jsonLick["bass"] + self.futureTranspose)
            self.root.lblKey.config(foreground="orange")
            self.root.lblKey.config(text="=>{}{}".format(newKey, self.jsonLick["type"]))
            self.root.lblNotes.config(text="({})".format( formatOutputInterval(self.futureTranspose-self.lastTranspose)))
            self.root.lblNotes.config(foreground="orange")
            self.lastTranspose=self.futureTranspose

        elif self.lickRepetitionCounter > self.lickMaxRepetition :
            # we pick a random transpose between -5 et 6 semitones
            self.transpose=self.futureTranspose
            self.lickRepetitionCounter=1

        # if self.lickRepetitionCounter ==1 :
            # self.playLick(self.transpose)
        else:
            pass
        # TODO : find a rule here i think play melody one time each transpose is OK
            # if self.lickRepetitionCounter == self.lickMaxRepetition:
                # self.playLick(self.transpose,playOnlyChord=True, lastBeforeTranspose=True)
            # else:
                # self.playLick(self.transpose, playOnlyChord=True)
    
    def prepareNewLoopAllLicks(self,delay):
        self.lickRepetitionCounter +=1
        print("ALL LOPPSSSSS", self.lickRepetitionCounter, self.lickMaxRepetition)
        # if we practise all licks we must choose a new lick
        # case where we practise all licks
        # if self.lickRepetitionCounter == self.lickMaxRepetition:
            # self.root.lblFollowing.config(text="Last loop before changing Lick...", foreground="orange")
            # self.playLick(self.transpose, lastBeforeLickChange=True)
        # elif self.lickRepetitionCounter > self.lickMaxRepetition:
        #     self.lickRepetitionCounter=1
        #     nextFile=""
        #     num = random.randint(0,len(self.midiFiles)-1)
        #     #we must check hehre the number of repetitions
        #     # we cahnge lick if it is the end
        #     # TODO: resolve the case where there is only 1 lick !!!!
        #     if len(self.midiFiles) == 0:
        #         return
        #     num =random.randint(0,len(self.midiFiles)-1)
        #     nextFile = self.midiFiles[num]
        #     self.loadSelectedItem(nextFile)
        #     self.transpose=random.randint(-5,6)
        # print("before switch" , self.lickRepetitionCounter)

        # if self.lickRepetitionCounter == 1:
        #     self.playLick(self.transpose)
        # else:
        #     self.playLick(self.transpose,playOnlyChord=True)
    
    
    def previousLick(self):
        self.currentLickIndex += -1
        if self.currentLickIndex < 0 :
            self.currentLickIndex = len(self.midiFiles) -1
        self.loadFile(self.midiFiles[self.currentLickIndex])
        self.cancelThreads()

    def nextLick(self):
        self.currentLickIndex += 1
        if self.currentLickIndex >= len(self.midiFiles) :
            self.currentLickIndex = 0
        self.loadFile(self.midiFiles[self.currentLickIndex])
        self.cancelThreads()


    def playOneLick(self):
        if self.isPlaying == False:
            self.isPlaying=True
            self.practiseAllLicks= False
            # self.playLick()
            self.activateAudioThread()
        else:
            self.cancelThreads()
            self.isPlaying =False
            return

    def playAll(self):
        # should load random file
        # one transpose 
            # play lick 4 tims
        # change lick and transpose
        if self.isPlaying==False:
            self.isPlaying=True
            self.transpose=random.randint(-5,6)
            self.practiseAllLicks= True
            # self.playLick()
        else:
            self.cancelThreads()
            self.isPlaying=False
        

    def deleteLick(self):
        self.cancelThreads()
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


    # def playChord(self, bass, mType):
    #     for note in self.recordedCustomChords:
    #         CustomSignal(self,note["type"], note["note"],note["velocity"], note["time"])



    def cancelThreads(self):
        try:
            self.audioThread.isAlive=False
        except:
            print("no threads to cancel")
        pygame.mixer.music.stop()
        try:
            self.nextLoopTimer.cancel()
        except:
            print("no threads to cancel")
        try:
            self.silenceIntervalTimer.cancel()
        except:
            print("no threads to cancel")
        try:
            self.precountTimer.cancel()
        except:
            print("no threads to cancel")
        # we try to kill all notes no already played
        for signal in self.activeCustomSignals:
            signal.timer.cancel()
        self.midiIO.panic()



    def destroy(self):
        self.cancelThreads()
        try:
            del self.silenceIntervalTimer
            del self.nextLoopTimer
            del self.activeCustomSignals
            del self.precountTimer
        except:
            print("tried delete")
        del self


class BackTrackThread(threading.Thread):
    def __init__(self, parent,backtrack, nbOfLoops):
        self.parent= parent
        threading.Thread.__init__(self)
        self.backtrack = backtrack
        self.isAlive = True
        self.nbOfLoops=nbOfLoops
        pygame.mixer.music.stop()
        pygame.mixer.music.load(self.backtrack)
        self.parent.playChords()
        self.parent.playMelody()
        pygame.mixer.music.play(loops=self.nbOfLoops)
        print("initialisation AUDIO THREAD")

    def run(self):
        print("runing thread...")
        while self.isAlive == True:
            if pygame.mixer.music.get_busy() == False: # means it is not playing
                print("relaunching backtrack loop")
                pygame.mixer.music.play(self.nbOfLoops)
                # self.parent.replayLick()
                self.parent.playChords()