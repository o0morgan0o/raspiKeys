import os
import time
import tkinter as tk
import json
from tkinter import ttk as ttk
from utils.customElements import BtnDefault
from utils.customElements import LblDefault
import mido
from utils.midiIO import MidiIO

from utils.questionNote import CustomSignal
import env



class Game:

    def __init__(self, parent):
        self.parent=parent

        # Default path
        self.midiRepository =env.MIDI_FOLDER

        # Callbacks for buttons
        self.parent.btnRecord.config(command=self.startRecording)
        self.parent.btnPractiseLick.config(command=self.playLick) 
        self.parent.btnPractiseAll.config(command=self.playAll) 

        self.midiFiles =[]
        # Tree creation
        for filename in os.listdir(self.midiRepository):
            # get only json files
            if os.path.splitext(filename)[1] == ".json":
                self.parent.tree.insert("", 1, text=filename)
                mFile = os.path.join(self.midiRepository, filename)
                self.midiFiles.append(mFile)

        #self.parent.tree.selection_set(self.parent.tree.get_children()[0])
        self.parent.tree.bind('<<TreeviewSelect>>', self.on_select)



        #self.loadFile(self.midiFiles[0])
        self.midiIO = MidiIO()
        self.midiIO.setCallback(self.handleMIDIInput)

        self.recordingBassLick = False
        self.recordingNotes = False
        self.startingTime = 0
        self.recordedNotes =[]

        self.currentLick =None

        # TODO : il faut que le programme demande une basse
        # ensuite on joue le lick
        # en play: le programme joue la basse et donne en indice le premier interval

    def reloadTree(self):
        # update the window
       # TODO : refactor this because we use it in init
        for item in self.parent.tree.get_children():
            self.parent.tree.delete(item)

        for filename in os.listdir(self.midiRepository):
            # get only json files
            if os.path.splitext(filename)[1] == ".json":
                self.parent.tree.insert("", 1, text=filename)
                mFile = os.path.join(self.midiRepository, filename)
                self.midiFiles.append(mFile)

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
        self.recordingBassLick= True
        self.parent.lblMessage.configure(text="Recording... Insert Bass Note")
         

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
        outfile = os.path.join(self.midiRepository, str(time.time())+ "out.json")
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
        self.alert = tk.Toplevel(self.parent.parent)
        self.alert.attributes('-topmost', True)
        self.alert.lbl1 = tk.Label(self.alert, text="Please record now... Choosen Bass is : "+ str(bassNote))
        self.alert.lbl2 = tk.Label(self.alert, text="Notes : ")

        # Buttons
        self.alert.btnCancel = tk.Button(self.alert, text="Cancel")
        self.alert.btnRetry = tk.Button(self.alert,text="Retry")
        self.bassNote = bassNote
        self.alert.btnSave = tk.Button(self.alert, text="Save", command=lambda: self.saveMidi(self.bassNote, self.recordedNotes))

        self.recordingNotes = True
        self.recordingStartTime = int(time.time()* 1000)
        print("starting time", self.recordingStartTime)


        self.alert.lbl1.pack()
        self.alert.lbl2.pack()
        self.alert.btnCancel.pack()
        self.alert.btnRetry.pack()
        self.alert.btnSave.pack()

    def handleMIDIInput(self, msg):
        print( "receiving MIDI input, ", msg)
        if self.recordingBassLick == True: # case : recording of bass
            if msg.type == "note_on":
                self.recordingBassLick=False
                bassNote = msg.note
                print(bassNote)
                # Open new window
                self.showRecordWindow(bassNote) #On passe la bassnote a la fenetre

        elif self.recordingNotes == True:
            if self.startingTime == 0: # it means it is the first played note
                self.startingTime = int(round(time.time()*1000))

            #TODO pass recordingNotes to False when one of the button is clicked
            mTime = self.getTimeFromStart()
            self.insertNoteAtTimeInJson(msg, mTime)
            pass
            


    def getTimeFromStart(self):
        return int(round(time.time()*1000)) - self.startingTime

    def insertNoteAtTimeInJson(self,msg, time):
        dictionnary =  { 
                "type": msg.type,
                "note": msg.note,
                "time": time
                }
        self.recordedNotes.append(dictionnary)


    def destroy(self):
        print("trying destroy")
        del self
