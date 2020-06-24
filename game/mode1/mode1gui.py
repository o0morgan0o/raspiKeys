import tkinter as tk
from mode1.gameplay import Game

from utils.customElements import BtnDefault

class Mode1:
    def __init__(self,gameFrame,config):
        print( "launching game 1 -------------- ")
        self.gameFrame = gameFrame
        self.gameFrame.pack_propagate(0)
        

        # labels
        # definition of sizes and fonts
        self.gameFrame.label1 = tk.Label(self.gameFrame,wraplength=200) # for user instructions
        self.gameFrame.label1.config(font=("Courier", 12))
        self.gameFrame.label2 = tk.Label(self.gameFrame, padx=10, pady=10) # for "correct" or "incorrect"response
        self.gameFrame.label2.config(font=("Courier", 18))
        self.gameFrame.label2.configure(anchor= "center")
        self.gameFrame.label3 = tk.Label(self.gameFrame) # for global score
        self.gameFrame.label3.config(font=("Courier", 30))
        self.gameFrame.btnSkip = BtnDefault(self.gameFrame, text= "SKIP >")
        self.gameFrame.btnSkip.config(bg="black", fg="white")
        self.gameFrame.lblNote= tk.Label(self.gameFrame, text="")
        self.gameFrame.lblNote.config(font=("Courier", 30), bg="black", fg="white")
        # canvas
        self.gameFrame.canvas = tk.Canvas(self.gameFrame, bg="black", width=200, height=70, highlightthickness=0)
        
        # placement of differents labels
        self.placeElements()

        self.game = Game(self.gameFrame, config)

    def placeElements(self):

#        self.gameFrame.label1.grid(row=1, column=0, columnspan=1, sticky="NSEW")
#        self.gameFrame.label3.grid(row=2, column=0, columnspan=1, sticky="NSEW")
#        self.gameFrame.canvas.grid(row=3, rowspan=1, column=0, columnspan=1, sticky="NS")
#        self.gameFrame.label2.grid(row=4, column=0, columnspan=1, sticky="NSEW")
#
#        self.gameFrame.btnSkip.grid(row=6, column=0, columnspan=1, sticky="")

        self.gameFrame.label1.place(x=0, y=10, width=320,height=50)
        self.gameFrame.label3.place(x=0,y=65,width=320,height=50)
        self.gameFrame.lblNote.place(x=0,y=110, width=320, height=80)
        self.gameFrame.canvas.place(x=60, y=190, width=200, height=70)
        self.gameFrame.btnSkip.place(x=90,y=280,width=140,height=60)
        

    def destroy(self):
        self.game.destroy()

    def __del__(self):
        print("trying destroy")

    def activateListening(self):
        self.game.isListening=True

