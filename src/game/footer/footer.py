import tkinter
import tkinter as tk
from src.game import env

from PIL import Image, ImageTk
from src.game.navbar.navbar import GameNames
from src.game.utils.customElements.buttons import *


class Footer:

    def __init__(self, master, parent: tkinter.Frame):
        self.master = master
        self.parent = parent

        PADDING_Y = 20
        PADDING_X = 14

        self.midiVolumeChangeToggle = BtnBlack20(self.parent, text="Midi", activebackground="black")
        self.midiVolumeChangeToggle.pack(side='left', fill=tk.BOTH, padx=(PADDING_X, PADDING_X / 2), pady=PADDING_Y)

        self.audioVolumeChangeToggle = BtnBlack20(self.parent, text="Audio", activebackground="black")
        self.audioVolumeChangeToggle.pack(side='left', fill=tk.BOTH, pady=PADDING_Y)

        self.btnVolumeMinus = BtnBlack20(self.parent, text="-", activebackground="black")
        self.btnVolumeMinus.pack(side='left', expand=True, fill=tk.BOTH, padx=(PADDING_X, 0), pady=PADDING_Y)
        # self.btnVolumeMinus.config(command=lambda: self.changeVolume(-.2), font=("Courier", 40))

        self.btnVolumePlus = BtnBlack20(self.parent, text="+", activebackground="black")
        self.btnVolumePlus.pack(side='left', expand=True, fill=tk.BOTH, padx=(0, PADDING_X), pady=PADDING_Y)
        # self.btnVolumePlus.config(command=lambda: self.changeVolume(.2), font=("Courier", 40))

        self.btnOptions = BtnBlack20(self.parent, text="Opts", activebackground="black")
        self.btnOptions.config(command=lambda: self.master.new_window(GameNames.GAME_OPTIONS))
        self.btnOptions.pack(side='right', fill=tk.BOTH, padx=(PADDING_X / 2, PADDING_X), pady=PADDING_Y)
