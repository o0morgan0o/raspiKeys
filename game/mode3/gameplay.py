import datetime
from utils.bpm import Bpm
from threading import Timer
import random
import os
import time
import tkinter as tk
import json
from tkinter import ttk as ttk
from utils.customElements.buttons import BtnDefault
from utils.customElements.buttons import BtnSettings
from utils.customElements.labels import LblDefault
from utils.customElements.labels import LblSettings
import mido
from utils.midiIO import MidiIO
from threading import Timer

from utils.questionNote import CustomSignal
import env
from utils.midiToNotenames import noteName
from utils.utilFunctions import getChordInterval
from utils.utilFunctions import formatOutputInterval
from autoload import Autoload


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
        self.recordWindow = tk.Toplevel(self.parent)
        self.bassNote=0 # reinitilisation of the bassnote
        self.recordWindow.geometry("320x480")
        self.recordWindow.attributes('-fullscreen', True)
        self.recordWindow["bg"]="black"
        # creation of 2 labels and 2 buttons
        self.recordWindow.lbl1= MyLabel12(self.recordWindow,text="Recording...\nInsert Bass note and click on chord type.")
        # show window the detected bass
        self.recordWindow.lbl2 =MyLabel30(self.recordWindow,text="")
        # lable which show the bass entered by the user
        self.recordWindow.lblBass = MyLabel18(self.recordWindow, text="Listening key...")
        self.recordWindow.lblBass.config(foreground="red")
        # buttons minor and major
        self.recordWindow.btnMinor = BtnBlack12(self.recordWindow, text="Minor")
        self.recordWindow.btnMinor.config(command=lambda:self.setChordQuality("minor"))
        self.recordWindow.btnMajor = BtnBlack12(self.recordWindow, text="Major")
        self.recordWindow.btnMajor.config(command=lambda:self.setChordQuality("major"))
        self.recordWindow.btndom7 = BtnBlack12(self.recordWindow, text="Dom7")
        self.recordWindow.btndom7.config(command=lambda:self.setChordQuality("dom7"))
        # slider
        self.recordWindow.bpmScale=tk.Scale(self.recordWindow, from_=40, to=140, resolution=1, orient=tk.HORIZONTAL )
        self.recordWindow.bpmScale.config(command=self.updateBpmValue, label="BPM", font=("Courier", 20, "bold"))
        self.recordWindow.bpmScale.config(background="black", foreground="white", sliderlength=80, width=70,bd=0)
        self.recordWindow.bpmScale.set(60) # default value for bpm record
        #custom progression
        self.recordWindow.btnCustom=BtnBlack12(self.recordWindow, text="Record BackChord")
        self.recordWindow.btnCustom.config(command=self.validateBeforeShowingWindow)
        # Button cancel
        self.recordWindow.btnCancel = BtnBlack12(self.recordWindow, text="Cancel")
        self.recordWindow.btnCancel.config(command=self.recordWindow.destroy)

        #----Placement------
        self.recordWindow.lbl1.place(x=0,y=10,width=320, height=40)
        self.recordWindow.lblBass.place(x=0,y=50, width=320, height=60)
        self.recordWindow.lbl2.place(x=0, y=120, width=320,height=30)

        self.recordWindow.btnMinor.place(x=25, y=180, width=90, height=60)
        self.recordWindow.btnMajor.place(x=115, y=180, width=90, height=60)
        self.recordWindow.btndom7.place(x=205, y=180, width=90, height=60)
        self.recordWindow.bpmScale.place(x=40, y=280, width=240, height=100)

        self.recordWindow.btnCustom.place(x=160, y=400, width=130, height=60)
        self.recordWindow.btnCancel.place(x=30, y=400, width=130, height=60)

        self.recordingBassLick= True

    def updateBpmValue(self, value):
        # print(value)
        self.recordBpm=value
        # print(self.recordBpm)

    
    def validateBeforeShowingWindow(self):
        if self.bassNote == 0 or self.chordQuality == "-": # check if user done the inputs
            self.recordWindow.lbl1.configure(foreground="red")
            self.recordWindow.lbl1.configure(text="Error, you need a valid bass note and valid chord quality!")
        
        else:
            self.recordingBassLick=False # desactivate the listen of user Bass
            self.recordWindow.destroy()
            self.showRecordCustomChordWindow(self.bassNote)


    def setChordQuality(self,quality):
        self.chordQuality=quality
        self.recordWindow.lbl1.config(text="Choosen Key : {} {}".format(str(self.bassNote), str(self.chordQuality)))
        self.recordWindow.lbl2.config(text=self.chordQuality)
         

    def saveMidi(self, bassNote, recordedNotes):
        self.createJson(bassNote, recordedNotes)
        self.currentLickIndex= len(self.midiFiles)-1
        self.currentLick = self.midiFiles[self.currentLickIndex]
        self.loadSelectedItem(self.currentLick)
        

    def createJson(self, bassNote, recordedNotes):
        mTime = self.getTimeFromStart()
        obj = {
                "bass": bassNote,
                "type": self.chordQuality,
                "chord_notes": self.recordedCustomChords,
                "notes": recordedNotes,
                "duration":mTime
                }
        # creation d'un objet json
        json_object = json.dumps(obj, indent=4)
        # print(json_object)

        # sauvegarde json dans un objet

        # TODO : Make try excerpt
        now = datetime.datetime.now()
        print("output file: ",now)
        now_string = now.strftime("%Y-%m-%d_%H:%M:%S-")
        now_string+=noteName(bassNote)
        now_string+=self.chordQuality
        outfile = os.path.join(self.midiRepository, now_string+".json")
        # TODO : increase counter if file exists
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
        self.alert.destroy() # close windwo
        # self.reloadTree()


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
                # create a new Note with timer
                self.activeCustomSignals.append(CustomSignal(self, note["type"], note["note"]+transpose, note["velocity"], note["time"]))
        for note in chord_notes:
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
        self.practiseAllLicks= False
        self.playLick()

    def playAll(self):
        # should load random file
        # one transpose 
            # play lick 4 tims
        # change lick and transpose
        self.transpose=random.randint(-5,6)
        self.practiseAllLicks= True
        self.playLick()
        

    def deleteLick(self):
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




    def showRecordWindow(self, bassNote):
        self.alert = tk.Toplevel(self.parent)
        self.alert.attributes('-fullscreen', True)
        self.alert.geometry("320x480")
        self.alert["bg"]="black"

        self.alert.lbl1 = MyLabel18(self.alert, text="Please record now...")
        self.stringNotes=""
        self.alert.lbl2=MyLabel40(self.alert,text="{} {}".format(noteName(self.bassNote), self.chordQuality))
        self.alert.lbl3 = MyLabel24(self.alert, text="Notes :\n\n" + self.stringNotes)

        # Buttons
        self.alert.btnCancel = BtnBlack12(self.alert, text="Cancel", command=self.cancel)
        self.alert.btnRetry = BtnBlack12(self.alert,text="Retry", command= self.retry)
        self.alert.btnSave = BtnBlack12(self.alert, text="Save", command=lambda: self.saveMidi(self.bassNote, self.recordedNotes))

        self.recordingNotes = True
        self.recordingStartTime = int(time.time()* 1000)
        print("starting time", self.recordingStartTime)


        self.alert.lbl1.place(x=0,y=40,width=320, height=80)
        self.alert.lbl2.place(x=0,y=140,width=320, height=80)
        self.alert.lbl3.place(x=0, y= 220, width=320, height=120)
        self.alert.btnCancel.place(x=20,y=360, width=80, height=80)
        self.alert.btnRetry.place(x=120,y=360,width=80,height=80)
        self.alert.btnSave.place(x=220,y=360,width=80,height=80)


        self.precountTimer = Bpm(self.recordBpm, lambda: self.activateRecordingNotes())

    def showRecordCustomChordWindow(self, bassNote):
        self.recordedCustomChords=[]
        self.customChordNotes=[]
        self.customChordWindow=tk.Toplevel(self.parent)
        self.customChordWindow.attributes('-fullscreen', True)
        self.customChordWindow.geometry("320x480")
        self.customChordWindow["bg"]="black"
        self.customChordWindow.lblMessage = MyLabel18(self.customChordWindow, text="Record your progression,\nRecord start when you press a key...")
        self.customChordWindow.lblBass =MyLabel40(self.customChordWindow, text="Key")
        self.customChordWindow.btnRetry=BtnBlack12(self.customChordWindow, text="Retry")
        self.customChordWindow.btnCancel=BtnBlack12(self.customChordWindow, text="Cancel")
        self.customChordWindow.btnOK=BtnBlack12(self.customChordWindow, text="OK")
        self.customChordWindow.btnOK.config(command=self.customChordSave)

        # placement
        self.customChordWindow.lblMessage.place(x=0, y=20, width=320, height=50)
        self.customChordWindow.lblBass.place(x=0, y=80, width=320, height=50)
        self.customChordWindow.btnCancel.place(x=20, y=360, width=80, height=80)
        self.customChordWindow.btnRetry.place(x=120, y=360, width=80, height=80)
        self.customChordWindow.btnOK.place(x=220, y=360, width=80, height=80)

        # we want to launch a thread, it will activate recording after count-in
        self.precountTimer = Bpm(self.recordBpm, lambda: self.activateRecordingChords())

    def activateRecordingNotes(self):
        self.startingTime = int(round(time.time()*1000))
        self.playChord(self.bassNote, self.chordQuality) # in order to play the chord when the user record
        self.alert["bg"]="red"

    def activateRecordingChords(self):
        self.startingTime=0 # in order to start at the first note
        self.customChordWindow["bg"]="red"
        self.recordingCustomChords=True




    def customChordSave(self):
        # print(self.recordedCustomChords)
        self.recordingCustomChords=False
        self.customChordWindow.destroy()
        self.showRecordWindow(self.bassNote)

    def customChordRetry(self):
        self.startingTime=0
        self.recordedCustomChords=[]
    
    def customChordCancel(self):
        self.recordingCustomChords=False
        self.customChordWindow.destroy()




    def cancel(self):
        self.alert.destroy()
        self.reloadMidiFiles()

    def retry(self):
        self.startingTime=0
        self.recordedNotes=[]
        self.stringNotes =""
        self.alert.lbl3.config(text="Notes :\n" + self.stringNotes)
        self.precountTimer = Bpm(self.recordBpm, lambda: self.activateRecordingNotes())

    def playChord(self, bass, mType):
        for note in self.recordedCustomChords:
            CustomSignal(self,note["type"], note["note"],note["velocity"], note["time"])
        # print(self.recordedCustomChords)


        


    def handleMIDIInput(self, msg):
        # print( "receiving MIDI input, ", msg)
        if self.recordingBassLick == True: # case : recording of bass
            if msg.type == "note_on":
                # print(msg.velocity)
                bassNote = msg.note
                self.bassNote= msg.note
                self.recordWindow.lblBass.config(text=noteName(self.bassNote), foreground="white")
                self.recordWindow.lblBass.config(font=("Courier", 40, "bold"))
                # self.recordWindow.lbl2.config(text="Choosen Key : {} {}".format( noteName(self.bassNote), str(self.chordQuality)))
                # print(bassNote)

        elif self.recordingNotes == True:
            # if self.startingTime == 0: # it means it is the first played note
                # self.startingTime = int(round(time.time()*1000))

            #TODO pass recordingNotes to False when one of the button is clicked
            mTime = self.getTimeFromStart()
            self.insertNoteAtTimeInJson(msg, mTime)
            self.alert.lbl3.config(text="Notes :\n\n" +self.stringNotes)

        if self.recordingCustomChords == True:
            if self.startingTime==0:
                self.startingTime=int(round(time.time()*1000))
                # print("first starting TIme trigger", self.startingTime)
            mTime =self.getTimeFromStart()
            self.insertNoteAtTimeInJsonCustomChords(msg,mTime)
            # TODO  : Le mieux est aussi d'enregistrer le backtrack dans le json

            


    def getTimeFromStart(self):
        return int(round(time.time()*1000)) - self.startingTime

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
            self.stringNotes += noteName(msg.note)
    
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
