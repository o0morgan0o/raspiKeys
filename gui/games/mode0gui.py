import tkinter as tk 
from games.mode0.gameplay import Game

from games.utils.customElements import BtnDefault

class Mode0:
    def __init__(self,gameFrame):
        print( "launching game 0 -------------- ")
        self.gameFrame = gameFrame
        self.gameFrame.pack_propagate(0)

        

        # TODO : make custom fonts
        # definition of sizes and fonts
        self.gameFrame.label1 = tk.Label(self.gameFrame ) # for user instructions
        self.gameFrame.label1.config(font=("Courier", 12))
        self.gameFrame.label2 = tk.Label(self.gameFrame, padx=10, pady=10) # for "correct" or "incorrect"response
        self.gameFrame.label2.config(font=("Courier", 18))
        self.gameFrame.label3 = tk.Label(self.gameFrame) # for global score
        self.gameFrame.label3.config(font=("Courier", 30))
        self.gameFrame.btnSkip = BtnDefault(self.gameFrame, text= "SKIP >")

        # placement of differents labels
        self.placeElements()

        self.game = Game(self.gameFrame)
        

    def placeElements(self):
        self.gameFrame.rowconfigure((0,1,2,3,4, 5,6), weight=1)
        self.gameFrame.columnconfigure(0, weight=1)
        self.gameFrame.configure(bg="black") # should be invisible

        self.gameFrame.label1.grid(row=1,column=0, columnspan=1, sticky="NSEW")
        self.gameFrame.label3.grid(row=2,rowspan=2, column=0, columnspan=1, sticky="NSEW")
        self.gameFrame.label2.grid(row=4, rowspan=2, column=0, columnspan=1, sticky="EW")
        self.gameFrame.btnSkip.grid(row=6,column=0, columnspan=1, sticky="")


    def __del__(self):
        print("trying destroy")

    def activateListening(self):
        self.game.isListening=True

        

