import tkinter as tk 
from tkinter import ttk as ttk
from games.mode4.gameplay import Game
import games.utils.tinkerStyles 

from games.utils.customElements import BtnDefault
from games.utils.customElements import LblDefault
from games.utils.customElements import BtnWavList
from games.utils.customElements import BtnBigButton
from games.utils.customElements import LblCurrentPlaying


        


class Mode4:
    def __init__(self,gameFrame):
        print( "launching game 4 -------------- ")
        self.gameFrame = gameFrame
        self.gameFrame.pack_propagate(0)
        self.gameFrame.config(bg="yellow")

        
        # Creation of the elements
        self.gameFrame.tree = ttk.Treeview(self.gameFrame)
        self.gameFrame.btnRecord = BtnDefault(self.gameFrame, text="record")
        self.gameFrame.btnPractiseLick = BtnDefault(self.gameFrame, text="Practise Lick")
        self.gameFrame.btnPractiseAll= BtnDefault(self.gameFrame, text="Practise All")
        self.gameFrame.lblMessage = LblDefault(self.gameFrame, text="there are x licks in the base")

        # placement

        self.placeElements()
        self.game = Game(self.gameFrame)


        
    def placeElements(self):
        self.gameFrame.rowconfigure((0,1,2,3), weight=1)
        self.gameFrame.columnconfigure(0, weight=1)

        self.gameFrame.tree.grid(row=0,column=0, columnspan=1, sticky="NSEW")
        self.gameFrame.lblMessage.grid(row=1,column=0, columnspan=1, sticky="NSEW")
        self.gameFrame.btnRecord.grid(row=2,column=0, columnspan=1, sticky="NSEW")
        self.gameFrame.btnPractiseLick.grid(row=3,column=0, columnspan=1, sticky="NSEW")
        self.gameFrame.btnPractiseAll.grid(row=4,column=0, columnspan=1, sticky="NSEW")




        

    def destroy(self):
        pass
        # TODO : should i do destory here ? would be better to destroy the frame but ici les elements ne sont pas dessin√s sur la frame
#        print( "trying destroy frame 3")
#        self.game.destroy()
#        del self

    def __del__(self):
        print("trying destroy")

        

