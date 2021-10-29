import tkinter as tk

from src.game.Views.navbarView import GameNames
from src.game.utils.customElements.customElements import *
from src.game.ViewModels.FooterViewModel import FooterViewModel
from enum import Enum


class ViewStrings(Enum):
    STRING_LBL_AUDIO_VOLUME = "AUDIO VOLUME : "
    STRING_LBL_MIDI_VOLUME = "MIDI VOLUME : "
    STRING_BTN_OPTIONS = "Opts"


class FooterView:

    def __init__(self, master, game_frame: tk.Frame):
        self.master = master
        self.gameFrame = game_frame

        DEFAULT_PADDING = 10

        self.gameFrame.grid_rowconfigure(0, weight=0, )
        self.gameFrame.grid_rowconfigure(1, weight=1, )

        self.gameFrame.grid_columnconfigure(0, weight=1)
        self.gameFrame.grid_columnconfigure(1, weight=1, )
        self.gameFrame.grid_columnconfigure(2, weight=1, )
        self.gameFrame.grid_columnconfigure(3, weight=1, )
        self.gameFrame.grid_columnconfigure(4, weight=1, )

        self.lblAudioVolume = ttk.Label(self.gameFrame, text=ViewStrings.STRING_LBL_AUDIO_VOLUME, style=CustomStylesNames.STYLE_LBL_FULL.value, padding=0)
        self.lblAudioVolume.grid(row=0, column=0, columnspan=2, sticky=tk.NSEW)

        self.lblMidiVolume = ttk.Label(self.gameFrame, text=ViewStrings.STRING_LBL_MIDI_VOLUME, style=CustomStylesNames.STYLE_LBL_FULL.value, padding=0)
        self.lblMidiVolume.grid(row=0, column=3, columnspan=2, sticky=tk.NSEW)

        self.btnAudioMinus = CustomButton(self.gameFrame, text="-", style=CustomStylesNames.STYLE_BTN_FOOTER_PLUS_MINUS.value)
        self.btnAudioMinus.grid(row=1, column=0, sticky=tk.NSEW)
        self.btnAudioPlus = CustomButton(self.gameFrame, text="+", style=CustomStylesNames.STYLE_BTN_FOOTER_PLUS_MINUS.value)
        self.btnAudioPlus.grid(row=1, column=1, sticky=tk.NSEW)

        self.btnMidiMinus = CustomButton(self.gameFrame, text="-", style=CustomStylesNames.STYLE_BTN_FOOTER_PLUS_MINUS.value)
        self.btnMidiMinus.grid(row=1, column=3, sticky=tk.NSEW)
        self.btnMidiPlus = CustomButton(self.gameFrame, text="+", style=CustomStylesNames.STYLE_BTN_FOOTER_PLUS_MINUS.value)
        self.btnMidiPlus.grid(row=1, column=4, sticky=tk.NSEW)

        self.btnOptions = CustomButton(self.gameFrame, text=ViewStrings.STRING_BTN_OPTIONS.value, style=CustomStylesNames.STYLE_BTN_DARK.value)
        self.btnOptions.config(command=lambda: self.master.new_window(GameNames.GAME_OPTIONS))
        self.btnOptions.grid(row=0, column=2, rowspan=2, sticky=tk.NSEW, padx=DEFAULT_PADDING)
        # self.slAudioVolume = tk.Scale(self.gameFrame, from_=1, to=100, orient=tk.HORIZONTAL, showvalue=1)
        # self.slAudioVolume.grid(row=0, column=0, sticky=tk.NSEW)

        # self.slMidiVolume = tk.Scale(self.gameFrame, from_=1, to=127, orient=tk.HORIZONTAL, showvalue=1)
        # self.slMidiVolume.grid(row=0, column=1, sticky=tk.NSEW)

        # =========== CREATION OF THE VIEW_MODEL ====================
        self.viewModel = FooterViewModel(self)
        # ===========================================================
        self.btnAudioMinus.config(command=self.viewModel.audioMinusClicked)
        self.btnAudioPlus.config(command=self.viewModel.audioPlusClicked)
        self.btnMidiMinus.config(command=self.viewModel.midiMinusClicked)
        self.btnMidiPlus.config(command=self.viewModel.midiPlusClicked)

    def setUiInitialization(self, audio_volume: int, midi_volume: int):
        self.lblAudioVolume.config(text=ViewStrings.STRING_LBL_AUDIO_VOLUME.value + str(audio_volume))
        self.lblMidiVolume.config(text=ViewStrings.STRING_LBL_MIDI_VOLUME.value + str(midi_volume))

    def updateLblAudioVolume(self, audio_volume: int):
        self.lblAudioVolume.config(text=ViewStrings.STRING_LBL_AUDIO_VOLUME.value + str(audio_volume))

    def updateLblMidiVolume(self, midi_volume:int):
        self.lblMidiVolume.config(text=ViewStrings.STRING_LBL_MIDI_VOLUME.value + str(midi_volume))
