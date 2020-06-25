import tkinter as tk 
from tkinter import ttk as ttk
from mode3.gameplay import Game
import utils.tinkerStyles 

from utils.customElements import BtnDefault
from utils.customElements import LblDefault
from utils.customElements import BtnWavList
from utils.customElements import BtnBigButton
from utils.customElements import LblCurrentPlaying

from utils.customElements import LblMode3


        


class Mode3:
    def __init__(self,gameFrame, config):
        print( "launching game 4 -------------- ")
        self.gameFrame = gameFrame
        self.gameFrame.pack_propagate(0)
        self.gameFrame.config(bg="black")

        
        # Creation of the elements
        self.gameFrame.tree = ttk.Treeview(self.gameFrame)
        self.gameFrame.scrollBar = ttk.Scrollbar(self.gameFrame,orient="vertical",command=self.gameFrame.tree.yview)
        self.gameFrame.scrollBarHor = ttk.Scrollbar(self.gameFrame,orient="horizontal",command=self.gameFrame.tree.xview)
        self.gameFrame.btnRecord = BtnDefault(self.gameFrame, text="record")
        self.gameFrame.btnDeleteSelected = BtnDefault(self.gameFrame, text="Delete lick")
        self.gameFrame.btnPractiseLick = BtnDefault(self.gameFrame, text="Practise Lick")
        self.gameFrame.btnPractiseAll= BtnDefault(self.gameFrame, text="Practise All")
        self.gameFrame.lblMessage = LblMode3(self.gameFrame, text="there are x licks in the base")
        self.gameFrame.lblStatic1 = LblMode3(self.gameFrame, text="licks found: ")

        self.gameFrame.lblUserIndication = LblMode3(self.gameFrame, text="aaaaa")


        # placement

        self.placeElements()
        self.game = Game(self.gameFrame, config)


        
    def placeElements(self):

        self.gameFrame.lblMessage.place(x=0, y=0, width=320, height=20)
        self.gameFrame.lblUserIndication.place(x=0,y=20,width=320,height=50)
        self.gameFrame.scrollBar.place(x=10,y=70,width=30,height=280)
        self.gameFrame.tree.place(x=40,y=70, width=180, height=250)
        self.gameFrame.scrollBarHor.place(x=40,y=320,width=180,height=30)
        self.gameFrame.btnRecord.place(x=230, y=70, width=90, height=70)
        self.gameFrame.btnDeleteSelected.place(x=230, y=140, width=90, height=70)
        self.gameFrame.btnPractiseLick.place(x=230, y=210, width=90,height=70)
        self.gameFrame.btnPractiseAll.place(x=230,y=280,width=90,height=70)






        

    def destroy(self):
        pass
        # TODO : should i do destory here ? would be better to destroy the frame but ici les elements ne sont pas dessin�s sur la frame
#        print( "trying destroy frame 3")
#        self.game.destroy()
#        del self

    def __del__(self):
        print("trying destroy")

        

