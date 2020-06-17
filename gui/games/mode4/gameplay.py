import os
import time
import tkinter as tk
import json
from tkinter import ttk as ttk
from games.utils.customElements import BtnDefault
from games.utils.customElements import LblDefault
import mido
from games.utils.midiIO import MidiIO



class Game:

    def __init__(self, parent):
        self.parent=parent
        print(self.parent)




        self.parent.btnRecord.config(command=self.startRecording)
        self.parent.btnStart.config(command=self.playLick) 



        self.midiRepository = "/home/pi/raspiKeys/gui/games/res/midi/"
        self.midiFiles =[]
        for filename in os.listdir(self.midiRepository):
            # get only json files
            if os.path.splitext(filename)[1] == ".json":
                self.parent.tree.insert("", 1, text=filename)
                mFile = os.path.join(self.midiRepository, filename)
                self.midiFiles.append(mFile)




        #self.loadFile(self.midiFiles[0])
        self.midiIO = MidiIO()
        self.midiIO.setCallback(self.handleMIDIInput)

        self.recordingBassLick = False
        self.recordingNotes = False
        self.startingTime = 0
        self.recordedNotes =[]

        # TODO : il faut que le programme demande une basse
        # ensuite on joue le lick
        # en play: le programme joue la basse et donne en indice le premier interval

    def loadExistingFiles(self):
        pass

    def loadFile(self, mFile):
        with open(mFile, 'r') as f:
            datastore = json.load(f)
        print(datastore)
        msgStr="Current lick: "
        msgStr+= "{} lick ".format(datastore["type"])
        # TODO format in order to show note name instead of midiCC
        msgStr+= "in {}".format(datastore["bass"])
        self.parent.lblMessage.config(text=msgStr)

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
        outfile = os.path.join(self.midiRepository, "out.json")
        with open(outfile, "w+") as outfile:
            outfile.write(json_object)
        print("file saved") # TODO : maku user info for this
        self.alert.destroy() # close windwo
        self.loadExistingFiles() # reload list


    def playLick(self):
        self.currentLick = self.midiFiles[0]
        print("trying to replay lick0", self.currentLick) 
        # we open the json
        with open(self.currentLick, "r") as jsonfile:
            jsonLick = json.load(jsonfile)
        
        key = jsonLick["bass"]
        notes = jsonLick["notes"]
        self.parent.lblMessage.config(text="Key is"+ str(key))
        # now we loop in the array create notes obejcts with timers
        print(notes)
        
        





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
