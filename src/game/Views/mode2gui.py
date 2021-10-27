
import tkinter as tk
from pathlib import Path
from glob import glob
import os

from src.game.mode2.gameplay import Game
from src.game import env

from src.game.utils.customElements.buttons import *
from src.game.utils.customElements.labels import *

from src.game.utils.customElements.buttons import BtnBlack20


class Mode2:
    def __init__(self, globalRoot, gameFrame, config, app):
        print("launching game 3 -------------- ")
        self.globalRoot = globalRoot
        self.gameFrame = gameFrame
        self.gameFrame.pack_propagate(0)
        self.gameFrame.config(bg=env.COL_BG)

        self.gameFrame.btnPlay = BtnBlack20(
            self.gameFrame, text="Play", activebackground="black")
        self.gameFrame.btnRandom = BtnBlack20(
            self.gameFrame, text="Random", activebackground="black")
        self.gameFrame.btnLick = BtnBlack20(
            self.gameFrame, text="Rec", wraplength="280", activebackground="black")

        # this canvas contains the red bar progression
        self.gameFrame.canvas = tk.Canvas(
            self.gameFrame, bd=0, highlightthickness=0)

        # getting all folders in user wav
        self.wav_folders = self.getAllWavFolders()
        print('found folders : ', self.wav_folders)

        # Metro btn
        self.gameFrame.btnMetro = BtnBlack20(self.gameFrame, text="Metro", activebackground="black")
        self.gameFrame.btnBpmMinus = BtnBlack20(self.gameFrame, text="-", activebackground="black")
        self.gameFrame.btnBpmPlus = BtnBlack20(self.gameFrame, text="+", activebackground="black")

        self.gameFrame.btnSwitchPage = BtnBlack20(self.gameFrame, text=">>", activebackground="black")

        self.gameFrame.wav_buttons = []
        for folder in self.wav_folders:
            all_files_in_folder = glob(env.PROCESSED_WAV_FOLDER + '/' + folder + '/*')
            button_text = folder + "\n(" + str(len(all_files_in_folder)) + ")"
            self.gameFrame.wav_buttons.append(BtnBlack20(self.gameFrame, text=button_text, activebackground="black"))

        self.placeElements()
        self.game = Game(self.globalRoot, self.gameFrame, config, app)

    @staticmethod
    def getAllWavFolders():
        raw_wav_folders = glob(env.PROCESSED_WAV_FOLDER + '/*/')
        wav_folders = []
        # We want to extract just the names of the folders for the display
        for folder in raw_wav_folders:
            # check if we are running on windows(dev) or linux(prod)
            if os.name == 'nt':
                wav_folders.append(folder.split('\\')[-2])
            elif os.name == 'posix':
                wav_folders.append(folder.split('/')[-2])
            else:
                raise Exception("Unknown operating system")

        return wav_folders

    def placeElements(self):
        yplacement = 20
        self.gameFrame.btnMetro.place(x=10, y=yplacement, width=100, height=80)
        self.gameFrame.btnBpmMinus.place(x=130, y=yplacement, width=90, height=80)
        self.gameFrame.btnBpmPlus.place(x=220, y=yplacement, width=90, height=80)

        counter = 0
        for button in self.gameFrame.wav_buttons:
            if counter == 0:
                button.place(x=10, y=120, width=140, height=80)
            elif counter == 1:
                button.place(x=170, y=120, width=140, height=80)
            elif counter == 2:
                button.place(x=10, y=220, width=140, height=80)
            elif counter >= 3:
                button.place(x=-200, y=0, width=140, height=80)
            counter += 1
        self.gameFrame.btnSwitchPage.place(x=170, y=220, width=140, height=80)

        self.gameFrame.canvas.place(x=0, y=320, width=320, height=10)

    # def destroy(self):
    # self.game.destroy()

    def __del__(self):
        self.destroy()

    def activateListening(self):
        self.game.isListening = True

    def destroy(self):
        print("trying destroy mode 2")
        self.game.destroy()
        del self
        pass
