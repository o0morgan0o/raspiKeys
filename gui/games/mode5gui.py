import tkinter as tk 
from tkinter import ttk 
from games.mode5.gameplay import Game
import games.utils.tinkerStyles 

from games.utils.customElements import BtnDefault
from games.utils.customElements import LblDefault
from games.utils.customElements import BtnWavList
from games.utils.customElements import BtnBigButton
from games.utils.customElements import LblCurrentPlaying

from games.utils.customElements import LblSettings
from games.utils.customElements import BtnSettings
from games.utils.customElements import BtnDefault

        


class Mode5:
    def __init__(self,gameFrame):
        print( "launching game 5 -------------- ")
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

        self.game = Game(self.gameFrame)



        

    def update(self):
        print("updating UI")

    def destroy(self):
        self.game.destroy()

    def __del__(self):
        print("trying destroy")


        

