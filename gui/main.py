#!/usr/bin/python3
import tkinter as tk
from random import choice
import sys

# import gamemodes
from games.mode0gui import Mode0
from games.mode1gui import Mode1
from games.mode3gui import Mode3
from games.mode4gui import Mode4
from games.mode5gui import Mode5

# import button styles
from games.utils.customElements import BtnMenu



class MainApplication(tk.Frame):
    # definition de la fenetre globale
    def __init__(self, master, tag=""):
        self.colors=['red', 'green', 'yellow']
        self.gameMode=0
        self.master=master
        
        # Main Frame
        self.master.title("RaspyKeys")
        self.master.geometry("320x480")
        self.master["bg"]="black"
        self.frame=tk.Frame(self.master)
        if(tag == "pi"): # to run at fullscreen if we get the "pi" tag
            self.master.attributes( "-fullscreen", True)
            self.master.buttonQuit = tk.Button(self.master, text="exit", command=lambda: self.master.quit())
            self.master.buttonQuit.pack(side=tk.BOTTOM, pady=(0,40))

        # keyboard shortcuts for dev
        self.master.bind("<Escape>", lambda event: self.master.quit())

        # toolbar
        self.master.toolbar = tk.Frame(self.master, bg="black", padx=0, pady=20)
        self.master.toolbar.pack(anchor=tk.CENTER, fill=tk.X)


        # TODO: make a way to load last settigns. save automatically each time a change
        # toolbar buttons
        # ///////// btn
        self.master.button1 = BtnMenu(self.master.toolbar, text="EarN")
        self.master.button1["command"] = lambda: self.toggleMode(0)
        self.master.button1.pack(side=tk.LEFT, padx=(10,0))
        # ///////// btn
        self.master.button2 = BtnMenu(self.master.toolbar, text="EarC")
        self.master.button2["command"] = lambda: self.toggleMode(1)
        self.master.button2.pack(side=tk.LEFT,)
        # ///////// btn
        # self.master.button3 =NavButton(self.master.toolbar, text="Metr")
        # self.master.button3["command"]=lambda: self.toggleMode(2)
        # self.master.button3.pack(side=tk.LEFT, )
        # ///////// btn
        self.master.button4=BtnMenu(self.master.toolbar , text= "BkTr")
        self.master.button4["command"]=lambda: self.toggleMode(3)
        self.master.button4.pack(side=tk.LEFT, )
        # ///////// btn
        self.master.button5 = BtnMenu(self.master.toolbar, text="Lick")
        self.master.button5["command"]= lambda: self.toggleMode(4)
        self.master.button5.pack(side=tk.LEFT)
        # ///////// btn
        self.master.button6 = BtnMenu(self.master.toolbar, text="Opts")
        self.master.button6["command"]= lambda: self.toggleMode(5)
        self.master.button6.pack(side=tk.LEFT)



        # Populate the GUI
        #self.button1= tk.Button(self.frame, text="hello", command=self.new_window)
        #self.button1.pack()

        #self.frame.pack()
        self.frame.place(relx=.5, rely=.5, anchor=tk.CENTER)

        # storage of the current Game Classe
        self.currentGameClass = None

        # initialization
        # determine the default game mode at the launch
        # TODO make a way to retrieve the last open tab (config file load at startup ? )
        self.new_window(3)

    
    # method to load a new game mode
    def new_window(self, intMode):
        self.frame.pack_propagate(0)
        self.frame.gameFrame = tk.Frame(self.master)
        if intMode == 0:
            self.app = Mode0(self.frame.gameFrame)
            # specific to mode0 bc in order to skip all midi notes during another mode
            self.app.activateListening()
        elif intMode == 1:
            self.app = Mode1(self.frame.gameFrame)
            self.app.activateListening()

        elif intMode == 3:
            self.app = Mode3(self.frame.gameFrame)

        elif intMode == 4:
            self.app = Mode4(self.frame.gameFrame)
        
        elif intMode == 5:
            self.app = Mode5(self.frame.gameFrame)

        else:
            return

        self.frame.gameFrame.pack(expand=True , fill=tk.BOTH, padx=0, pady=20)

    def destroyExistingFrame(self):
        self.frame.gameFrame.pack_forget()
        self.frame.gameFrame.destroy()
        self.app.destroy()
        del self.app



    def toggleMode(self, intMode):
        #destroy the existing gameFrame
        self.destroyExistingFrame()
        
        self.new_window(intMode)



if __name__ == "__main__":
    if len(sys.argv) > 1:
        tag= sys.argv[1].split("=")[1]
    else:
        tag=""
        print("run with no arguments...")
    root=tk.Tk()
    root.config(cursor="dot")
    MainApplication(root, tag)
    root.mainloop()



