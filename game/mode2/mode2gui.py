import tkinter as tk 
import pygame
from tkinter import ttk 
from mode2.gameplay import Game
import utils.tinkerStyles 
import env

from utils.customElements.buttons import *
from utils.customElements.labels import *

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
        self.gameFrame.canvas = tk.Canvas(self.gameFrame)

        self.placeElements()
        self.game = Game(self.gameFrame, config)


    def placeElements(self):


        self.gameFrame.lblStatic1.place(x=0,y=20,width=320, height=40)
        self.gameFrame.labelCurrent.place(x=0, y= 100, width=340,height=120)
        self.gameFrame.canvas.place(x=20, y=240, width=280, height=20)

        self.gameFrame.btnPlay.place(x=10, y=280,width=140, height=80)
        self.gameFrame.btnRandom.place(x=170,y=280,width=140, height=80)



        

    # def destroy(self):
        # self.game.destroy()

    def __del__(self):
        print("trying destroy mode 2")
        # pygame.mixer.music.stop()
        del self
        # del self

    def activateListening(self):
        self.game.isListening=True

        

