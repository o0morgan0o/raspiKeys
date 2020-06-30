import tkinter as tk 
from tkinter import ttk as ttk
from mode3.gameplay import Game
import utils.tinkerStyles 

from utils.customElements.buttons import BtnDefault
from utils.customElements.labels import LblDefault
from utils.customElements.buttons import BtnWavList
from utils.customElements.buttons import BtnBigButton
from utils.customElements.labels import LblCurrentPlaying

from utils.customElements.labels import LblMode3

from utils.customElements.labels import MyLabel8
from utils.customElements.labels import MyLabel12
from utils.customElements.labels import MyLabel18
from utils.customElements.labels import MyLabel30
from utils.customElements.labels import MyLabel40
from utils.customElements.buttons import BtnBlack10
from utils.customElements.buttons import BtnBlack12
from utils.customElements.buttons import BtnBlack20


        


class Mode3:
    def __init__(self,gameFrame, config):
        print( "launching game 4 -------------- ")
        self.gameFrame = gameFrame
        self.gameFrame.pack_propagate(0)
        self.gameFrame.config(bg="black")

        
        # Creation of the elements
        # self.gameFrame.tree = ttk.Treeview(self.gameFrame)
        # self.gameFrame.scrollBar = ttk.Scrollbar(self.gameFrame,orient="vertical",command=self.gameFrame.tree.yview)
        # self.gameFrame.scrollBarHor = ttk.Scrollbar(self.gameFrame,orient="horizontal",command=self.gameFrame.tree.xview)
        self.gameFrame.btnRecord = BtnBlack10(self.gameFrame, text="record")
        self.gameFrame.btnDeleteSelected = BtnBlack10(self.gameFrame, text="Delete lick")
        self.gameFrame.btnPractiseLick = BtnBlack10(self.gameFrame, text="Practise Lick")
        self.gameFrame.btnPractiseAll= BtnBlack10(self.gameFrame, text="Practise All")
        self.gameFrame.lblMessage = MyLabel12(self.gameFrame, text="there are no licks in the base")
        self.gameFrame.lblStatic1 = MyLabel12(self.gameFrame, text="licks found: ")

        self.gameFrame.lblKey = MyLabel30(self.gameFrame, text="")
        self.gameFrame.lblKey.config(font=("Courier", 30, "bold"))
        self.gameFrame.lblNotes = MyLabel12(self.gameFrame, text="notes....", wraplength=180 )
        self.gameFrame.lblFollowing = MyLabel8(self.gameFrame, text="next...")

        self.gameFrame.btnNext = BtnBlack12(self.gameFrame, text=">")
        self.gameFrame.btnNext.config(font=("Courier", 12, "bold"))
        self.gameFrame.btnPrev = BtnBlack12(self.gameFrame, text="<")
        self.gameFrame.btnPrev.config(font=("Courier", 12, "bold"))


        # placement
        self.placeElements()
        self.game = Game(self.gameFrame, config)


        
    def placeElements(self):

        self.gameFrame.lblMessage.place(x=0, y=10, width=320, height=20)

        self.gameFrame.lblKey.place(x=20,y=60, width=280, height=40)
        self.gameFrame.lblNotes.place(x=0, y=120, width=320, height=50)
        self.gameFrame.lblFollowing.place(x=0, y=180, width=320, height=30)

        self.gameFrame.btnPrev.place(x=-2,y=45, width=40,height=80)
        self.gameFrame.btnNext.place(x=275,y=40, width=47,height=80)


        self.gameFrame.btnRecord.place(x=30, y=300, width=115, height=50)
        self.gameFrame.btnDeleteSelected.place(x=175, y=300, width=115, height=50)
        self.gameFrame.btnPractiseLick.place(x=30, y=210, width=115,height=70)
        self.gameFrame.btnPractiseAll.place(x=175,y=210,width=115,height=70)






        

    def destroy(self):
        self.game.destroy()
        del self
        pass
        # TODO : should i do destory here ? would be better to destroy the frame but ici les elements ne sont pas dessin�s sur la frame
#        print( "trying destroy frame 3")
#        self.game.destroy()
#        del self

    def __del__(self):
        self.destroy()

        

