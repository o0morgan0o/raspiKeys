import tkinter
import tkinter as tk
from src.game.modeOptions.gameplay import Game
from src.game.navbar.navbar import GameNames

from src.game.utils.customElements.buttons import *
from src.game.utils.customElements.labels import *
from src.game.utils.customElements.scales import *


class ModeOptions:
    def __init__(self, master, game_frame: tk.Frame, config: dict):
        print("launching game {}".format(GameNames.GAME_OPTIONS))
        self.game = None
        self.config = config
        self.master = master
        self.gameFrame = game_frame
        self.gameFrame.config(bg="black")

        DEFAULT_PADDING = 3

        self.gameFrame.grid_rowconfigure(0, weight=1, pad=DEFAULT_PADDING)
        self.gameFrame.grid_rowconfigure(1, weight=1, pad=DEFAULT_PADDING)
        self.gameFrame.grid_rowconfigure(2, weight=1, pad=DEFAULT_PADDING)
        self.gameFrame.grid_rowconfigure(3, weight=1, pad=DEFAULT_PADDING)
        self.gameFrame.grid_rowconfigure(4, weight=1, pad=DEFAULT_PADDING)

        self.gameFrame.grid_columnconfigure(0, weight=1, pad=DEFAULT_PADDING)
        self.gameFrame.grid_columnconfigure(1, weight=1, pad=DEFAULT_PADDING)

        current_row: int = 0

        self.section1 = MyLabel12(self.gameFrame, text="OPTIONS:")
        self.section1.grid(row=current_row, column=0, sticky=tk.NW)

        current_row += 1

        self.currentMidiIn = MyLabel12(self.gameFrame, text="MIDI in: (Current ...)")
        self.currentMidiIn.grid(row=current_row, column=0, sticky=tk.W, padx=20)

        self.currentMidiOut = MyLabel12(self.gameFrame, text="MIDI out: (Current ...)")
        self.currentMidiOut.grid(row=current_row, column=1, sticky=tk.W, padx=20)

        current_row += 1

        self.midiInListbox = tk.Listbox(self.gameFrame, selectmode='single')
        self.midiInListbox.grid(row=current_row, column=0, sticky=tk.NSEW, padx=20)

        self.midiOutListbox = tk.Listbox(self.gameFrame, selectmode='single')
        self.midiOutListbox.grid(row=current_row, column=1, sticky=tk.NSEW, padx=20)

        current_row +=1

        self.btnConfig = BtnDefault(self.gameFrame, text="Return Default")
        self.btnConfig.grid(row=current_row, column=1 ,sticky=tk.SE, padx=20)

        # self.label1_1 = MyLabel8(self.gameFrame, text="question Delay ms:\n(Affect modes EarN and EarC)")
        # self.label1_1.pack()

        # self.slider1_1 = SettingsScale(self.gameFrame, from_=10, to=200, orient=tk.HORIZONTAL,
        #                                command=self.updateConfig)
        # self.slider1_1.pack()

        # self.label1_2 = MyLabel8(self.gameFrame, text="Difficulty:\n(Affect mode EarN)")
        # self.label1_2.pack()
        #
        # self.slider1_2 = SettingsScale(self.gameFrame, from_=0, to=4, orient=tk.HORIZONTAL, command=self.updateConfig)
        # self.slider1_2.pack()

        # self.label2_1 = MyLabel8(self.gameFrame, text="Times each transpose:\n(Affect mode Lick)")
        # self.label2_1.pack()
        #
        # self.slider2_1 = SettingsScale(self.gameFrame, from_=1, to=8, orient=tk.HORIZONTAL, command=self.updateConfig)
        # self.slider2_1.pack()
        #
        # self.label2_2 = MyLabel8(self.gameFrame, text="Num of transposes / Lick:\n(Affect mode Lick)")
        # self.label2_2.pack()
        #
        # self.slider2_2 = SettingsScale(self.gameFrame, from_=1, to=8, orient=tk.HORIZONTAL, command=self.updateConfig)
        # self.slider2_2.pack()
        #
        # self.btnSaveDefault = BtnDefault(self.gameFrame, text="Save")
        # self.btnSaveDefault.pack()
        #
        # self.lblSaveAsDefault = MyLabel8(self.gameFrame, text="Save current settings\nas default:")
        # self.lblSaveAsDefault.pack()
        #
        # self.label3_1 = MyLabel8(self.gameFrame, text="Select Midi interface:")
        # self.label3_1.pack()

        # self.game = Game(self.gameFrame, self.gameFrame, config)

    def updateConfig(self, value):
        difficulty = self.slider1_2.get()
        times_each_transpose = self.slider2_1.get()
        nb_of_transpose_before_change = self.slider2_2.get()

        # self.parent.config(["default_mode"])=default_mode
        old_config = self.config
        old_config["default_mode"] = 1
        old_config["question_delay"] = question_delay
        old_config["difficulty"] = difficulty
        old_config["times_each_transpose"] = times_each_transpose
        old_config["nb_of_transpose_before_change"] = nb_of_transpose_before_change

        self.config = old_config
        # self.parent.config(["question_delay"])=question_delay

    # def placeElements(self):
    #
    #     # SECTION 1 - Ear Training Note
    #     self.gameFrameRight.section1.place(x=0, y=0, width=320, height=30)
    #     self.gameFrameRight.label1_1.place(x=0, y=30, width=175, height=60)
    #     self.gameFrameRight.slider1_1.place(x=175, y=30, width=145, height=60)
    #     self.gameFrameRight.label1_2.place(x=0, y=90, width=175, height=60)
    #     self.gameFrameRight.slider1_2.place(x=175, y=90, width=145, height=60)
    #
    #     # SECTION 2 - Practise licks
    #     self.gameFrameRight.label2_1.place(x=0, y=150, width=175, height=60)
    #     self.gameFrameRight.slider2_1.place(x=175, y=150, width=145, height=60)
    #     self.gameFrameRight.label2_2.place(x=0, y=210, width=175, height=60)
    #     self.gameFrameRight.slider2_2.place(x=175, y=210, width=145, height=60)
    #
    #     # SECTION 3- IkkkkkkjO
    #     self.gameFrameRight.label3_1.place(x=0, y=280, width=175, height=40)
    #     self.gameFrameRight.btnConfig.place(x=175, y=280, width=115, height=40)
    #
    #     # SECTION 4 - bouttons
    #     self.gameFrameRight.lblSaveAsDefault.place(x=0, y=320, width=175, height=40)
    #     self.gameFrameRight.btnSaveDefault.place(x=175, y=320, width=115, height=40)

    def update(self):
        print("updating UI")

    def destroy(self):
        if self.game is not None:
            self.game.destroy()

    def __del__(self):
        print("trying destroy")
