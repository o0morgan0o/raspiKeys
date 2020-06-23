import tkinter as tk 
from tkinter import ttk as ttk
from mode3.gameplay import Game
import utils.tinkerStyles 

from utils.customElements import BtnDefault
from utils.customElements import LblDefault
from utils.customElements import BtnWavList
from utils.customElements import BtnBigButton
from utils.customElements import LblCurrentPlaying


        


class Mode3:
    def __init__(self,gameFrame, config):
        print( "launching game 4 -------------- ")
        self.gameFrame = gameFrame
        self.gameFrame.pack_propagate(0)
        self.gameFrame.config(bg="black")

        
        # Creation of the elements
        self.gameFrame.tree = ttk.Treeview(self.gameFrame)
        self.gameFrame.btnRecord = BtnDefault(self.gameFrame, text="record")
        self.gameFrame.btnPractiseLick = BtnDefault(self.gameFrame, text="Practise Lick")
        self.gameFrame.btnPractiseAll= BtnDefault(self.gameFrame, text="Practise All")
        self.gameFrame.lblMessage = LblDefault(self.gameFrame, text="there are x licks in the base")
        self.gameFrame.lblStatic1 = LblDefault(self.gameFrame, text="licks found: ")

        # placement

        self.placeElements()
        self.game = Game(self.gameFrame, config)


        
    def placeElements(self):
        self.gameFrame.rowconfigure(0, weight=1)
        self.gameFrame.rowconfigure(1, weight=1)
        self.gameFrame.rowconfigure(2, weight=1)
        self.gameFrame.rowconfigure(3, weight=1)
        self.gameFrame.rowconfigure(4, weight=1)

        self.gameFrame.columnconfigure((0,1,2), weight=1)


        #self.gameFrame.lblStatic1.grid(row=0, column=0, columnspan=3, sticky="EW")
        self.gameFrame.tree.grid(row=1,column=0, columnspan=3, sticky="NEW")
        self.gameFrame.lblMessage.grid(row=2,column=0, columnspan=3, sticky="EW")
        self.gameFrame.btnRecord.grid(row=3,column=0, columnspan=1, sticky="NSEW")
        self.gameFrame.btnPractiseLick.grid(row=3,column=1, columnspan=1, sticky="NSEW")
        self.gameFrame.btnPractiseAll.grid(row=3,column=2, columnspan=1, sticky="NSEW")




        

    def destroy(self):
        pass
        # TODO : should i do destory here ? would be better to destroy the frame but ici les elements ne sont pas dessin�s sur la frame
#        print( "trying destroy frame 3")
#        self.game.destroy()
#        del self

    def __del__(self):
        print("trying destroy")

        

