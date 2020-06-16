import tkinter as tk 
from games.demo3dir.demo3 import Game



class Demo3:
    def __init__(self,parent):
        print( "launching game 3 -------------- ")
        self.parent = parent
        self.parent.pack_propagate(0)
        

        self.btnPlay = tk.Button(text="play/Pause", width=14, height=5)
        self.btnPlay.place(relx = .08, rely = .92,anchor=tk.SW)

        self.btnRandom = tk.Button(text="random song", width=14, height=5)
        self.btnRandom.place(relx=.92, rely= .92, anchor=tk.SE)

        self.randTrack0 = tk.Button(text="", width=20 , height= 2)
        self.randTrack0.place(relx=.5, rely=.1+ .1, anchor=tk.N)
        self.randTrack1 = tk.Button(text="", width=20, height=2)
        self.randTrack1.place(relx=.5, rely=.1+ 2*.1, anchor=tk.N)
        self.randTrack2 = tk.Button(text="", width=20, height=2)
        self.randTrack2.place(relx=.5, rely=.1+ 3*.1, anchor=tk.N)
        self.randTrack3 = tk.Button(text="", width=20, height=2)
        self.randTrack3.place(relx=.5, rely=.1+ 4*.1, anchor=tk.N)

        self.labelCurrent= tk.Label(text="aaaa")
        self.labelCurrent.place(relx = .5, rely = .62, anchor = tk.N)



        self.game = Game(self)



        

    def update(self):
        print("updating UI")

    def destroy(self):
        self.game.destroy()

    def __del__(self):
        print("trying destroy")

    def activateListening(self):
        self.game.isListening=True

        

