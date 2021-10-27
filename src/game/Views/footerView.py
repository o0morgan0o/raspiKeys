import tkinter as tk

from src.game.Views.navbarView import GameNames
from src.game.utils.customElements.buttons import *
from src.game.ViewModels.FooterViewModel import FooterViewModel


class FooterView:

    def __init__(self, master, game_frame: tk.Frame):
        self.master = master
        self.gameFrame = game_frame

        DEFAULT_PADDING = 10

        self.gameFrame.grid_rowconfigure(0, weight=1, pad=DEFAULT_PADDING)
        self.gameFrame.grid_columnconfigure(0, weight=1, pad=DEFAULT_PADDING)
        self.gameFrame.grid_columnconfigure(1, weight=1, pad=DEFAULT_PADDING)
        self.gameFrame.grid_columnconfigure(2, weight=1, pad=DEFAULT_PADDING)

        self.slAudioVolume = tk.Scale(self.gameFrame, from_=1, to=100, orient=tk.HORIZONTAL, showvalue=1)
        self.slAudioVolume.grid(row=0, column=0, sticky=tk.NSEW)

        self.slMidiVolume = tk.Scale(self.gameFrame, from_=1, to=127, orient=tk.HORIZONTAL, showvalue=1)
        self.slMidiVolume.grid(row=0, column=1, sticky=tk.NSEW)

        self.btnOptions = BtnBlack20(self.gameFrame, text="Opts", activebackground="black")
        self.btnOptions.config(command=lambda: self.master.new_window(GameNames.GAME_OPTIONS))
        self.btnOptions.grid(row=0, column=2)

        self.viewModel = FooterViewModel(self)
        self.slAudioVolume.bind("<ButtonRelease-1>", self.viewModel.updateAudioVolumeCallback)
        self.slMidiVolume.bind("<ButtonRelease-1>" ,self.viewModel.updateMidiVolumeCallback)


