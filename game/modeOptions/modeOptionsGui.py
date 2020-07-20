import tkinter as tk
from game.modeOptions.gameplay import Game

from game.utils.customElements.buttons import *
from game.utils.customElements.labels import *
from game.utils.customElements.scales import *


class ModeOptions:
    def __init__(self, gameFrame, config, volumeSlider, parent):
        self.parent = parent
        print("launching game 4 -------------- ")
        self.gameFrame = gameFrame
        self.gameFrame.pack_propagate(0)
        self.gameFrame.config(bg="black")

        self.gameFrame.section1 = MyLabel12(self.gameFrame, text="OPTIONS:")
        self.gameFrame.label1_1 = MyLabel8(self.gameFrame, text="question Delay ms:\n(Affect modes EarN and EarC)")
        self.gameFrame.slider1_1 = SettingsScale(self.gameFrame, from_=10, to=200, orient=tk.HORIZONTAL, command=self.updateConfig)
        self.gameFrame.label1_2 = MyLabel8(self.gameFrame, text="Difficulty:\n(Affect mode EarN)")
        self.gameFrame.slider1_2 = SettingsScale(self.gameFrame, from_=0, to=4, orient=tk.HORIZONTAL, command=self.updateConfig)
        #
        self.gameFrame.label2_1 = MyLabel8(self.gameFrame, text="Times each transpose:\n(Affect mode Lick)")
        self.gameFrame.slider2_1 = SettingsScale(self.gameFrame, from_=1, to=8, orient=tk.HORIZONTAL, command=self.updateConfig)
        self.gameFrame.label2_2 = MyLabel8(self.gameFrame, text="Num of transposes / Lick:\n(Affect mode Lick)")
        self.gameFrame.slider2_2 = SettingsScale(self.gameFrame, from_=1, to=8, orient=tk.HORIZONTAL, command=self.updateConfig)
        #
        self.gameFrame.btnSaveDefault = BtnDefault(self.gameFrame, text="Save")
        self.gameFrame.lblSaveAsDefault = MyLabel8(self.gameFrame, text="Save current settings\nas default:")

        self.gameFrame.label3_1 = MyLabel8(self.gameFrame, text="Select Midi interface:")
        self.gameFrame.btnConfig = BtnDefault(self.gameFrame, text="Select MIDI")

        self.placeElements()

        self.game = Game(self.gameFrame, config, volumeSlider)

    def updateConfig(self, value):
        difficulty = self.gameFrame.slider1_2.get()
        times_each_transpose = self.gameFrame.slider2_1.get()
        nb_of_transpose_before_change = self.gameFrame.slider2_2.get()
        print(self.parent.config)

        # self.parent.config(["default_mode"])=default_mode
        oldconfig = self.parent.config
        oldconfig["default_mode"] = 1
        oldconfig["question_delay"] = question_delay
        oldconfig["difficulty"] = difficulty
        oldconfig["times_each_transpose"] = times_each_transpose
        oldconfig["nb_of_transpose_before_change"] = nb_of_transpose_before_change

        self.parent.config = oldconfig
        # self.parent.config(["question_delay"])=question_delay

    def placeElements(self):

        # SECTION 1 - Ear Training Note
        self.gameFrame.section1.place(x=0, y=0, width=320, height=30)
        self.gameFrame.label1_1.place(x=0, y=30, width=175, height=60)
        self.gameFrame.slider1_1.place(x=175, y=30, width=145, height=60)
        self.gameFrame.label1_2.place(x=0, y=90, width=175, height=60)
        self.gameFrame.slider1_2.place(x=175, y=90, width=145, height=60)

        # SECTION 2 - Practise licks
        self.gameFrame.label2_1.place(x=0, y=150, width=175, height=60)
        self.gameFrame.slider2_1.place(x=175, y=150, width=145, height=60)
        self.gameFrame.label2_2.place(x=0, y=210, width=175, height=60)
        self.gameFrame.slider2_2.place(x=175, y=210, width=145, height=60)

        # SECTION 3- IkkkkkkjO
        self.gameFrame.label3_1.place(x=0, y=280, width=175, height=40)
        self.gameFrame.btnConfig.place(x=175, y=280, width=115, height=40)

        # SECTION 4 - bouttons
        self.gameFrame.lblSaveAsDefault.place(x=0, y=320, width=175, height=40)
        self.gameFrame.btnSaveDefault.place(x=175, y=320, width=115, height=40)

    def update(self):
        print("updating UI")

    def destroy(self):
        self.game.destroy()

    def __del__(self):
        print("trying destroy")

