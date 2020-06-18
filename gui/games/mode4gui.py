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
    def __init__(self,parent):
        print( "launching game 4 -------------- ")
        self.parent = parent
        self.parent.pack_propagate(0)
        self.parent.config(bg="black")

        
        # Creation of the elements
        self.parent.tree = ttk.Treeview()
        self.parent.btnRecord = BtnDefault(text="record")
        self.parent.btnPractiseLick = BtnDefault(text="Practise Lick")
        self.parent.btnPractiseAll= BtnDefault(text="Practise All")
        self.parent.lblMessage = LblDefault(text="there are x licks in the base")

        # placement
        self.parent.tree.pack( fill=tk.X)
        self.parent.lblMessage.pack()
        self.parent.btnRecord.pack()
        self.parent.btnPractiseLick.pack()
        self.parent.btnPractiseAll.pack()

        self.game = Game(self.parent)



        

    def update(self):
        print("updating UI")

    def destroy(self):
        # TODO : should i do destory here ? would be better to destroy the frame but ici les elements ne sont pas dessin√s sur la frame
        self.game.destroy()

    def __del__(self):
        print("trying destroy")

        

