import tkinter as tk 
from tkinter import ttk 
from games.mode5.gameplay import Game
import games.utils.tinkerStyles 

from games.utils.customElements import BtnDefault
from games.utils.customElements import LblDefault
from games.utils.customElements import BtnWavList
from games.utils.customElements import BtnBigButton
from games.utils.customElements import LblCurrentPlaying


        


class Mode5:
    def __init__(self,parent):
        print( "launching game 5 -------------- ")
        self.parent = parent
        self.parent.pack_propagate(0)
        self.parent.config(bg="black")
        self.game = Game(self.parent)



        

    def update(self):
        print("updating UI")

    def destroy(self):
        self.game.destroy()

    def __del__(self):
        print("trying destroy")


        

