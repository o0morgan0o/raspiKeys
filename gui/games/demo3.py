import tkinter as tk 
from games.demo3dir.demo3 import Game
from games.utils.sounds import Sound

class Demo3:
    def __init__(self,parent):
        print( "launching game 3 -------------- ")
        self.parent = parent
        self.parent.pack_propagate(0)
        
        #self.parent.button1 = tk.Button(self.parent, text="game1", command=self)
        #self.parent.button1.pack(side=tk.TOP)

        # labels
        # definition of sizes and fonts
        self.btnPlay = tk.Button(text="play/Pause")
        self.btnPlay.place(relx = .5, rely = .7,anchor=tk.CENTER)

        self.btnRandom = tk.Button(text="random song")
        self.btnRandom.place(relx=.5, rely= .4, anchor=tk.CENTER)

        self.game = Game(self.parent)
        self.sound = Sound()
        self.sound.loadBacktracks()

        

    def update(self):
        #self.parent.update()
        print("updating UI")

    def destroy(self):
        self.game.destroy()

    def __del__(self):
        print("trying destroy")

    def activateListening(self):
        self.game.isListening=True

        

