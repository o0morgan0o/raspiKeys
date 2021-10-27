import tkinter
import tkinter as tk
from src.game import env
from src.game.utils.customElements.buttons import *
from src.game.utils.customElements.scales import *
from enum import Enum

from PIL import Image, ImageTk


class GameNames(Enum):
    GAME_EAR_TRAINING_NOTE = "EarTraining_Note"
    GAME_EAR_TRAINING_CHORDS = "EarTraining_Chords"
    GAME_METRONOME = "Metronome"
    GAME_BACKTRACKS = "Backtracks"
    GAME_LICKS_PRACTISE = "LickPractise"
    GAME_OPTIONS = "Options"


class NavBarView:

    def __init__(self, master, parent: tkinter.Frame):
        self.parent = parent
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

        # ///////// btn
        PADDING_FOR_VERTICAL_SPACE = 60
        BUTTON_HEIGHT = 80
        self.button1 = BtnMenu(self.parent, image=self.mode0ImageBlack, height=BUTTON_HEIGHT)
        self.button1.config(command=lambda: self.master.new_window(GameNames.GAME_EAR_TRAINING_NOTE))
        self.button1.pack(fill=tk.BOTH, expand=True, pady=(PADDING_FOR_VERTICAL_SPACE, 0))
        # self.original_background = self.button1.cget("background")  # get original background color
        # ///////// btn
        self.button2 = BtnMenu(self.parent, image=self.mode1ImageBlack, height=BUTTON_HEIGHT)
        self.button2.config(command=lambda: self.master.new_window(GameNames.GAME_EAR_TRAINING_CHORDS))
        self.button2.pack(fill=tk.BOTH, expand=True)
        # self.button2["command"] = lambda: self.new_window(1)
        # ///////// btn
        self.button3 = BtnMenu(self.parent, image=self.mode2ImageBlack, height=BUTTON_HEIGHT)
        # self.button3.config(command=lambda: self.master.)
        self.button3.pack(fill=tk.BOTH, expand=True)
        # self.button3["command"] = lambda: self.new_window(2)
        # ///////// btn
        self.button4 = BtnMenu(self.parent, image=self.mode3ImageBlack, height=BUTTON_HEIGHT)
        self.button4.pack(fill=tk.BOTH, expand=True, pady=(0, PADDING_FOR_VERTICAL_SPACE))
        # self.button4["command"] = lambda: self.new_window(3)

    def highLightActiveMode(self, game_mode: GameNames):
        pass
        # self.button0.configure(background=self.original_background)
        # self.button1.configure(background=self.original_background)
        # self.button2.configure(background=self.original_background)
        # self.button3.configure(background=self.original_background)
        # self.button0["image"] = self.mode0ImageBlack
        # self.button1["image"] = self.mode1ImageBlack
        # self.button2["image"] = self.mode2ImageBlack
        # self.button3["image"] = self.mode3ImageBlack
        # self.button0["fg"] = "black"
        # self.button1["fg"] = "black"
        # self.button2["fg"] = "black"
        # self.button3["fg"] = "black"
        # if intMode == -1:
        #     self.button0["image"] = self.mode0ImageWhite
        #     self.button0["bg"] = "black"
        #     self.button0["activebackground"] = "black"
        # elif intMode == 0:
        #     self.button1["image"] = self.mode1ImageWhite
        #     self.button1["bg"] = "black"
        #     self.button1["activebackground"] = "black"
        # elif intMode == 1:
        #     self.button2["image"] = self.mode2ImageWhite
        #     self.button2["bg"] = "black"
        #     self.button2["activebackground"] = "black"
        # elif intMode == 2:
        #     self.button3["image"] = self.mode3ImageWhite
        #     self.button3["bg"] = "black"
        #     self.button3["activebackground"] = "black"
