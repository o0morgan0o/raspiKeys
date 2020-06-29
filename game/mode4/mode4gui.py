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

from utils.customElements import MyLabel10
from utils.customElements import MyLabel12
from utils.customElements import MyLabel18
from utils.customElements import MyLabel24
from utils.customElements import MyLabel30

from utils.customElements import SettingsScale

        


class Mode4:
    def __init__(self,gameFrame,config, volumeSlider):
        print( "launching game 4 -------------- ")
        self.gameFrame = gameFrame
        self.gameFrame.pack_propagate(0)
        self.gameFrame.config(bg="black")

        self.gameFrame.section1=MyLabel12(self.gameFrame, text="OPTIONS:")
        self.gameFrame.label1_1= MyLabel10(self.gameFrame, text="question Delay ms:\n(Affect modes EarN and EarC)")
        self.gameFrame.slider1_1 = SettingsScale(self.gameFrame,  from_=0, to=200, orient=tk.HORIZONTAL)
        self.gameFrame.label1_2 = MyLabel10(self.gameFrame, text="Difficulty:\n(Affect mode EarN)")
        self.gameFrame.slider1_2 = SettingsScale(self.gameFrame,  from_=0, to=1000, orient=tk.HORIZONTAL)
#
        self.gameFrame.label2_1 = MyLabel10(self.gameFrame, text="Times each transpose:\n(Affect mode Lick)")
        self.gameFrame.slider2_1 = SettingsScale(self.gameFrame,  from_=0, to=200, orient=tk.HORIZONTAL)
        self.gameFrame.label2_2 = MyLabel10(self.gameFrame, text="Num of transposes / Lick:\n(Affect mode Lick)")
        self.gameFrame.slider2_2 = SettingsScale(self.gameFrame,  from_=0, to=200, orient=tk.HORIZONTAL)
#
        self.gameFrame.btnSaveDefault = BtnDefault(self.gameFrame, text="Save") 
        self.gameFrame.btnCancel = BtnDefault(self.gameFrame, text="Cancel") 

        self.gameFrame.label3_1 = MyLabel10(self.gameFrame, text="Select Midi interface:")
        self.gameFrame.btnConfig = BtnDefault(self.gameFrame, text="Select MIDI") 


        self.placeElements()

        self.game = Game(self.gameFrame, config, volumeSlider)



    def placeElements(self):

        # SECTION 1 - Ear Training Note
        self.gameFrame.section1.place(x=0, y=0, width=320, height=30)
        self.gameFrame.label1_1.place(x=0,y=30, width=175,height=60)
        self.gameFrame.slider1_1.place(x=175,y=30, width=145,height=60)
        self.gameFrame.label1_2.place(x=0,y=90, width=175, height=60)
        self.gameFrame.slider1_2.place(x=175,y=90,width=145,height=60)

        # SECTION 2 - Practise licks
        self.gameFrame.label2_1.place(x=0, y=150, width=175,height=60)
        self.gameFrame.slider2_1.place(x=175, y=150, width=145, height=60)
        self.gameFrame.label2_2.place(x=0, y=210, width=175,height=60)
        self.gameFrame.slider2_2.place(x=175, y=210, width=145,height=60)


        # SECTION 3- IkkkkkkjO
        self.gameFrame.label3_1.place(x=0,y=280, width=175, height=40)
        self.gameFrame.btnConfig.place(x=175, y=280,width=115,height=40)


        # SECTION 4 - bouttons
        self.gameFrame.btnCancel.place(x=30, y=320, width=115, height=40)
        self.gameFrame.btnSaveDefault.place(x=175, y=320,width=115, height=40)
        

    def update(self):
        print("updating UI")

    def destroy(self):
        self.game.destroy()

    def __del__(self):
        print("trying destroy")


        

