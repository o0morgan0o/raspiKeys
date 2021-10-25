import tkinter as Tk
from src.game import env
from src.game.mode0.gameplay import Game
from src.game.navbar.navbar import GameNames

from src.game.utils.customElements.buttons import *
from src.game.utils.customElements.labels import *
from src.game.utils.customElements.scales import SettingsScale
from src.game.utils.utilFunctions import *


class Mode0:
    def __init__(self, master, game_frame: tk.Frame, config: dict):
        print("launching game {}".format(GameNames.GAME_EAR_TRAINING_NOTE))
        self.master = master
        self.game = None
        self.gameFrame = game_frame

        DEFAULT_PADDING = 3
        current_row = 0

        self.gameFrame.grid_rowconfigure(0, weight=1, pad=DEFAULT_PADDING)
        self.gameFrame.grid_rowconfigure(1, weight=1, pad=DEFAULT_PADDING)
        self.gameFrame.grid_rowconfigure(2, weight=1, pad=DEFAULT_PADDING)
        self.gameFrame.grid_columnconfigure(0, weight=1, pad=DEFAULT_PADDING)
        self.gameFrame.grid_columnconfigure(1, weight=1, pad=DEFAULT_PADDING)

        self.slInterval = tk.Scale(self.gameFrame, from_=3, to=18, orient=tk.HORIZONTAL, width=40, label="Interval Max", showvalue=0)  # command=self.updateConfig)
        self.slInterval.grid(row=0, column=0, sticky=tk.EW, padx=(10, 10))

        self.slDelay = tk.Scale(self.gameFrame, from_=3, to=18, orient=tk.HORIZONTAL, width=40, label="Note Delay" ,showvalue=0)  # command=self.updateConfig)
        self.slDelay.grid(row=0, column=1, sticky=tk.EW, padx=(10,10))

        # self.slInterval.set(int(config["mode0IntervalOffset"]))
        # self.slInterval.config(showvalue=0)

        self.pickNote = MyLabel18(self.gameFrame)  # for user instructions
        self.pickNote.config(font=("Courier", 24), text="pickNote")
        self.pickNote.grid(row=current_row, columnspan=2)

        current_row += 1

        self.lblNote = MyLabel40(self.gameFrame, justify="right")
        self.lblNote.config(font=("Courier", 120, "bold"), text="?")
        self.lblNote.grid(row=current_row, column=0, sticky=tk.E, padx=(0, 12))

        self.lblNoteUser = MyLabel40(self.gameFrame)
        self.lblNoteUser.config(font=("Courier", 120, "bold"), text="A", justify="left")
        self.lblNoteUser.grid(row=current_row, column=1, sticky=tk.W, padx=(12, 0))

        current_row += 1

        self.result = MyLabel18(self.gameFrame, padx=10, pady=10)  # for "correct" or "incorrect"response
        self.result.config(font=("Courier", 18, "bold"), text="Correct / Incorrect")
        self.result.grid(row=current_row, columnspan=2)

        current_row += 1

        self.btnSkip = BtnBlack20(self.gameFrame, text="SKIP >")
        self.btnSkip.config(bd=0, highlightthickness=0)
        self.btnSkip.grid(row=current_row, columnspan=2)

        current_row += 1

        self.score = MyLabel30(self.gameFrame, )  # for global score
        self.score.config(font=("Courier", 10, "bold"), text="SCORE")
        # self.score.grid(row=2, sticky=tk.SW)
        self.score.grid(row=current_row, columnspan=2)
        current_row += 1

        #
        # self.lblInterval = MyLabel18(self.gameFrame)
        # self.lblInterval.config(font=("Courier", 12), text="Interval section:")
        # self.lblInterval.pack(fill=tk.BOTH)
        #
        # self.lblMidiVolume = MyLabel18(self.gameFrame)
        # self.lblMidiVolume.config(font=("Courier", 12), text="Midi Volume:")
        # self.lblMidiVolume.pack(fill=tk.BOTH)

        #
        # self.gameFrame.slMidiVolume = SettingsScale(self.gameFrame, from_=1, to=127, orient=tk.HORIZONTAL)  # command=self.updateConfig)
        # self.gameFrame.slMidiVolume.set(int(config["mode0MidiVolume"]))
        # self.gameFrame.slMidiVolume.config(showvalue=0)
        # # self.gameFrameLeft.slMidiVolume.set()
        #

        # placement of differents labels
        # self.placeElements()

        # self.game = Game(self.gameFrameLeft, self.gameFrameRight, config)

    def placeElements(self):
        pass
        # self.gameFrame.lblInterval.pack()
        # yoffset = 160
        # self.gameFrameLeft.lblInterval.place(x=20, y=yoffset, width=env.LEFT_SCREEN_W - 40, height=30)
        # yoffset += 40
        # self.gameFrameLeft.slInterval.place(x=20, y=yoffset, width=env.LEFT_SCREEN_W - 40, height=30)
        # yoffset += 40
        # self.gameFrameLeft.lblMidiVolume.place(x=20, y=yoffset, width=env.LEFT_SCREEN_W - 40, height=30)
        # yoffset += 40
        # self.gameFrameLeft.slMidiVolume.place(x=20, y=yoffset, width=env.LEFT_SCREEN_W - 40, height=30)

        # self.gameFrameRight.configure(bg="red") # should be invisible
        # self.gameFrameRight.result.place(x=0, y=0,width=env.RIGHT_SCREEN_W,height=80)

        # self.gameFrameRight.pickNote.place(x=0, y=30, width=env.RIGHT_SCREEN_W, height=40)
        # self.gameFrameRight.lblNoteUser.place(x=0, y=140, width=env.RIGHT_SCREEN_W)
        # self.gameFrameRight.lblNote.place(x=0, y=140, width=env.RIGHT_SCREEN_W)
        # self.gameFrameRight.lblNote.lift()
        # self.gameFrameRight.btnSkip.place(x=0, y=350, width=env.RIGHT_SCREEN_W, height=60)
        # self.gameFrameRight.score.place(x=0, y=420, width=env.RIGHT_SCREEN_W, height=60)

    def activateListening(self):
        self.master.isListening = True

    def __del__(self):
        print("trying destroy Mode 0")
        if self.game is not None:
            self.game.destroy()
