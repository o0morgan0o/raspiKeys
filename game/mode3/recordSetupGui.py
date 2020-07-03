import tkinter as tk
from autoload import Autoload

from mode3.recordChordsGui import RecordChordsGui

from utils.midiToNotenames import noteName
from utils.utilFunctions import getChordInterval
from utils.utilFunctions import formatOutputInterval

from utils.customElements.buttons import *
from utils.customElements.labels import *


class RecordSetupGui:
    def __init__(self,globalRoot, backtrackFile, backtrackDuration, nbOfLoops ):
        self.globalRoot=  globalRoot
        self.midiIO=Autoload().getInstance() 
        self.midiIO.setCallback(self.handleMIDIInput)
        self.backtrackFile = backtrackFile
        self.backtrackDuration = backtrackDuration
        self.nbOfLoops = nbOfLoops
        self.isRecording = False

        print("backtrack : ", backtrackFile, backtrackDuration, nbOfLoops)

        self.window= tk.Toplevel(self.globalRoot)
        self.window.geometry("320x480")
        self.window.attributes('-fullscreen', True)
        self.window["bg"]="black"
        # creation of 2 labels and 2 buttons
        self.window.lbl1= MyLabel12(self.window,text="Recording...\nInsert Bass note and click on chord type.", wraplength=280)

        # show window the detected bass
        self.window.lbl2 =MyLabel18(self.window,text="?")
        self.window.lbl2.config(foreground="red")
        # lable which show the bass entered by the user
        self.window.lblBass = MyLabel18(self.window, text="?")
        self.window.lblBass.config(foreground="red")
        # buttons minor and major
        self.window.btnMinor = BtnBlack12(self.window, text="Minor")
        self.window.btnMinor.config(command=lambda:self.setChordQuality("minor"))
        self.window.btnMajor = BtnBlack12(self.window, text="Major")
        self.window.btnMajor.config(command=lambda:self.setChordQuality("major"))
        self.window.btndom7 = BtnBlack12(self.window, text="Dom7")
        self.window.btndom7.config(command=lambda:self.setChordQuality("dom7"))
        # slider
        self.window.bpmScale=tk.Scale(self.window, from_=40, to=140, resolution=1, orient=tk.HORIZONTAL, showvalue=0 )
        self.window.bpmScale.config(command=self.updateBpmValue)
        self.window.bpmScale.config(background="black", foreground="white", sliderlength=80, width=90,bd=0)
        self.window.bpmScale.set(60) # default value for bpm record
        #custom progression
        self.window.btnCustom=BtnBlack12(self.window, text="Record BackChord", wraplength=130)
        self.window.btnCustom.config(command=self.validateBeforeShowingWindow)
        # Button cancel
        self.window.btnCancel = BtnBlack12(self.window, text="Cancel")
        self.window.btnCancel.config(command=self.window.destroy)

        #----Placement------
        self.window.lbl1.place(x=0,y=10,width=320, height=60)
        self.window.lblBass.place(x=80,y=80, width=60, height=60)
        self.window.lbl2.place(x=150, y=80, width=100,height=60)

        self.window.btnMinor.place(x=25, y=160, width=90, height=60)
        self.window.btnMajor.place(x=115, y=160, width=90, height=60)
        self.window.btndom7.place(x=205, y=160, width=90, height=60)
        self.window.bpmScale.place(x=40, y=260, width=240, height=90)

        self.window.btnCustom.place(x=160, y=370, width=130, height=90)
        self.window.btnCancel.place(x=30, y=370, width=130, height=90)





        # self.bassNote=0 # reinitilisation of the bassnote
        self.bassNote=60 # reinitilisation of the bassnote
        self.chordQuality="major"
        # self.ent.recordingBassLick= True

    def updateBpmValue(self, value):
        self.recordBpm=value

    def setChordQuality(self,quality):
        self.chordQuality=quality
        self.window.lbl1.config(text="Choosen Key : {} {}".format(str(self.bassNote), str(self.chordQuality)))
        self.window.lbl2.config(foreground="white", text=self.chordQuality, font=("Courier", 24,"bold"))

    def validateBeforeShowingWindow(self):
        print(self.bassNote , self.chordQuality)
        if self.bassNote == 0 or self.chordQuality == "-": # check if user done the inputs
            self.window.lbl1.configure(foreground="red")
            self.window.lbl1.configure(text="Error, you need a valid bass note and valid chord quality!")
        
        else:
            # self.parent.recordingBassLick=False # desactivate the listen of user Bass
            self.window.destroy()
            # TODO use the same "temp window"  in global root for all (try delete it first)
            self.globalRoot.showRecordCustomChordWindow = RecordChordsGui(
                    self.globalRoot, 
                    self.bassNote,
                    self.chordQuality,
                    self.backtrackFile,
                    self.backtrackDuration,
                    self.nbOfLoops)


    def handleMIDIInput(self, msg):
        if self.isRecording == True: # case : recording of bass
            if msg.type == "note_on":
                # print(msg.velocity)
                bassNote = msg.note
                # self.recordSetupWindow.bassNote= msg.note
                # self.recordSetupWindow.window.lblBass.config(text=noteName(self.recordSetupWindow.bassNote), foreground="white")
                # self.recordSetupWindow.window.lblBass.config(font=("Courier", 40, "bold"))
                # self.recordSetupWindow.window.lbl2.config(text=noteName(self.bassNote), foreground="white")
                # self.recordWindow.lbl2.config(text="Choosen Key : {} {}".format( noteName(self.bassNote), str(self.chordQuality)))
                # print(bassNote)
