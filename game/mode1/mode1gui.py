import tkinter as tk
from mode1.gameplay import Game

from utils.customElements.buttons import *
from utils.customElements.labels import *


class Mode1:
    def __init__(self,gameFrame,config):
        print( "launching game 1 -------------- ")
        self.gameFrame = gameFrame
        self.gameFrame.pack_propagate(0)
        

        # labels
        # definition of sizes and fonts
        self.gameFrame.label1 = MyLabel18(self.gameFrame) # for user instructions
        self.gameFrame.label2 = MyLabel18(self.gameFrame, padx=10, pady=10) # for "correct" or "incorrect"response
        self.gameFrame.label3 = MyLabel30(self.gameFrame) # for global score
        self.gameFrame.btnSkip = BtnBlack20(self.gameFrame, text= "SKIP >")
        self.gameFrame.lblNote= MyLabel18(self.gameFrame, text="")
        self.gameFrame.lblNote.config(font=("Courier", 18, "bold"))
        # canvas
        self.gameFrame.canvas = tk.Canvas(self.gameFrame, bg="black", width=200, height=70, highlightthickness=0)
        
        # placement of differents labels
        self.placeElements()

        self.game = Game(self.gameFrame, config)

    def placeElements(self):

        self.gameFrame.label1.place(x=0, y=10, width=320,height=50)
        self.gameFrame.label3.place(x=0,y=65,width=320,height=50)
        self.gameFrame.lblNote.place(x=0,y=110, width=320, height=80)
        self.gameFrame.canvas.place(x=60, y=190, width=200, height=70)
        self.gameFrame.btnSkip.place(x=90,y=280,width=140,height=60)
        

    def destroy(self):
        self.game.destroy()

    def __del__(self):
        print("trying destroy Mode1")

    def activateListening(self):
        self.game.isListening=True

