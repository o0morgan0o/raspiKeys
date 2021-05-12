import tkinter as tk

from game.mode2.gameplay import Game
from game import env

from game.utils.customElements.buttons import *
from game.utils.customElements.labels import *


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

        # Metro btn
        self.gameFrame.btnMetro = BtnBlack20( self.gameFrame, text="Metro", activebackground="black")
        self.gameFrame.btnBpmMinus=BtnBlack20(self.gameFrame,text="-",activebackground="black")
        self.gameFrame.btnBpmPlus=BtnBlack20(self.gameFrame,text="+",activebackground="black")

        self.gameFrame.btnSwitchPage=BtnBlack20(self.gameFrame, text=">>", activebackground="black")

        self.gameFrame.btnHouse = BtnBlack20(
            self.gameFrame, text="House", activebackground="black")
        self.gameFrame.btnLatin = BtnBlack20(
            self.gameFrame, text="Latin", activebackground="black")
        self.gameFrame.btnJazz = BtnBlack20(
            self.gameFrame, text="Jazz", activebackground="black")
        self.gameFrame.btnHipHop = BtnBlack20(
            self.gameFrame, text="H.H.", activebackground="black")

        self.placeElements()
        self.game = Game(self.globalRoot, self.gameFrame, config, app)

    def placeElements(self):
        yplacement = 20
        self.gameFrame.btnMetro.place(x=10, y=yplacement, width=100,height=80)
        self.gameFrame.btnBpmMinus.place(x=130, y=yplacement,width=90, height=80)
        self.gameFrame.btnBpmPlus.place(x=220, y=yplacement,width=90, height=80)

        yplacement+= 100
        self.gameFrame.btnHouse.place(x=10, y=yplacement, width=140, height=80)
        self.gameFrame.btnLatin.place( x=170, y=yplacement, width=140, height=80)
        # self.gameFrame.lblStatic1.place(
        #     x=0, y=yplacement, width=320, height=40)
        yplacement += 100
        self.gameFrame.btnJazz.place(x=10, y=yplacement, width=140, height=80)
        # self.gameFrame.labelCurrent.place(
        #     x=0, y=yplacement, width=340, height=80)
        self.gameFrame.btnSwitchPage.place(x=170, y=yplacement, width=140,height=80)


        # self.gameFrame.canvas.place(x=20, y=yplacement, width=280, height=20)
        #============
        # PAGE 2
        self.gameFrame.btnHipHop.place( x=-200, y=yplacement, width=140, height=80)
        self.gameFrame.btnPlay.place(x=-200, y=yplacement, width=140, height=80)
        self.gameFrame.btnLick.place(x=-200, y=yplacement, width=140, height=80)
        #============
        yplacement += 100
        self.gameFrame.canvas.place(x=0, y=yplacement, width=320, height=10)
        # self.gameFrame.btnRandom.place(x=170, y=yplacement, width=140, height=80)

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
