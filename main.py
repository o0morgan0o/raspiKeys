#!/usr/bin/python3
import tkinter as tk
from random import choice
import sys

from game.utils.images import create_image
from PIL import Image, ImageTk

# import odes
from game.mode0.mode0gui import Mode0
from game.mode1.mode1gui import Mode1
from game.mode2.mode2gui import Mode2
from game.mode3.mode3gui import Mode3
from game.modeOptions.modeOptionsGui import ModeOptions

# import button styles
from game.utils.customElements.buttons import *
from game.utils.customElements.scales import *
from game.autoload import Autoload
from game.utils.audio import Audio
from game.utils.utilFunctions import loadConfig

from game import env


class MainApplication(tk.Frame):
    # definition de la fenetre g)lobale

    def __init__(self, master, tag=""):

        self.config = loadConfig()
        self.gameMode = int(self.config["default_mode"])
        self.master = master

        # images
        self.volumeImage = ImageTk.PhotoImage(Image.open(env.VOLUME_IMAGE))
        self.configImage = ImageTk.PhotoImage(Image.open(env.SETTINGS_IMAGE))
        self.mode0ImageBlack = ImageTk.PhotoImage(Image.open(env.MODE0_IMAGE_BLACK))
        self.mode1ImageBlack = ImageTk.PhotoImage(Image.open(env.MODE1_IMAGE_BLACK))
        self.mode2ImageBlack = ImageTk.PhotoImage(Image.open(env.MODE2_IMAGE_BLACK))
        self.mode3ImageBlack = ImageTk.PhotoImage(Image.open(env.MODE3_IMAGE_BLACK))
        self.mode0ImageWhite = ImageTk.PhotoImage(Image.open(env.MODE0_IMAGE_WHITE))
        self.mode1ImageWhite = ImageTk.PhotoImage(Image.open(env.MODE1_IMAGE_WHITE))
        self.mode2ImageWhite = ImageTk.PhotoImage(Image.open(env.MODE2_IMAGE_WHITE))
        self.mode3ImageWhite = ImageTk.PhotoImage(Image.open(env.MODE3_IMAGE_WHITE))

        # Main Frame
        self.master.title("RaspyKeys")
        self.master.geometry("320x480")
        self.frame = None
        self.master.body = None

        # if(tag == "pi"): # to run at fullscreen if we get the "pi" tag
        # self.master.attributes( "-fullscreen", True)

        # keyboard shortcuts for dev
        self.master.bind("<Escape>", lambda event: self.master.quit())

        # toolbar
        self.master.toolbar = tk.Frame(self.master, bg=env.COL_TOOLBG,)
        self.master.toolbar.place(x=0, y=0, width=320, height=60)
        #        self.master.toolbar.pack(side=tk.TOP, fill=tk.X)

        self.master.body = tk.Frame(self.master, bg="orange")
        self.master.footer = tk.Frame(self.master, bg="yellow")
        self.master.footer.place(x=0, y=430, width=320, height=50)

        # ///////// btn
        self.button1 = BtnMenu(self.master.toolbar, image=self.mode0ImageBlack)
        self.button1.config(command=lambda: self.new_window(0))
        self.button1.place(x=0, y=0, width=80, height=60)
        self.original_background = self.button1.cget("background")  # get original background color
        # ///////// btn
        self.button2 = BtnMenu(self.master.toolbar, image=self.mode1ImageBlack)
        self.button2["command"] = lambda: self.new_window(1)
        self.button2.place(x=80, y=0, width=80, height=60)
        # ///////// btn
        self.button3 = BtnMenu(self.master.toolbar, image=self.mode2ImageBlack)
        self.button3["command"] = lambda: self.new_window(2)
        self.button3.place(x=160, y=0, width=80, height=60)
        # ///////// btn
        self.button4 = BtnMenu(self.master.toolbar, image=self.mode3ImageBlack)
        self.button4["command"] = lambda: self.new_window(3)
        self.button4.place(x=240, y=0, width=80, height=60)

        self.master.footer.columnconfigure((0, 1, 2), weight=1)
        self.button5 = BtnMenu(self.master.footer, text="Opts")
        self.button5["command"] = lambda: self.new_window(4)
        self.button5.place(x=240, y=0, width=80, height=50)

        self.buttonVolume = BtnMenu(self.master.footer, image=self.volumeImage)
        # self.buttonVolume.config(background="grey", foreground="black")
        self.buttonVolume.place(x=0, y=0, width=80, height=50)

        self.volumeSlider = VolumeSliderScale(self.master.footer, command=self.sliderMoved)
        self.volumeSlider.place(x=80, y=0, width=160, height=80)

        # load default volume
        volume = int(self.config["volume"])
        self.volumeSlider.set(volume)

        # storage of the current Game Classe
        self.currentGameClass = None

        # initialization
        # Load default Screen
        self.new_window(self.gameMode)
        # TODO make a way to retrieve the last open tab (config file load at startup ? )

    def sliderMoved(self, value):
        mSound = Audio.setVolume(None, value)

    # method to load a new game mode
    def new_window(self, intMode):
        self.audioInstance = Autoload().getInstanceAudio()  # in order to create the first instance of audio file
        try:
            self.master.body.destroy()
            del self.app
        except:
            print("no window to destroy, recreation ...", intMode)
        print("Creating new window")
        # recreation of the body frame (middle frame)
        self.master.body = tk.Frame(self.master, bg="green")
        self.master.body.place(x=0, y=60, width=320, height=370)

        try:
            del self.app
            print("Should be empty  : ", self.app)
        except:
            pass

        if intMode == 0:
            self.app = Mode0(self.master.body, self.config)
            # specific to mode0 bc in order to skip all midi notes during another mode
            self.app.activateListening()
        elif intMode == 1:
            self.app = Mode1(self.master.body, self.config)
            self.app.activateListening()
        elif intMode == 2:
            self.app = Mode2(self.master, self.master.body, self.config, self)
        elif intMode == 3:
            self.app = Mode3(self.master, self.master.body, self.config, self)
        elif intMode == 4:
            self.app = ModeOptions(self.master.body, self.config, self.volumeSlider, self)
        else:
            return

        self.highLightActiveMode(intMode)

    def highLightActiveMode(self, intMode):
        self.button1.configure(background=self.original_background)
        self.button2.configure(background=self.original_background)
        self.button3.configure(background=self.original_background)
        self.button4.configure(background=self.original_background)
        self.button1["image"] = self.mode0ImageBlack
        self.button2["image"] = self.mode1ImageBlack
        self.button3["image"] = self.mode2ImageBlack
        self.button4["image"] = self.mode3ImageBlack
        self.button1["fg"] = "black"
        self.button2["fg"] = "black"
        self.button3["fg"] = "black"
        self.button4["fg"] = "black"
        if intMode == 0:
            self.button1["image"] = self.mode0ImageWhite
            self.button1["bg"] = "black"
            self.button1["activebackground"] = "black"
        elif intMode == 1:
            self.button2["image"] = self.mode1ImageWhite
            self.button2["bg"] = "black"
            self.button2["activebackground"] = "black"
        elif intMode == 2:
            self.button3["image"] = self.mode2ImageWhite
            self.button3["bg"] = "black"
            self.button3["activebackground"] = "black"
        elif intMode == 3:
            self.button4["image"] = self.mode3ImageWhite
            self.button4["bg"] = "black"
            self.button4["activebackground"] = "black"

    def toggleMidiListen(self):
        instance = Autoload().getInstance()
        instance.panic()
        instance.toggleListening()
        # if instance.isListening == True:
        # self.buttonMidiListen.config(background="grey", text="MIDILis")
        # else:
        # self.buttonMidiListen.config(background="red", text="OFF")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        tag = sys.argv[1].split("=")[1]
    else:
        tag = ""
        print("Program runned with no arguments...")
    root = tk.Tk()
    root.config(cursor="none")
    MainApplication(root, tag)

    root.mainloop()
