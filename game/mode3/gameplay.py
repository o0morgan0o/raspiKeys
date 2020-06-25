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
from utils.utilFunctions import formatOutputInterval
from autoload import Autoload


from utils.customElements import MyLabel8
from utils.customElements import MyLabel12
from utils.customElements import MyLabel18
from utils.customElements import MyLabel24
from utils.customElements import MyLabel30
from utils.customElements import MyLabel40
from utils.customElements import BtnBlack12
from utils.customElements import BtnBlack20



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
        self.startingTime = 0
        self.recordedNotes =[]
        self.bassNote=0
        self.chordQuality="-"
        self.transpose=0
        self.activeCustomSignals=[]
        self.lickRepetitionCounter=1
        self.lickMaxRepetition=2

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


    def showUserInfo(self,bass,mType,notes, transpose=0):
        self.userMessage=""
        for note in notes:
            print(note)
            if note["type"]=="note_on":
                self.userMessage += noteName(note["note"]+transpose)+" "
        self.parent.lblKey.config(foreground="white")
        self.parent.lblKey.config(text="{} {}".format(noteName(bass+transpose), mType))
        self.parent.lblNotes.config(foreground="white")
        self.parent.lblNotes.config(text=self.userMessage)
        print("updateing , " , len(self.midiFiles))
        self.parent.lblMessage.config(text="Lick {} / {} loaded.".format(self.currentLickIndex+1,len(self.midiFiles)))
        self.parent.lblFollowing.config(text="{} / {} before transpose...".format(self.lickRepetitionCounter, self.lickMaxRepetition))

        

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
            print("problem loading file :", mFile, e)
            return

    def startRecording(self):
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
        self.recordWindow.btnMinor7 = BtnBlack12(self.recordWindow, text="Minor7")
        self.recordWindow.btnMinor7.config(command=lambda:self.setChordQuality("min7"))
        self.recordWindow.btnMajor7 = BtnBlack12(self.recordWindow, text="Major7")
        self.recordWindow.btnMajor7.config(command=lambda:self.setChordQuality("maj7"))
        self.recordWindow.btndom7 = BtnBlack12(self.recordWindow, text="Dom7")
        self.recordWindow.btndom7.config(command=lambda:self.setChordQuality("dom7"))
        self.recordWindow.btnmin7b5 = BtnBlack12(self.recordWindow, text="Min7b5")
        self.recordWindow.btnmin7b5.config(command=lambda:self.setChordQuality("min7b5"))
        # Button cancel
        self.recordWindow.btnOK = BtnBlack20(self.recordWindow, text="OK")
        self.recordWindow.btnCancel = BtnBlack12(self.recordWindow, text="Cancel")
        self.recordWindow.btnCancel.config(command=self.recordWindow.destroy)

        #----Placement------
        self.recordWindow.lbl1.place(x=0,y=10,width=320, height=40)
        self.recordWindow.lblBass.place(x=0,y=50, width=320, height=60)
        self.recordWindow.lbl2.place(x=0, y=120, width=320,height=30)

        self.recordWindow.btnMinor.place(x=30, y=180, width=130, height=60)
        self.recordWindow.btnMinor7.place(x=30, y=240, width=130, height=60)
        self.recordWindow.btnmin7b5.place(x=30, y=300, width=130, height=60)
        self.recordWindow.btnMajor.place(x=160, y=180, width=130, height=60)
        self.recordWindow.btnMajor7.place(x=160, y=240, width=130, height=60)
        self.recordWindow.btndom7.place(x=160, y=300, width=130, height=60)

        self.recordWindow.btnOK.place(x=160, y=400, width=130, height=60)
        self.recordWindow.btnOK.config(command=self.validateBeforeShowingWindow)
        self.recordWindow.btnCancel.place(x=30, y=400, width=130, height=60)

        self.recordingBassLick= True

    
    def validateBeforeShowingWindow(self):
        if self.bassNote == 0 or self.chordQuality == "-": # check if user done the inputs
            self.recordWindow.lbl1.configure(text="Error, you need a valid bass note and valid chord quality!")
        else:
            # we close the bass record window and open the note record window
            self.recordingBassLick=False # desactivate the listen of user Bass
            self.recordWindow.destroy()
            self.showRecordWindow(self.bassNote)


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
        self.reloadMidiFiles()
        self.currentLickIndex=len(self.midiFiles)-1
        self.currentLick=self.midiFiles[self.currentLickIndex]
        self.loadSelectedItem(self.currentLick)
        self.alert.destroy() # close windwo
        # self.reloadTree()


    def playLick(self, transpose=0):
        self.cancelThreads()
        # if there is no file, we return imediately
        if len(self.midiFiles) == 0:
            print("no file to load...")
            return
        with open(self.currentLick, "r") as jsonfile:
            self.jsonLick = json.load(jsonfile)
        key = self.jsonLick["bass"]+transpose
        mType= self.jsonLick["type"]
        notes = self.jsonLick["notes"]
        duration=self.jsonLick["duration"]
        delay=1000 #Needed because we want to hear the bass first
        # first we play the chord:
        self.showUserInfo(self.jsonLick["bass"],mType,notes, transpose)
        self.playChord(key,self.jsonLick["type"]) # used to play a diffrent chord type
    #        bassPlay=CustomSignal(self,"note_on", key,0)
        # now we loop in the array create notes obejcts with timers
        self.activeCustomSignals=[]
        for note in notes:
            # create a new Note with timer
            self.activeCustomSignals.append(CustomSignal(self, note["type"], note["note"]+transpose, note["time"]+delay))

        # we want the lick to replay and loop so we make a thread to midi_off all the notes
        delayEnd= (duration+delay)/1000
        print("delay" , delayEnd)
        self.nextLoopTimer = Timer(delayEnd, lambda: self.prepareNewLoop(delayEnd))
        self.nextLoopTimer.start()
        
    def prepareNewLoop(self, delay):
        self.lickRepetitionCounter +=1
        # if we practise all licks we must choose a new lick
        # i can't get the selection of tree so we have to reload a nextFile
        if self.practiseAllLicks == True:
            nextFile=""
            num = random.randint(0,len(self.midiFiles)-1)
            # TODO: resolve the case where there is only 1 lick !!!!
            if len(self.midiFiles) > 1:
                while num == self.currentLickIndex:
                    num =random.randint(0,len(self.midiFiles)-1)
                nextFile = self.midiFiles[num]
            else:
                nextFile = self.midiFiles[0]
            self.loadSelectedItem(nextFile)
        
        # modulation is done here
        print("SEND PANIC AND WAIT ===================================================")
        self.midiIO.panic()
        if self.lickRepetitionCounter > self.lickMaxRepetition :
            # we pick a random transpose between -5 et 6 semitones
            num = random.randint(-5,6)
            while num ==0:
                num =random.randint(-5,6)
                
            self.transpose=num
            self.lickRepetitionCounter=1
            self.parent.lblFollowing.config(text="will transpose")
            newKey = noteName(self.jsonLick["bass"] + self.transpose)
            self.parent.lblKey.config(foreground="red")
            self.parent.lblKey.config(text="=>{}{}".format(newKey, self.jsonLick["type"]))
            self.parent.lblNotes.config(text="({})".format( formatOutputInterval(self.transpose-self.lastTranspose)))
            self.parent.lblNotes.config(foreground="red")
            self.lastTranspose=self.transpose
        # TODO: This timer must be cancel if user click on something
        self.silenceIntervalTimer = Timer(delay,lambda: self.playLick(self.transpose))
        self.silenceIntervalTimer.start()
        
    
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

    def cancel(self):
        self.alert.destroy()
        self.reloadMidiFiles()

    def retry(self):
        self.startingTime=0
        self.recordedNotes=[]
        self.stringNotes =""
        self.alert.lbl3.config(text="Notes :\n" + self.stringNotes)

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
                self.recordWindow.lblBass.config(text=noteName(self.bassNote), foreground="white")
                self.recordWindow.lblBass.config(font=("Courier", 40, "bold"))
                # self.recordWindow.lbl2.config(text="Choosen Key : {} {}".format( noteName(self.bassNote), str(self.chordQuality)))
                print(bassNote)

        elif self.recordingNotes == True:
            if self.startingTime == 0: # it means it is the first played note
                self.startingTime = int(round(time.time()*1000))

            #TODO pass recordingNotes to False when one of the button is clicked
            mTime = self.getTimeFromStart()
            self.insertNoteAtTimeInJson(msg, mTime)
            self.alert.lbl3.config(text="Notes :\n\n" +self.stringNotes)
            


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
