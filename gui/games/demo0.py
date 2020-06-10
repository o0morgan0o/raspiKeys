import tkinter as tk 
from games.demo0C.test import Game

class Demo0:
    def __init__(self,parent):
        print( "launching game 0 -------------- ")
        self.parent = parent
        self.parent.pack_propagate(0)
        
        #self.parent.button1 = tk.Button(self.parent, text="game1", command=self)
        #self.parent.button1.pack(side=tk.TOP)

        # labels
        self.parent.label1 = tk.Label(self.parent, text="Score :")
        self.parent.label2 = tk.Label(self.parent, text="Listen !")
        self.parent.label1.pack(side=tk.TOP)
        self.parent.label2.pack(side=tk.TOP)


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

        

