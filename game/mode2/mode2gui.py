import tkinter as tk 
from tkinter import ttk 
from mode2.gameplay import Game
import utils.tinkerStyles 

from utils.customElements import BtnDefault
from utils.customElements import LblDefault
from utils.customElements import BtnWavList
from utils.customElements import BtnBigButton
from utils.customElements import LblCurrentPlaying

from utils.customElements import MyLabel8
from utils.customElements import MyLabel12
from utils.customElements import MyLabel18
from utils.customElements import MyLabel30
from utils.customElements import MyLabel40
from utils.customElements import BtnBlack20


import env

        


class Mode2:
    def __init__(self,gameFrame, config):
        print( "launching game 3 -------------- ")
        self.gameFrame = gameFrame
        self.gameFrame.pack_propagate(0)
        self.gameFrame.config(bg=env.COL_BG)

        self.gameFrame.lblStatic1 = MyLabel12(self.gameFrame,text="")
        self.gameFrame.btnPlay = BtnBlack20(self.gameFrame,text="play/Pause")
        self.gameFrame.btnRandom = BtnBlack20(self.gameFrame,text="Random")
        self.gameFrame.labelCurrent= MyLabel12(self.gameFrame,text="",borderwidth=2, relief="groove")

        self.placeElements()
        self.game = Game(self.gameFrame, config)


    def placeElements(self):


        self.gameFrame.lblStatic1.place(x=0,y=20,width=320, height=40)
        self.gameFrame.labelCurrent.place(x=40, y= 140, width=240,height=80)

        self.gameFrame.btnPlay.place(x=10, y=280,width=140, height=80)
        self.gameFrame.btnRandom.place(x=170,y=280,width=140, height=80)



        

    # def destroy(self):
        # self.game.destroy()

    def __del__(self):
        print("trying destroy")

    def activateListening(self):
        self.game.isListening=True

        

