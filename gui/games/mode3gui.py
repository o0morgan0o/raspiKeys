import tkinter as tk 
from tkinter import ttk 
from games.mode3.gameplay import Game
import games.utils.tinkerStyles 

from games.utils.customElements import BtnDefault
from games.utils.customElements import LblDefault
from games.utils.customElements import BtnWavList
from games.utils.customElements import BtnBigButton
from games.utils.customElements import LblCurrentPlaying


        


class Mode3:
    def __init__(self,gameFrame):
        print( "launching game 3 -------------- ")
        self.gameFrame = gameFrame
        self.gameFrame.pack_propagate(0)
        self.gameFrame.config(bg="yellow")

        self.gameFrame.lblStatic1 = LblDefault(self.gameFrame,text="randomBeats:")
        self.gameFrame.btnPlay = BtnBigButton(self.gameFrame,text="play/Pause")
        self.gameFrame.btnRandom = BtnBigButton(self.gameFrame,text="Randoms")
        self.gameFrame.randTrack0 = BtnWavList(self.gameFrame,text="" )
        self.gameFrame.randTrack1 = BtnWavList(self.gameFrame,text="" )
        self.gameFrame.randTrack2 = BtnWavList(self.gameFrame,text="" )
        self.gameFrame.randTrack3 = BtnWavList(self.gameFrame,text="" )
        self.gameFrame.labelCurrent= LblCurrentPlaying(self.gameFrame,text="")

        self.placeElements()
        self.game = Game(self.gameFrame)


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



        

    def destroy(self):
        self.game.destroy()

    def __del__(self):
        print("trying destroy")

    def activateListening(self):
        self.game.isListening=True

        

