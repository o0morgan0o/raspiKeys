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
        self.gameFrame.btnDeleteSelected = BtnDefault(self.gameFrame, text="Delete lick")
        self.gameFrame.btnPractiseLick = BtnDefault(self.gameFrame, text="Practise Lick")
        self.gameFrame.btnPractiseAll= BtnDefault(self.gameFrame, text="Practise All")
        self.gameFrame.lblMessage = LblDefault(self.gameFrame, text="there are x licks in the base")
        self.gameFrame.lblStatic1 = LblDefault(self.gameFrame, text="licks found: ")

        self.gameFrame.lblUserIndication = LblDefault(self.gameFrame, text="aaaaa")


        # placement

        self.placeElements()
        self.game = Game(self.gameFrame, config)


        
    def placeElements(self):
#        self.gameFrame.rowconfigure(0, weight=1)
#        self.gameFrame.rowconfigure(1, weight=1)
#        self.gameFrame.rowconfigure(2, weight=1)
#        self.gameFrame.rowconfigure(3, weight=1)
#        self.gameFrame.rowconfigure(4, weight=1)
#
#        self.gameFrame.columnconfigure((0,1,2), weight=1)
#

        #self.gameFrame.lblStatic1.grid(row=0, column=0, columnspan=3, sticky="EW")
#        self.gameFrame.tree.grid(row=1,column=0, columnspan=3, sticky="NEW")
#        self.gameFrame.lblMessage.grid(row=2,column=0, columnspan=3, sticky="EW")
#        self.gameFrame.btnRecord.grid(row=3,column=0, columnspan=1, sticky="NSEW")
#        self.gameFrame.btnPractiseLick.grid(row=3,column=1, columnspan=1, sticky="NSEW")
#        self.gameFrame.btnPractiseAll.grid(row=3,column=2, columnspan=1, sticky="NSEW")


#        self.gameFrame.tree.pack()
#        self.gameFrame.lblMessage.pack()
#        self.gameFrame.btnRecord.pack()
#        self.gameFrame.btnDeleteSelected.pack()
#        self.gameFrame.btnPractiseLick.pack()
#        self.gameFrame.btnPractiseAll.pack()

        self.gameFrame.lblMessage.place(x=0, y=0, width=320, height=20)
        self.gameFrame.tree.place(x=0,y=30, width=200, height=180)
        self.gameFrame.btnRecord.place(x=210, y=30, width=120, height=80)
        self.gameFrame.btnDeleteSelected.place(x=210, y=120, width=120, height=80)
        self.gameFrame.btnPractiseLick.place(x=0, y=200, width=160,height=80)
        self.gameFrame.btnPractiseAll.place(x=160,y=200,width=160,height=80)
        self.gameFrame.lblUserIndication.place(x=0,y=300,width=320,height=80)






        

    def destroy(self):
        pass
        # TODO : should i do destory here ? would be better to destroy the frame but ici les elements ne sont pas dessin�s sur la frame
#        print( "trying destroy frame 3")
#        self.game.destroy()
#        del self

    def __del__(self):
        print("trying destroy")

        

