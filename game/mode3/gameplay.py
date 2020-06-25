import datetime
import random
import os
import time
import tkinter as tk
import json
from tkinter import ttk as ttk
from utils.customElements import BtnDefault
from utils.customElements import BtnSettings
from utils.customElements import LblDefault
from utils.customElements import LblSettings
import mido
from utils.midiIO import MidiIO
from threading import Timer

from utils.questionNote import CustomSignal
import env
from utils.midiToNotenames import noteName
from utils.utilFunctions import getChordInterval
from autoload import Autoload


class Game:

    def __init__(self, parent,config):
        self.config= config
        self.parent=parent

        # Default path
        self.midiRepository =env.MIDI_FOLDER

        # Callbacks for buttons
        self.parent.btnRecord.config(command=self.startRecording)
        self.parent.btnPractiseLick.config(command=self.playOneLick) 
        self.parent.btnPractiseAll.config(command=self.playAll) 
        self.parent.btnDeleteSelected.config(command=self.deleteLick)

        self.midiFiles =[]
        self.reloadTree()
        self.fileIndex=0

        self.parent.tree.bind('<<TreeviewSelect>>', self.on_select)

        self.midiIO = Autoload().getInstance()
        self.midiIO.setCallback(self.handleMIDIInput)

        self.recordingBassLick = False
        self.recordingNotes = False
        self.startingTime = 0
        self.recordedNotes =[]
        self.bassNote=0
        self.chordQuality="-"
        self.transpose=0
        self.activeCustomSignals=[]

        self.currentLickIndex=0
        self.currentLick =None

        self.practiseAllLicks = False
        try:
            self.loadSelectedItem(self.midiFiles[0])
        except:
            print("can't load initial item...")


    def reloadTree(self):
        for item in self.parent.tree.get_children():
            self.parent.tree.delete(item)

        counter=0
        for filename in os.listdir(self.midiRepository):
            # get only json files
            if os.path.splitext(filename)[1] == ".json":
                self.parent.tree.insert("", 1,iid="Row {}".format(str(counter)), text=filename)
                mFile = os.path.join(self.midiRepository, filename)
                self.midiFiles.append(mFile)
                counter+=1
        try:
            self.parent.tree.selection_set("Row 0")
        except:
            print("can't load initial item...")

        self.parent.lblMessage.config(text="there are {} licks in the base".format(counter))


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
               print("FOUND")
               self.currentLickIndex=counter
           counter+=1
       print("index Lick selected :", self.currentLickIndex)
       
    def loadSelectedItem(self, name):
        print("selected is: ", name)
        outFile = os.path.join(self.midiRepository, name)
        print(outFile)
        self.loadFile( os.path.join(self.midiRepository, name))
        print( "should be loaded")


        

    def loadFile(self, mFile):
        try:
            with open(mFile, 'r') as f:
                datastore = json.load(f)
        except:
            print("problem loading file :", mFile)
            return
        msgStr="Current lick: " 
        bass = datastore["bass"]
        self.userMessage = "{} {} ({}ms)->".format(noteName(bass), datastore["type"], str(datastore["duration"])) # user Message is construct in order to show the notes of the lick to the user
        notes=datastore["notes"]
        for note in notes:
            print(note)
            if note["type"]=="note_on":
                self.userMessage += " "+noteName(note["note"])
        self.parent.lblUserIndication.config(text=self.userMessage)
        #msgStr+= "{} lick ".format(datastore["type"])
        # TODO format in order to show note name instead of midiCC
        msgStr+= "in {}".format(datastore["bass"])
        self.parent.lblMessage.config(text=msgStr)
        self.currentLick = mFile

    def startRecording(self):
        self.recordWindow = tk.Toplevel(self.parent)
        self.bassNote=0 # reinitilisation of the bassnote
        self.recordWindow.attributes('-topmost', True)
        self.recordWindow.geometry("320x480")
        # creation of 2 labels and 2 buttons
        self.recordWindow.lbl1= LblSettings(self.recordWindow,text="Recording...\nInsert only the bass note...")
        self.recordWindow.lbl1.pack()
        # show window the detected bass
        self.recordWindow.lbl2 =LblSettings(self.recordWindow,text="")
        self.recordWindow.lbl2.pack()
        # lable which show the bass entered by the user
        self.recordWindow.lblBass = tk.Label(self.recordWindow, text="-")
        self.recordWindow.lblBass.pack()
        # buttons minor and major
        self.recordWindow.btnMinor = BtnSettings(self.recordWindow, text="Minor")
        self.recordWindow.btnMinor.config(command=lambda:self.setChordQuality("minor"))
        self.recordWindow.btnMinor.pack()
        self.recordWindow.btnMajor = BtnSettings(self.recordWindow, text="Major")
        self.recordWindow.btnMajor.config(command=lambda:self.setChordQuality("major"))
        self.recordWindow.btnMajor.pack()
        self.recordWindow.btnMinor7 = BtnSettings(self.recordWindow, text="Minor7")
        self.recordWindow.btnMinor7.config(command=lambda:self.setChordQuality("min7"))
        self.recordWindow.btnMinor7.pack()
        self.recordWindow.btnMajor7 = BtnSettings(self.recordWindow, text="Major7")
        self.recordWindow.btnMajor7.config(command=lambda:self.setChordQuality("maj7"))
        self.recordWindow.btnMajor7.pack()
        self.recordWindow.btndom7 = BtnSettings(self.recordWindow, text="Dom7")
        self.recordWindow.btndom7.config(command=lambda:self.setChordQuality("dom7"))
        self.recordWindow.btndom7.pack()
        self.recordWindow.btnmin7b5 = BtnSettings(self.recordWindow, text="Min7b5")
        self.recordWindow.btnmin7b5.config(command=lambda:self.setChordQuality("min7b5"))
        self.recordWindow.btnmin7b5.pack()
        # Etiquette
        self.recordWindow.lbl3 =LblSettings(self.recordWindow, text="Choosen Key : {} {}".format(str(self.bassNote), str(self.chordQuality)))
        self.recordWindow.lbl3.pack()
        # Button cancel
        self.recordWindow.btnCancel = BtnSettings(self.recordWindow, text="Cancel")
        self.recordWindow.btnCancel.config(command=self.recordWindow.destroy)
        self.recordWindow.btnCancel.pack()

        self.recordingBassLick= True
        self.parent.lblMessage.configure(text="Recording... Insert Bass Note")

    
    def validateBeforeShowingWindow(self):
        if self.bassNote == 0 or self.chordQuality == "-": # check if user done the inputs
            self.recordWindow.lbl3.configure(text="Error, you need a valid bass note and valid chord quality!")
        else:
            # we close the bass record window and open the note record window
            self.recordingBassLick=False # desactivate the listen of user Bass
            self.recordWindow.destroy()
            self.showRecordWindow(self.bassNote)


    def setChordQuality(self,quality):
        self.chordQuality=quality
        self.recordWindow.lbl3.config(text="Choosen Key : {} {}".format(str(self.bassNote), str(self.chordQuality)))
        self.validateBeforeShowingWindow()
         

    def saveMidi(self, bassNote, recordedNotes):
        self.createJson(bassNote, recordedNotes)
        

    def createJson(self, bassNote, recordedNotes):
        mTime = self.getTimeFromStart()
        obj = {
                "bass": bassNote,
                "type": self.chordQuality,
                "notes": recordedNotes,
                "duration":mTime
                }
        # creation d'un objet json
        json_object = json.dumps(obj, indent=4)
        print(json_object)

        # sauvegarde json dans un objet

        # TODO : Make try excerpt
        now = datetime.datetime.now()
        now_string = now.strftime("%Y-%m-%d_%H:%M:%S-")
        now_string+=noteName(bassNote)
        now_string+=self.chordQuality
        outfile = os.path.join(self.midiRepository, now_string+".json")
        # TODO : increase counter if file exists
        with open(outfile, "w+") as outfile:
            outfile.write(json_object)
        print("file saved") # TODO : maku user info for this
        self.recordedNotes = []
        self.startingTime = 0
        self.recordingNotes = False
        self.recordingBassLick = False
        self.alert.destroy() # close windwo
        self.reloadTree()


    def playLick(self, transpose=0):
        self.cancelThreads()
        print("trying to replay lick0", self.currentLick) 
        # we open the json
        with open(self.currentLick, "r") as jsonfile:
            jsonLick = json.load(jsonfile)
        
        key = jsonLick["bass"]+transpose
        notes = jsonLick["notes"]
        duration=jsonLick["duration"]
        self.parent.lblMessage.config(text="Key is"+ str(key+transpose))
        delay=1000 #Needed because we want to hear the bass first
        # first we play the chord:
        self.playChord(key,jsonLick["type"]) # used to play a diffrent chord type
    #        bassPlay=CustomSignal(self,"note_on", key,0)
        # now we loop in the array create notes obejcts with timers
        self.userMessage = "{} {}->".format(noteName(key), jsonLick["type"]) # user Message is construct in order to show the notes of the lick to the user
        self.activeCustomSignals=[]
        for note in notes:
            # create a new Note with timer
            self.activeCustomSignals.append(CustomSignal(self, note["type"], note["note"]+transpose, note["time"]+delay))
            if note["type"]=="note_on":
                self.userMessage += " {}".format(noteName(note["note"] + transpose))

        self.parent.lblUserIndication.config(text=self.userMessage)
        # we want the lick to replay and loop so we make a thread to midi_off all the notes
        delayEnd= (duration+delay)/1000
        print("delay" , delayEnd)
        self.nextLoopTimer = Timer(delayEnd, lambda: self.prepareNewLoop(delayEnd))
        self.nextLoopTimer.start()
        
    def prepareNewLoop(self, delay):
        # if we practise all licks we must choose a new lick
        # i can't get the selection of tree so we have to reload a nextFile
        if self.practiseAllLicks == True:
            num = random.randint(0,len(self.midiFiles)-1)
            # TODO: resolve the case where there is only 1 lick !!!!
            while num == self.currentLickIndex:
                num =random.randint(0,len(self.midiFiles)-1)
            nextFile = self.midiFiles[num]
            self.parent.tree.selection_set("Row " + str(num))
            selection = self.parent.tree.focus()
            self.loadSelectedItem(nextFile)
        
        # modulation is done here
        # TODO set up the number of repetititons before transpose
        print("SEND PANIC AND WAIT ===================================================")
        self.midiIO.panic()
        # we pick a random transpose between -5 et 6 semitones
        num = random.randint(-5,6)
        while num ==0:
            num =random.randint(-5,6)
        self.transpose=num
        # TODO: This timer must be cancel if user click on something
        self.silenceIntervalTimer = Timer(delay,lambda: self.playLick(self.transpose))
        self.silenceIntervalTimer.start()
        




    def playOneLick(self):
        self.practiseAllLicks= False
        self.playLick()

    def playAll(self):
        self.practiseAllLicks= True
        self.playLick()
        

    def deleteLick(self):
        try:
            print("-->try to delete lick :", self.currentLick)
            os.remove(self.currentLick)
            self.reloadTree()
        except:
            print("Error trying to delete lick", self.currentLick)




    def showRecordWindow(self, bassNote):
        self.alert = tk.Toplevel(self.parent)
        self.alert.attributes('-topmost', True)
        self.alert.geometry("320x480")

        self.alert.lbl1 = tk.Label(self.alert, text="Please record now... Choosen Bass is : "+ noteName(self.bassNote))
        self.stringNotes=""
        self.alert.lbl2 = tk.Label(self.alert, text="Notes :\n" + self.stringNotes)

        # Buttons
        self.alert.btnCancel = tk.Button(self.alert, text="Cancel", command=self.cancel)
        self.alert.btnRetry = tk.Button(self.alert,text="Retry", command= self.retry)
        self.alert.btnSave = tk.Button(self.alert, text="Save", command=lambda: self.saveMidi(self.bassNote, self.recordedNotes))

        self.recordingNotes = True
        self.recordingStartTime = int(time.time()* 1000)
        print("starting time", self.recordingStartTime)


        self.alert.lbl1.pack()
        self.alert.lbl2.pack()
        self.alert.btnCancel.pack()
        self.alert.btnRetry.pack()
        self.alert.btnSave.pack()

    def cancel(self):
        self.alert.destroy()
        self.reloadTree()

    def retry(self):
        self.startingTime=0
        self.recordedNotes=[]
        self.stringNotes =""
        self.alert.lbl2.config(text="Notes :\n" + self.stringNotes)

    def playChord(self, bass, mType):
        chordTones=getChordInterval(mType)
        for chordTone in chordTones:
            CustomSignal(self, "note_on", bass + chordTone,0)


        

    #        bassPlay=CustomSignal(self,"note_on", key,0)

    def handleMIDIInput(self, msg):
        print( "receiving MIDI input, ", msg)
        if self.recordingBassLick == True: # case : recording of bass
            if msg.type == "note_on":
                bassNote = msg.note
                self.bassNote= msg.note
                self.recordWindow.lblBass.config(text=noteName(self.bassNote))
                self.recordWindow.lbl3.config(text="Choosen Key : {} {}".format( noteName(self.bassNote), str(self.chordQuality)))
                print(bassNote)

        elif self.recordingNotes == True:
            if self.startingTime == 0: # it means it is the first played note
                self.startingTime = int(round(time.time()*1000))

            #TODO pass recordingNotes to False when one of the button is clicked
            mTime = self.getTimeFromStart()
            self.insertNoteAtTimeInJson(msg, mTime)
            self.alert.lbl2.config(text="Notes :\n" +self.stringNotes)
            


    def getTimeFromStart(self):
        return int(round(time.time()*1000)) - self.startingTime

    def insertNoteAtTimeInJson(self,msg, time):
        dictionnary =  { 
                "type": msg.type,
                "note": msg.note,
                "time": time
                }
        self.recordedNotes.append(dictionnary)
        # we also put the note in a string in order to show the user the notes
        if msg.type == "note_on":
            self.stringNotes += noteName(msg.note)


    def cancelThreads(self):
        try:
            self.nextLoopTimer.cancel()
        except:
            print("no threads to cancel")
        try:
            self.silenceIntervalTimer.cancel()
        except:
            print("no threads to cancel")
        # we try to kill all notes no already played
        for signal in self.activeCustomSignals:
            signal.timer.cancel()
        self.midiIO.panic()


    def destroy(self):
        self.cancelThreads()
        print("trying destroy")
        del self
