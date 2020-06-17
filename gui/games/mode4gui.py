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
        self.tree = ttk.Treeview()
        self.btnRecord = BtnDefault(text="record")
        self.btnStart = BtnDefault(text="startPractice")
        self.lblMessage = LblDefault(text="there are x licks in the base")

        # placement
        self.tree.pack( fill=tk.X)
        self.lblMessage.pack()
        self.btnRecord.pack()
        self.btnStart.pack()

        self.game = Game(self)



        

    def update(self):
        print("updating UI")

    def destroy(self):
        # TODO : should i do destory here ? would be better to destroy the frame but ici les elements ne sont pas dessin√s sur la frame
        self.game.destroy()
        self.tree.pack_forget()
        self.tree.destroy()

        del self

    def __del__(self):
        print("trying destroy")

        

