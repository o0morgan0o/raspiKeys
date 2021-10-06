import tkinter as tk
from game import env
from game.mode0.gameplay import Game

from game.utils.customElements.buttons import *
from game.utils.customElements.labels import *
from game.utils.customElements.scales import SettingsScale
from game.utils.utilFunctions import *


class Mode0:
    def __init__(self, gameFrameLeft, gameFrameRight, config):
        print("launchiOg game 0 -------------- ")
        self.gameFrameLeft = gameFrameLeft
        self.gameFrameRight = gameFrameRight
        self.gameFrameLeft.pack_propagate(0)

        config = loadConfig()
        # TODO : make custom fonts

        self.gameFrameLeft.lblInterval = MyLabel18(self.gameFrameLeft)
        self.gameFrameLeft.lblInterval.config(font=("Courier", 12), text="Interval section:")
        self.gameFrameLeft.lblMidiVolume = MyLabel18(self.gameFrameLeft)
        self.gameFrameLeft.lblMidiVolume.config(font=("Courier", 12), text="Midi Volume:")

        self.gameFrameLeft.slInterval = SettingsScale(self.gameFrameLeft, from_=3, to=18,
                                                      orient=tk.HORIZONTAL)  # command=self.updateConfig)
        self.gameFrameLeft.slInterval.set(int(config["mode0IntervalOffset"]))
        self.gameFrameLeft.slInterval.config(showvalue=0)

        self.gameFrameLeft.slMidiVolume = SettingsScale(self.gameFrameLeft, from_=1, to=127,
                                                        orient=tk.HORIZONTAL)  # command=self.updateConfig)
        self.gameFrameLeft.slMidiVolume.set(int(config["mode0MidiVolume"]))
        self.gameFrameLeft.slMidiVolume.config(showvalue=0)
        # self.gameFrameLeft.slMidiVolume.set()

        # definition of sizes and fonts
        self.gameFrameRight.pickNote = MyLabel18(self.gameFrameRight)  # for user instructions
        self.gameFrameRight.pickNote.config(font=("Courier", 24))
        self.gameFrameRight.result = MyLabel18(self.gameFrameRight, padx=10,
                                               pady=10)  # for "correct" or "incorrect"response
        self.gameFrameRight.result.config(font=("Courier", 18, "bold"), text="")
        self.gameFrameRight.score = MyLabel30(self.gameFrameRight, )  # for global score
        self.gameFrameRight.score.config(font=("Courier", 10, "bold"), text="SCORE")

        self.gameFrameRight.btnSkip = BtnBlack20(self.gameFrameRight, text="SKIP >")
        self.gameFrameRight.btnSkip.config(bd=0, highlightthickness=0)
        self.gameFrameRight.lblNote = MyLabel40(self.gameFrameRight, justify="right")
        self.gameFrameRight.lblNote.config(font=("Courier", 120, "bold"), text="?")
        self.gameFrameRight.lblNoteUser = MyLabel40(self.gameFrameRight)
        self.gameFrameRight.lblNoteUser.config(font=("Courier", 120, "bold"), text="", justify="left")

        # placement of differents labels
        self.placeElements()

        self.game = Game(self.gameFrameLeft, self.gameFrameRight, config)

    def placeElements(self):
        yoffset = 160
        self.gameFrameLeft.lblInterval.place(x=20, y=yoffset, width=env.LEFT_SCREEN_W - 40, height=30)
        yoffset += 40
        self.gameFrameLeft.slInterval.place(x=20, y=yoffset, width=env.LEFT_SCREEN_W - 40, height=30)
        yoffset += 40
        self.gameFrameLeft.lblMidiVolume.place(x=20, y=yoffset, width=env.LEFT_SCREEN_W - 40, height=30)
        yoffset += 40
        self.gameFrameLeft.slMidiVolume.place(x=20, y=yoffset, width=env.LEFT_SCREEN_W - 40, height=30)

        # self.gameFrameRight.configure(bg="red") # should be invisible
        # self.gameFrameRight.result.place(x=0, y=0,width=env.RIGHT_SCREEN_W,height=80)
        self.gameFrameRight.pickNote.place(x=0, y=30, width=env.RIGHT_SCREEN_W, height=40)
        self.gameFrameRight.lblNoteUser.place(x=0, y=140, width=env.RIGHT_SCREEN_W)
        self.gameFrameRight.lblNote.place(x=0, y=140, width=env.RIGHT_SCREEN_W)
        self.gameFrameRight.lblNote.lift()
        self.gameFrameRight.btnSkip.place(x=0, y=350, width=env.RIGHT_SCREEN_W, height=60)
        self.gameFrameRight.score.place(x=0, y=420, width=env.RIGHT_SCREEN_W, height=60)

    def __del__(self):
        print("trying destroy Mode 0")
        self.game.destroy()

    def activateListening(self):
        self.game.isListening = True
