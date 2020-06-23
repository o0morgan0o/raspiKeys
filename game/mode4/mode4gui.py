import tkinter as tk 
from tkinter import ttk 
from mode4.gameplay import Game
import utils.tinkerStyles 

from utils.customElements import BtnDefault
from utils.customElements import LblDefault
from utils.customElements import BtnWavList
from utils.customElements import BtnBigButton
from utils.customElements import LblCurrentPlaying

from utils.customElements import LblSettings
from utils.customElements import BtnSettings
from utils.customElements import BtnDefault

        


class Mode4:
    def __init__(self,gameFrame,config):
        print( "launching game 4 -------------- ")
        self.gameFrame = gameFrame
        self.gameFrame.pack_propagate(0)
        self.gameFrame.config(bg="red")

        self.gameFrame.section1=LblSettings(self.gameFrame, text="EarTraining:")
        self.gameFrame.label1_1= LblSettings(self.gameFrame, text="question Delay (ms):")
        self.gameFrame.slider1_1 = tk.Scale(self.gameFrame,  from_=0, to=200, orient=tk.HORIZONTAL)
        self.gameFrame.label1_2 = LblSettings(self.gameFrame, text="Difficulty:")
        self.gameFrame.slider1_2 = tk.Scale(self.gameFrame,  from_=0, to=1000, orient=tk.HORIZONTAL)
#
        self.gameFrame.section2 = LblSettings(self.gameFrame, text="midi Licks")
        self.gameFrame.label2_1 = LblSettings(self.gameFrame, text="Times each transpose:")
        self.gameFrame.slider2_1 = tk.Scale(self.gameFrame,  from_=0, to=200, orient=tk.HORIZONTAL)
        self.gameFrame.label2_2 = LblSettings(self.gameFrame, text="nb of transpose before change: ")
        self.gameFrame.slider2_2 = tk.Scale(self.gameFrame,  from_=0, to=200, orient=tk.HORIZONTAL)
#
        self.gameFrame.btnSaveDefault = BtnDefault(self.gameFrame, text="Save") 
        self.gameFrame.btnCancel = BtnDefault(self.gameFrame, text="Cancel") 

        self.gameFrame.label3_1 = LblSettings(self.gameFrame, text="Select Midi interface:")
        self.gameFrame.btnConfig = BtnDefault(self.gameFrame, text="Select MIDI") 

        self.gameFrame.label3_2 = LblSettings(self.gameFrame, text="Select midi hotkey, actual is XX:")
        self.gameFrame.btnHotKey = BtnDefault(self.gameFrame, text="Change")

        self.placeElements()

        self.game = Game(self.gameFrame, config)



    def placeElements(self):
        self.gameFrame.rowconfigure((0,1,2,3,4,5,6,7,8,9), weight = 1)

        self.gameFrame.columnconfigure(0, weight=2)
        self.gameFrame.columnconfigure(1, weight=1)
        self.gameFrame.columnconfigure(2, weight=2)

        # SECTION 1 - Ear Training Note
        self.gameFrame.section1.grid(row=0, column=0, columnspan=3, sticky="EW")
        self.gameFrame.label1_1.grid(row=1,column=0, columnspan=1, sticky= "EWNS")
        self.gameFrame.slider1_1.grid(row=1,column=2, columnspan=2, sticky= "EW")
        self.gameFrame.label1_2.grid(row=2,column=0, columnspan=1, sticky= "EWNS")
        self.gameFrame.slider1_2.grid(row=2,column=2, columnspan=2, sticky= "EW")

        # SECTION 2 - Practise licks
        self.gameFrame.section2.grid(row=3, column=0,columnspan=3, sticky="EW")
        self.gameFrame.label2_1.grid(row=4,column=0, columnspan=1, sticky= "EWNS")
        self.gameFrame.slider2_1.grid(row=4,column=2, columnspan=2, sticky= "EWNS")
        self.gameFrame.label2_2.grid(row=5,column=0, columnspan=1, sticky= "EWNS")
        self.gameFrame.slider2_2.grid(row=5,column=2, columnspan=2, sticky= "EWNS")

        # SECTION 3- IkkkkkkjO
        self.gameFrame.label3_1.grid(row=7, column=0, columnspan=1, sticky="S")
        self.gameFrame.btnConfig.grid(row=7, column=2, columnspan=2, sticky="S")

        self.gameFrame.label3_2.grid(row=8, column=0, columnspan =1, sticky="S")
        self.gameFrame.btnHotKey.grid(row=8, column=2, columnspan=2, sticky="S")

        # SECTION 4 - bouttons
        self.gameFrame.btnSaveDefault.grid(row=9, column=0, columnspan=1, sticky="S")
        self.gameFrame.btnCancel.grid(row=9, column=2, columnspan=1, sticky="S")
        

    def update(self):
        print("updating UI")

    def destroy(self):
        self.game.destroy()

    def __del__(self):
        print("trying destroy")


        

