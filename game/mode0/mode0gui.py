import tkinter as tk 
from mode0.gameplay import Game
from utils.customElements import BtnDefault
from utils.customElements import LblMode0

from utils.customElements import MyLabel8
from utils.customElements import MyLabel12
from utils.customElements import MyLabel18
from utils.customElements import MyLabel30
from utils.customElements import MyLabel40
from utils.customElements import BtnBlack20

class Mode0:
    def __init__(self,gameFrame, config):
        print( "launching game 0 -------------- ")
        self.gameFrame = gameFrame
        self.gameFrame.pack_propagate(0)

        

        # TODO : make custom fonts
        # definition of sizes and fonts
        self.gameFrame.label1 = MyLabel18(self.gameFrame) # for user instructions
        self.gameFrame.label2 = MyLabel18(self.gameFrame,padx=10, pady=10) # for "correct" or "incorrect"response
        self.gameFrame.label3 = MyLabel30(self.gameFrame,) # for global score
        self.gameFrame.btnSkip = BtnBlack20(self.gameFrame,text= "SKIP >")
        self.gameFrame.lblNote = MyLabel40(self.gameFrame)
        self.gameFrame.lblNote.config(font=("Courier", 40, "bold"))
        self.gameFrame.lblNoteUser=MyLabel40(self.gameFrame)
        self.gameFrame.lblNoteUser.config(font=("Courier", 40, "bold"))

        # placement of differents labels
        self.placeElements()

        self.game = Game(self.gameFrame, config)
        

    def placeElements(self):
        self.gameFrame.configure(bg="black") # should be invisible
        self.gameFrame.label1.place(x=0, y=10, width=320, height=50)
        self.gameFrame.label3.place(x=0,y=65, width=320, height=50)
        self.gameFrame.lblNote.place(x=30,y=110,width=200,height=80)
        self.gameFrame.lblNoteUser.place(x=200,y=110, width=100,height=80)
        self.gameFrame.label2.place(x=0, y=190,width=320,height=70)
        self.gameFrame.btnSkip.place(x=90,y=280,width=140, height=60)


    def __del__(self):
        print("trying destroy")

    def activateListening(self):
        self.game.isListening=True

        

