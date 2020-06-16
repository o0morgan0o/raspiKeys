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
    def __init__(self,parent):
        print( "launching game 3 -------------- ")
        self.parent = parent
        self.parent.pack_propagate(0)
        self.parent.config(bg="black")

        self.btnPlay = BtnBigButton(text="play/Pause")
        self.btnPlay.place(relx = .08, rely = .92,anchor=tk.SW)

        self.btnRandom = BtnBigButton(text="random song")
        self.btnRandom.place(relx=.92, rely= .92, anchor=tk.SE)


        self.randTrack0 = BtnWavList(text="" , height= 2)
        self.randTrack0.place(relx=.5, rely=.1+ .1, relwidth=.8,  anchor=tk.N)
        self.randTrack1 = BtnWavList(text="" , height=2)
        self.randTrack1.place(relx=.5, rely=.1+ 2*.1, relwidth=.8,  anchor=tk.N)
        self.randTrack2 = BtnWavList(text="" , height=2)
        self.randTrack2.place(relx=.5, rely=.1+ 3*.1, relwidth=.8,  anchor=tk.N)
        self.randTrack3 = BtnWavList(text="" , height=2)
        self.randTrack3.place(relx=.5, rely=.1+ 4*.1, relwidth=.8,  anchor=tk.N)
       

        self.labelCurrent= LblCurrentPlaying(text="")
        self.labelCurrent.place(relx = .5, rely = .62, anchor = tk.N, relwidth = 1)



        self.game = Game(self)



        

    def update(self):
        print("updating UI")

    def destroy(self):
        self.game.destroy()

    def __del__(self):
        print("trying destroy")

    def activateListening(self):
        self.game.isListening=True

        

