import tkinter as tk 
from tkinter import ttk as ttk
from game.mode3.gameplay import Game

from game.utils.customElements.buttons import *
from game.utils.customElements.labels import *


        


class Mode3:
    def __init__(self,globalRoot,gameFrame, config, app):
        print( "launching game 3 -------------- ")
        self.globalRoot = globalRoot
        self.gameFrame = gameFrame
        self.gameFrame.pack_propagate(0)
        self.gameFrame.config(bg="black")

        
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
        self.game = Game(self.globalRoot,self.gameFrame, config, app)


        
    def placeElements(self):
        yplacement = 10
        self.gameFrame.lblMessage.place(x=0, y=yplacement, width=320, height=20)
        yplacement+=50
        self.gameFrame.lblKey.place(x=20,y=yplacement, width=280, height=40)
        yplacement+=60
        self.gameFrame.lblNotes.place(x=0, y=yplacement, width=320, height=50)
        yplacement+=50
        self.gameFrame.lblFollowing.place(x=0, y=yplacement, width=320, height=15)

        self.gameFrame.btnPrev.place(x=-2,y=45, width=40,height=80)
        self.gameFrame.btnNext.place(x=275,y=40, width=47,height=80)
        yplacement+=20

        self.gameFrame.btnPractiseLick.place(x=30, y=yplacement, width=130,height=80)
        self.gameFrame.btnPractiseAll.place(x=160,y=yplacement,width=130,height=80)
        yplacement+=80

        self.gameFrame.btnRecord.place(x=30, y=yplacement, width=130, height=80)
        self.gameFrame.btnDeleteSelected.place(x=160, y=yplacement, width=130, height=80)






        

    def destroy(self):
        # self.game.destroy()
        self.game.destroy()
        del self
        pass
        # TODO : should i do destory here ? would be better to destroy the frame but ici les elements ne sont pas dessin�s sur la frame
#        print( "trying destroy frame 3")
#        del self

    def __del__(self):
        self.destroy()

        

