import tkinter as tk 
from mode0.gameplay import Game
from utils.customElements import BtnDefault
from utils.customElements import LblMode0

class Mode0:
    def __init__(self,gameFrame, config):
        print( "launching game 0 -------------- ")
        self.gameFrame = gameFrame
        self.gameFrame.pack_propagate(0)

        

        # TODO : make custom fonts
        # definition of sizes and fonts
        self.gameFrame.label1 = LblMode0(self.gameFrame) # for user instructions
        self.gameFrame.label1.config(font=("Courier", 20))
        self.gameFrame.label2 = LblMode0(self.gameFrame,padx=10, pady=10) # for "correct" or "incorrect"response
        self.gameFrame.label2.config(font=("Courier", 16))
        self.gameFrame.label3 = LblMode0(self.gameFrame,) # for global score
        self.gameFrame.label3.config(font=("Courier", 30))
        self.gameFrame.btnSkip = BtnDefault(self.gameFrame,text= "SKIP >")
        self.gameFrame.btnSkip.config(bg="black", fg="white", font=("Courier", 20))
        self.gameFrame.lblNote = LblMode0(self.gameFrame)
        self.gameFrame.lblNote.config(font=("Courier", 40, "bold"))
        self.gameFrame.lblNoteUser=LblMode0(self.gameFrame)
        self.gameFrame.lblNoteUser.config(font=("Courier", 40, "bold"))

        # placement of differents labels
        self.placeElements()

        self.game = Game(self.gameFrame, config)
        

    def placeElements(self):
        self.gameFrame.configure(bg="black") # should be invisible
#        self.gameFrame.rowconfigure((0,1,2,3,4, 5,6), weight=1)
#        self.gameFrame.columnconfigure(0, weight=1)
#
#        self.gameFrame.label1.grid(row=1,column=0, columnspan=1, sticky="NSEW")
#        self.gameFrame.label3.grid(row=2,rowspan=2, column=0, columnspan=1, sticky="NSEW")
#        self.gameFrame.label2.grid(row=4, rowspan=2, column=0, columnspan=1, sticky="EW")
#        self.gameFrame.btnSkip.grid(row=6,column=0, columnspan=1, sticky="")
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

        

