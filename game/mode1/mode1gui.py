import tkinter as tk
from mode1.gameplay import Game

from utils.customElements import BtnDefault

class Mode1:
    def __init__(self,gameFrame,config):
        print( "launching game 1 -------------- ")
        self.gameFrame = gameFrame
        self.gameFrame.pack_propagate(0)
        
        #self.gameFrame.button1 = tk.Button(self.gameFrame, text="game1", command=self)
        #self.gameFrame.button1.pack(side=tk.TOP)

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
        # canvas
        self.gameFrame.canvas = tk.Canvas(self.gameFrame, bg="black", width=200, height=80, highlightthickness=0)
        
        # placement of differents labels
        self.placeElements()

        self.game = Game(self.gameFrame, config)

    def placeElements(self):
        self.gameFrame.rowconfigure((0,1,2,3,4,5,6,7), weight=1)
        self.gameFrame.columnconfigure(0, weight=1)

        self.gameFrame.label1.grid(row=1, column=0, columnspan=1, sticky="NSEW")
        self.gameFrame.label3.grid(row=2, column=0, columnspan=1, sticky="NSEW")
        self.gameFrame.canvas.grid(row=3, rowspan=1, column=0, columnspan=1, sticky="NS")
        self.gameFrame.label2.grid(row=4, column=0, columnspan=1, sticky="NSEW")

        self.gameFrame.btnSkip.grid(row=6, column=0, columnspan=1, sticky="")
        

    def destroy(self):
        self.game.destroy()

    def __del__(self):
        print("trying destroy")

    def activateListening(self):
        self.game.isListening=True

