import tkinter as tk 
from games.demo0dir.demo0 import Game

class Demo0:
    def __init__(self,parent):
        print( "launching game 0 -------------- ")
        self.parent = parent
        self.parent.pack_propagate(0)
        
        #self.parent.button1 = tk.Button(self.parent, text="game1", command=self)
        #self.parent.button1.pack(side=tk.TOP)

        # labels
        # definition of sizes and fonts
        self.parent.label1 = tk.Label(self.parent,wraplength=200) # for user instructions
        self.parent.label1.config(font=("Courier", 12))
        self.parent.label2 = tk.Label(self.parent, padx=10, pady=10) # for "correct" or "incorrect"response
        self.parent.label2.config(font=("Courier", 18))
        self.parent.label2.configure(anchor= "center")
        self.parent.label3 = tk.Label(self.parent) # for global score
        self.parent.label3.config(font=("Courier", 30))

        # placement of differents labels
        # TODO : may be there is a better way to center this
        self.parent.label3.place(relx=.5, rely=.5, anchor=tk.CENTER)
        self.parent.label1.place(relx=.5, rely= .2, anchor=tk.CENTER)
        self.parent.label2.place(relx=.5, rely=.76, anchor=tk.CENTER)

        self.parent.btnListen = tk.Button(self.parent, text="ListenON")
        self.parent.btnListen.place(relx=0, rely = 1, anchor=tk.SW)

        self.parent.btnSkip = tk.Button(self.parent, text= "SKIP >")
        self.parent.btnSkip.place(relx=1, rely=1, anchor=tk.SE)


        self.game = Game(self.parent)
        

    def update(self):
        #self.parent.update()
        print("updating UI")

    def destroy(self):
        self.game.destroy()

    def __del__(self):
        print("trying destroy")

    def activateListening(self):
        self.game.isListening=True

        

