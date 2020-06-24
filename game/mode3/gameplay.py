import datetime
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

from utils.questionNote import CustomSignal
import env
from utils.midiToNotenames import noteName

from autoload import Autoload



class Game:

    def __init__(self, parent,config):
        self.config= config
        self.parent=parent

        # Default path
        self.midiRepository =env.MIDI_FOLDER

        # Callbacks for buttons
        self.parent.btnRecord.config(command=self.startRecording)
        self.parent.btnPractiseLick.config(command=self.playLick) 
        self.parent.btnPractiseAll.config(command=self.playAll) 

        self.midiFiles =[]
#        # Tree creation
#        for filename in os.listdir(self.midiRepository):
#            # get only json files
#            if os.path.splitext(filename)[1] == ".json":
#                self.parent.tree.insert("", 1, text=filename)
#                mFile = os.path.join(self.midiRepository, filename)
#                self.midiFiles.append(mFile)
        self.reloadTree()

        #self.parent.tree.selection_set(self.parent.tree.get_children()[0])
        self.parent.tree.bind('<<TreeviewSelect>>', self.on_select)



        #self.loadFile(self.midiFiles[0])
        self.midiIO = Autoload().getInstance()
        self.midiIO.setCallback(self.handleMIDIInput)

        self.recordingBassLick = False
        self.recordingNotes = False
        self.startingTime = 0
        self.recordedNotes =[]
        self.bassNote=0
        self.chordQuality="-"

        self.currentLick =None

        # TODO : il faut que le programme demande une basse
        # ensuite on joue le lick
        # en play: le programme joue la basse et donne en indice le premier interval

    def reloadTree(self):
        # update the window
       # TODO : refactor this because we use it in init
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
#        self.parent.tree.selection_set("Row 0")

        self.parent.lblMessage.config(text="there are {} licks in the base".format(counter))


    # Return the details of the selected item
    def on_select(self, selected):
       print("slected trigger", selected)
       selection = self.parent.tree.focus()
       selection_details = self.parent.tree.item(selection)
       print(selection_details['text'])
       self.loadSelectedItem(selection_details['text'])
       
    def loadSelectedItem(self, name):
        print("selected is: ", name)
        outFile = os.path.join(self.midiRepository, name)
        print(outFile)
        self.loadFile( os.path.join(self.midiRepository, name))
        print( "should be loaded")


        

    def loadFile(self, mFile):
        with open(mFile, 'r') as f:
            datastore = json.load(f)
        print(datastore)
        msgStr="Current lick: "
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
        # Etiquette
        self.recordWindow.lbl3 =LblSettings(self.recordWindow, text="Choosen Key : {} {}".format(str(self.bassNote), str(self.chordQuality)))
        self.recordWindow.lbl3.pack()
        # Button cancel
        self.recordWindow.btnCancel = BtnSettings(self.recordWindow, text="Cancel")
        self.recordWindow.btnCancel.config(command=self.recordWindow.destroy)
        self.recordWindow.btnCancel.pack()
        # Button save

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
        if quality == "minor":
            self.chordQuality="minor"
        else:
            self.chordQuality="major"
        self.recordWindow.lbl3.config(text="Choosen Key : {} {}".format(str(self.bassNote), str(self.chordQuality)))

        self.validateBeforeShowingWindow()
         

    def saveMidi(self, bassNote, recordedNotes):
        self.createJson(bassNote, recordedNotes)
        

    def createJson(self, bassNote, recordedNotes):
        obj = {
                "bass": bassNote,
                "notes": recordedNotes,
                }
        # creation d'un objet json
        json_object = json.dumps(obj, indent=4)
        print(json_object)

        # sauvegarde json dans un objet

        # TODO : Make try excerpt
        now = datetime.datetime.now()
        now_string = now.strftime("Lick_saved:%Y-%m-%d::%H:%M:%S-")
        now_string+="Lick_in_" + str(bassNote)
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


    def playLick(self):
        print("trying to replay lick0", self.currentLick) 
        # we open the json
        with open(self.currentLick, "r") as jsonfile:
            jsonLick = json.load(jsonfile)
        
        key = jsonLick["bass"]
        notes = jsonLick["notes"]
        self.parent.lblMessage.config(text="Key is"+ str(key))
        # now we loop in the array create notes obejcts with timers
        for note in notes:
            # create a new Note with timer

            print(note)
            #self.midiIO.sendOut("note_on", 60)
            a= []
            a.append(CustomSignal(self, note["type"], note["note"], note["time"]))
        

    def playAll(self):
        pass
        





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

    def destroy(self):
        print("trying destroy")
        del self
