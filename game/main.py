#!/usr/bin/python3
import tkinter as tk
from random import choice
import sys

# import odes
from mode0.mode0gui import Mode0
from mode1.mode1gui import Mode1
from mode2.mode2gui import Mode2
from mode3.mode3gui import Mode3
from mode4.mode4gui import Mode4

# import button styles
from utils.customElements import BtnMenu
from autoload import Autoload
from utils.audio import Sound

import env


class MainApplication(tk.Frame):
    # definition de la fenetre g)lobale
    def loadConfig(self):
        print("trying to load config")
    # location of config file
        # DEFAULT CONFIGURATION IF LOADING OF FILE FAILED
        default_config = {}
        default_config["default_mode"] = 0
        default_config["question_delay"] = 50
        default_config["difficulty"]=50
        default_config["times_each_transpose"]=4
        default_config["nb_of_transpose_before_change"]=4
        default_config["MIDI_interface"]=""
        default_config["midi_hotkey"]=50


        configFile = env.CONFIG_FILE
        configLabels=default_config.keys()
        print(configLabels)
        try:
            config={}
            with open(configFile, 'r') as file:
                for line in file:
                    for param in configLabels:
                        if line.find(param) != -1:
                            paramVal = line.split("=")[1].replace("\n","")
                            config[param]= paramVal
            print(config)

                    # maybe should test values
                    # loading in a dictionnary
                    # audio config trying to laod

        except:
            print("No config file found")
        
        return True





    def __init__(self, master, tag=""):
        # self.config = self.loadConfig()
        self.config=self.loadConfig()

        self.gameMode=0
        self.master=master
        
        # Main Frame
        self.master.title("RaspyKeys")
        self.master.geometry("320x480")
        self.frame=None
        self.master.body =None

        # print(self.config)


        # if(tag == "pi"): # to run at fullscreen if we get the "pi" tag
        #     self.master.attributes( "-fullscreen", True)
        #     self.master.buttonQuit = tk.Button(self.master, text="exit", command=lambda: self.master.quit())
        #     self.master.buttonQuit.pack(side=tk.BOTTOM, pady=(0,40))

        # keyboard shortcuts for dev
        self.master.bind("<Escape>", lambda event: self.master.quit())




        # toolbar
        self.master.toolbar = tk.Frame(self.master, bg=env.COL_TOOLBG, padx=10, pady=10)
        self.master.toolbar.pack(side=tk.TOP, fill=tk.X)

        self.master.body = tk.Frame(self.master, bg="orange")
        self.master.body.pack(expand=True, side=tk.TOP, fill=tk.BOTH)

        self.master.footer = tk.Frame(self.master, bg="grey")
        self.master.footer.pack(side=tk.BOTTOM, fill=tk.X) 
        

        # TODO: make a way to load last settigns. save automatically each time a change
        # toolbar buttons
        self.master.toolbar.columnconfigure((0,1,2,3), weight=1)
        # ///////// btn
        self.button1 = BtnMenu(self.master.toolbar, text="EarN")
        self.button1["command"] = lambda: self.new_window(0)
        self.button1.grid(row=0,column=0, columnspan=1, sticky="NSEW")
        # ///////// btn
        self.button2 = BtnMenu(self.master.toolbar, text="EarC")
        self.button2["command"] = lambda: self.new_window(1)
        self.button2.grid(row=0,column=1, columnspan=1, sticky="NSEW")
        # ///////// btn
        self.button3=BtnMenu(self.master.toolbar , text= "BkTr")
        self.button3["command"]=lambda: self.new_window(2)
        self.button3.grid(row=0,column=2, columnspan=1, sticky="NSEW")
        # ///////// btn
        self.button4 = BtnMenu(self.master.toolbar, text="Lick")
        self.button4["command"]= lambda: self.new_window(3)
        self.button4.grid(row=0,column=3, columnspan=1, sticky="NSEW")

        

        self.master.footer.columnconfigure((0,1,2), weight=1)
        self.button5 = BtnMenu(self.master.footer, text="Opts")
        self.button5["command"]= lambda: self.new_window(4)
        self.buttonMidiListen = BtnMenu(self.master.footer, text="MIDILis", command=self.toggleMidiListen)
        self.volumeSlider = tk.Scale(self.master.footer,  from_=0, to=100, orient=tk.HORIZONTAL,command=self.sliderMoved) 

        self.buttonMidiListen.grid(row=0, column=0, sticky="NSEW")
        self.volumeSlider.grid(row=0, column=1, sticky="NSEW")
        self.button5.grid(row=0, column=2, sticky="NSEW")

        # storage of the current Game Classe
        self.currentGameClass = None

        # initialization
        # Load default Screen
        self.new_window(0)
        # TODO make a way to retrieve the last open tab (config file load at startup ? )

    def sliderMoved(self, value):
        print("silder moved", value)
        mSound = Sound.setVolume(value) 
        

    
    # method to load a new game mode
    def new_window(self, intMode):
        try:
            pass
            self.master.body.destroy()
        except:
            print("no window to destroy, recreation ...", intMode)
        print("new window")
        # recreation of the body frame (middle frame)
        self.master.body=tk.Frame(self.master, bg="green")
        self.master.body.pack(side=tk.TOP, expand=True, fill=tk.BOTH)

        if intMode == 0:
            self.app= Mode0(self.master.body)
            # specific to mode0 bc in order to skip all midi notes during another mode
            self.app.activateListening()
        elif intMode == 1:
            self.app = Mode1(self.master.body)
            self.app.activateListening()
        elif intMode == 2:
            self.app = Mode2(self.master.body)
        elif intMode == 3:
            self.app = Mode3(self.master.body)
        elif intMode == 4:
            self.app = Mode4(self.master.body)
        else:
            return

    
    def toggleMidiListen(self):
        print("toggle listen mode")
        instance = Autoload().getInstance()
        instance.panic()
        instance.toggleListening()
        if instance.isListening == True:
            self.buttonMidiListen.config(text="MIDILis")
        else:
            self.buttonMidiListen.config(text="OFF")




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



