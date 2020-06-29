import tkinter as tk 
from tkinter import ttk 
from mode2.gameplay import Game
import utils.tinkerStyles 

from utils.customElements.buttons import BtnDefault
from utils.customElements.buttons import BtnBlack20
from utils.customElements.buttons import BtnWavList
from utils.customElements.buttons import BtnBigButton

from utils.customElements.labels import LblDefault
from utils.customElements.labels import MyLabel8
from utils.customElements.labels import MyLabel12
from utils.customElements.labels import MyLabel18
from utils.customElements.labels import MyLabel30
from utils.customElements.labels import MyLabel40
from utils.customElements.labels import LblCurrentPlaying


import env

        


class Mode2:
    def __init__(self,gameFrame, config):
        print( "launching game 3 -------------- ")
        self.gameFrame = gameFrame
        self.gameFrame.pack_propagate(0)
        self.gameFrame.config(bg=env.COL_BG)

        self.gameFrame.lblStatic1 = MyLabel12(self.gameFrame,text="")
        self.gameFrame.btnPlay = BtnBlack20(self.gameFrame,text="Play")
        self.gameFrame.btnRandom = BtnBlack20(self.gameFrame,text="Random")
        self.gameFrame.labelCurrent= MyLabel12(self.gameFrame,text="", wraplength=280)
        self.gameFrame.labelCurrent.config(background="white", foreground="black")

        self.placeElements()
        self.game = Game(self.gameFrame, config)


    def placeElements(self):


        self.gameFrame.lblStatic1.place(x=0,y=20,width=320, height=40)
        self.gameFrame.labelCurrent.place(x=0, y= 100, width=340,height=120)

        self.gameFrame.btnPlay.place(x=10, y=280,width=140, height=80)
        self.gameFrame.btnRandom.place(x=170,y=280,width=140, height=80)



        

    # def destroy(self):
        # self.game.destroy()

    def __del__(self):
        print("trying destroy")

    def activateListening(self):
        self.game.isListening=True

        

