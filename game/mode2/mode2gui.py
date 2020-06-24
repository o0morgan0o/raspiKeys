import tkinter as tk 
from tkinter import ttk 
from mode2.gameplay import Game
import utils.tinkerStyles 

from utils.customElements import BtnDefault
from utils.customElements import LblDefault
from utils.customElements import BtnWavList
from utils.customElements import BtnBigButton
from utils.customElements import LblCurrentPlaying

import env

        


class Mode2:
    def __init__(self,gameFrame, config):
        print( "launching game 3 -------------- ")
        self.gameFrame = gameFrame
        self.gameFrame.pack_propagate(0)
        self.gameFrame.config(bg=env.COL_BG)

        self.gameFrame.lblStatic1 = LblDefault(self.gameFrame,text="Random beats selected:\n(Click on one of these to change beat)")
        self.gameFrame.btnPlay = BtnBigButton(self.gameFrame,text="play/Pause")
        self.gameFrame.btnRandom = BtnBigButton(self.gameFrame,text="Randoms")
        self.gameFrame.randTrack0 = BtnWavList(self.gameFrame,text="" )
        self.gameFrame.randTrack1 = BtnWavList(self.gameFrame,text="" )
        self.gameFrame.randTrack2 = BtnWavList(self.gameFrame,text="" )
        self.gameFrame.randTrack3 = BtnWavList(self.gameFrame,text="" )
        self.gameFrame.labelCurrent= LblCurrentPlaying(self.gameFrame,text="")

        self.placeElements()
        self.game = Game(self.gameFrame, config)


    def placeElements(self):
        self.gameFrame.rowconfigure((0,1,2,3,4,5,6,7,8), weight=1)
        self.gameFrame.columnconfigure(0, weight=1)
        self.gameFrame.columnconfigure(1, weight=1)
        self.gameFrame.columnconfigure(2, weight=1)
        self.gameFrame.columnconfigure(3, weight=1)

        self.gameFrame.lblStatic1.grid(row=0, column=0 , columnspan=4, sticky="EW")

        #TODO improve placement not perfect i don t understand why
        self.gameFrame.randTrack0.grid(row=1,column=1, columnspan=2, sticky="NSEW")
        self.gameFrame.randTrack1.grid(row=2,column=1, columnspan=2, sticky="NSEW")
        self.gameFrame.randTrack2.grid(row=3,column=1, columnspan=2, sticky="NSEW")
        self.gameFrame.randTrack3.grid(row=4,column=1, columnspan=2, sticky="NSEW")
        self.gameFrame.labelCurrent.grid(row=6,column=0, columnspan=4, sticky="EW")
        self.gameFrame.btnPlay.grid(row=7,column=0, columnspan=2,  sticky="NSEW")
        self.gameFrame.btnRandom.grid(row=7,column=2, columnspan=2, sticky="NSEW")



        

    # def destroy(self):
        # self.game.destroy()

    def __del__(self):
        print("trying destroy")

    def activateListening(self):
        self.game.isListening=True

        

