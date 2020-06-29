import datetime
from utils.bpm import Bpm
from threading import Timer
import random
import os
import time
import tkinter as tk
import json
from tkinter import ttk as ttk
import mido
from utils.midiIO import MidiIO
from threading import Timer
from mode3.recordSetupGui import RecordSetupGui
from mode3.recordNotesGui import RecordNotesGui

import env

from autoload import Autoload
from utils.questionNote import CustomSignal
from utils.midiToNotenames import noteName
from utils.utilFunctions import getChordInterval
from utils.utilFunctions import formatOutputInterval

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


class Game:

    def __init__(self, parent,config):
        self.isPlaying = False
        self.config= config
        self.parent=parent

        # Default path
        self.midiRepository =env.MIDI_FOLDER
        self.recordBpm = 90

        # Callbacks for buttons
        self.parent.btnRecord.config(command=self.startRecording)
        self.parent.btnPractiseLick.config(command=self.playOneLick) 
        self.parent.btnPractiseAll.config(command=self.playAll) 
        self.parent.btnDeleteSelected.config(command=self.deleteLick)
        self.parent.btnPrev.config(command=self.previousLick)
        self.parent.btnNext.config(command=self.nextLick)

        self.midiFiles =[]
        self.reloadMidiFiles()
        self.fileIndex=0

        self.parent.tree.bind('<<TreeviewSelect>>', self.on_select)

        self.midiIO = Autoload().getInstance()
        self.midiIO.setCallback(self.handleMIDIInput)

        self.recordingBassLick = False
        self.recordingNotes = False
        self.recordingCustomChords=False
        self.startingTime = 0
        self.recordedNotes =[]
        self.recordedCustomChords=[]
        self.bassNote=0
        self.chordQuality="-"
        self.transpose=0
        self.activeCustomSignals=[]
        self.lickRepetitionCounter=1
        self.lickMaxRepetition=2
        self.playOnlyChord= False

        self.currentLickIndex=0
        self.currentLick =None

        self.practiseAllLicks = False
        self.lastTranspose=0

        # we need the number of licks in order to show the user
        nbOfSamples = len(self.midiFiles) 
        if nbOfSamples == 0:
            self.parent.lblNotes.config(text="No lick, record one first !")
        else:
            # we load a random sample
            num=random.randint(0,len(self.midiFiles)-1)
            self.currentLickIndex=num
            self.loadSelectedItem(self.midiFiles[self.currentLickIndex])
            self.parent.lblMessage.config(text="Lick {} / {} loaded.".format(num+1,len(self.midiFiles)))


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


    # Return the details of the selected item
    def on_select(self, selected):
       selection = self.parent.tree.focus()
       selection_details = self.parent.tree.item(selection)
       self.loadSelectedItem(selection_details['text'])
       # we must find the index of the selected item
       counter= 0
       print("starting loop")
       for lick in self.midiFiles:
           search = os.path.join(self.midiRepository, selection_details["text"])
           if lick == search:
            #    print("FOUND")
               self.currentLickIndex=counter
           counter+=1
    #    print("index Lick selected :", self.currentLickIndex)
       
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
        self.parent.lblKey.config(foreground="white")
        self.parent.lblKey.config(text="{} {}".format(noteName(bass+transpose), mType))
        self.parent.lblNotes.config(foreground="white")
        self.parent.lblNotes.config(text=self.userMessage)
        # print("updateing , " , len(self.midiFiles))
        self.parent.lblMessage.config(text="Lick {} / {} loaded.".format(self.currentLickIndex+1,len(self.midiFiles)))
        self.parent.lblFollowing.config(text="{} / {} before transpose...".format(self.lickRepetitionCounter, self.lickMaxRepetition), foreground="white")

        

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

    def startRecording(self):
        self.cancelThreads()
        self.startingTime=0
        self.recordSetupWindow = RecordSetupGui(self.parent, self)



    def playLick(self, transpose=0, playOnlyChord=False, lastBeforeTranspose=False, lastBeforeLickChange=False):
        self.cancelThreads()
        # if there is no file, we return imediately
        if len(self.midiFiles) == 0:
            # print("no file to load...")
            return
        with open(self.currentLick, "r") as jsonfile:
            self.jsonLick = json.load(jsonfile)
        key = self.jsonLick["bass"]+transpose
        mType= self.jsonLick["type"]
        notes = self.jsonLick["notes"]
        chord_notes= self.jsonLick["chord_notes"]
        duration=self.jsonLick["duration"]
        if lastBeforeTranspose== False and lastBeforeLickChange==False:
            self.showUserInfo(self.jsonLick["bass"],mType,notes, transpose)
        self.activeCustomSignals=[]
        if playOnlyChord==False:
            for note in notes:
            # for note in chord_notes:
                # pass
                # create a new Note with timer
                self.activeCustomSignals.append(CustomSignal(self, note["type"], note["note"]+transpose, note["velocity"], note["time"]))
        # for note in chord_notes:
        for note in chord_notes:
            # pass
            # print("trying to play chord", note["type"], note["note"], note["time"])
            self.activeCustomSignals.append(CustomSignal(self, note["type"], note["note"]+transpose, note["velocity"],note["time"]))

        # we want the lick to replay and loop so we make a thread to midi_off all the notes
        delayEnd= (duration)/1000
        # print("delay" , delayEnd)
        self.nextLoopTimer = Timer(delayEnd, lambda: self.prepareNewLoop(delayEnd))
        self.nextLoopTimer.start()
        
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
            self.parent.lblFollowing.config(text="Last loop before transpose...", foreground="orange")
            newKey = noteName(self.jsonLick["bass"] + self.futureTranspose)
            self.parent.lblKey.config(foreground="orange")
            self.parent.lblKey.config(text="=>{}{}".format(newKey, self.jsonLick["type"]))
            self.parent.lblNotes.config(text="({})".format( formatOutputInterval(self.futureTranspose-self.lastTranspose)))
            self.parent.lblNotes.config(foreground="orange")
            self.lastTranspose=self.futureTranspose

        elif self.lickRepetitionCounter > self.lickMaxRepetition :
            # we pick a random transpose between -5 et 6 semitones
            self.transpose=self.futureTranspose
            self.lickRepetitionCounter=1

        if self.lickRepetitionCounter ==1 :
            self.playLick(self.transpose)
        else:
        # TODO : find a rule here i think play melody one time each transpose is OK
            if self.lickRepetitionCounter == self.lickMaxRepetition:
                self.playLick(self.transpose,playOnlyChord=True, lastBeforeTranspose=True)
            else:
                self.playLick(self.transpose, playOnlyChord=True)
    
    def prepareNewLoopAllLicks(self,delay):
        self.lickRepetitionCounter +=1
        print("ALL LOPPSSSSS", self.lickRepetitionCounter, self.lickMaxRepetition)
        # if we practise all licks we must choose a new lick
        # i can't get the selection of tree so we have to reload a nextFile
        # case where we practise all licks
        if self.lickRepetitionCounter == self.lickMaxRepetition:
            self.parent.lblFollowing.config(text="Last loop before changing Lick...", foreground="orange")
            self.playLick(self.transpose, lastBeforeLickChange=True)
        elif self.lickRepetitionCounter > self.lickMaxRepetition:
            self.lickRepetitionCounter=1
            nextFile=""
            num = random.randint(0,len(self.midiFiles)-1)
            #we must check hehre the number of repetitions
            # we cahnge lick if it is the end
            # TODO: resolve the case where there is only 1 lick !!!!
            if len(self.midiFiles) == 0:
                return
            num =random.randint(0,len(self.midiFiles)-1)
            nextFile = self.midiFiles[num]
            self.loadSelectedItem(nextFile)
            self.transpose=random.randint(-5,6)
        print("before switch" , self.lickRepetitionCounter)

        if self.lickRepetitionCounter == 1:
            self.playLick(self.transpose)
        else:
            self.playLick(self.transpose,playOnlyChord=True)
    
    
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
            self.playLick()
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
            self.playLick()
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
                self.parent.lblNotes.config(text="No lick, record one first !")
                self.parent.lblKey.config(text="")
                self.parent.lblFollowing.config(text="")
                self.parent.lblMessage.config(text="")
        except Exception as e:
            print("Error trying to delete lick", self.currentLick, e)


    def playChord(self, bass, mType):
        for note in self.recordedCustomChords:
            CustomSignal(self,note["type"], note["note"],note["velocity"], note["time"])
        # print(self.recordedCustomChords)

    def createJson(self, bassNote,chordQuality):
        mTime = self.getTimeFromStart()
        obj = {
                "bass": bassNote,
                "type": chordQuality,
                "chord_notes": self.recordedCustomChords,
                "notes": self.recordedNotes,
                "duration":mTime
                }
        # creation d'un objet json
        json_object = json.dumps(obj, indent=4)
        # sauvegarde json dans un objet
        # TODO : Make try excerpt
        now_string=str(int(round(time.time())*1000))
        outfile = os.path.join(self.midiRepository, now_string+".json")
        # TODO : increase counter if file exists
        print("saving : ", outfile, "data :" ,json_object)
        with open(outfile, "w+") as outfile:
            outfile.write(json_object)
        # print("file saved") # TODO : maku user info for this
        self.recordedNotes = []
        self.startingTime = 0
        self.recordingNotes = False
        self.recordingBassLick = False
        self.reloadMidiFiles()
        self.currentLickIndex=len(self.midiFiles)-1
        self.currentLick=self.midiFiles[self.currentLickIndex]
        self.loadSelectedItem(self.currentLick)
        # self.recordNotes.destroy() # close windwo
        # self.reloadTree()
        self.currentLickIndex=len(self.midiFiles)-1
        self.currentLick = self.midiFiles[self.currentLickIndex]
        self.loadSelectedItem(self.currentLick)

    def insertNoteAtTimeInJson(self,msg, time):
        dictionnary =  { 
                "type": msg.type,
                "note": msg.note,
                "velocity": msg.velocity,
                "time": time,
                }
        self.recordedNotes.append(dictionnary)
        # we also put the note in a string in order to show the user the notes
        if msg.type == "note_on":
            self.recordNotes.stringNotes += noteName(msg.note)
    
    def insertNoteAtTimeInJsonCustomChords(self,msg,time):
        dictionnary =  { 
                "type": msg.type,
                "note": msg.note,
                "velocity": msg.velocity,
                "time": time
                }
        self.recordedCustomChords.append(dictionnary)


    def cancelThreads(self):
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
        print("TRIGGER       trying destroy")
        self.cancelThreads()
        try:
            del self.silenceIntervalTimer
            del self.nextLoopTimer
            del self.activeCustomSignals
            del self.precountTimer
        except:
            print("tried delete")
        del self

    def handleMIDIInput(self, msg):
        if self.recordingBassLick == True: # case : recording of bass
            if msg.type == "note_on":
                # print(msg.velocity)
                bassNote = msg.note
                self.recordSetupWindow.bassNote= msg.note
                self.recordSetupWindow.window.lblBass.config(text=noteName(self.recordSetupWindow.bassNote), foreground="white")
                self.recordSetupWindow.window.lblBass.config(font=("Courier", 40, "bold"))
                # self.recordSetupWindow.window.lbl2.config(text=noteName(self.bassNote), foreground="white")
                # self.recordWindow.lbl2.config(text="Choosen Key : {} {}".format( noteName(self.bassNote), str(self.chordQuality)))
                # print(bassNote)

        elif self.recordingNotes == True:
            # if self.startingTime == 0: # it means it is the first played note
                # self.startingTime = int(round(time.time()*1000))

            #TODO pass recordingNotes to False when one of the button is clicked
            mTime = self.getTimeFromStart()
            self.insertNoteAtTimeInJson(msg, mTime)
            self.recordNotes.window.lbl3.config(text="Notes : " +noteName(msg.note))

        if self.recordingCustomChords == True:
            if self.startingTime==0:
                self.startingTime=int(round(time.time()*1000))
                # print("first starting TIme trigger", self.startingTime)
            mTime =self.getTimeFromStart()
            self.insertNoteAtTimeInJsonCustomChords(msg,mTime)
            # TODO  : Le mieux est aussi d'enregistrer le backtrack dans le json

    def getTimeFromStart(self):
        return int(round(time.time()*1000)) - self.startingTime