import tkinter as tk
from autoload import Autoload

from utils.customElements.buttons import *
from utils.customElements.labels import *

class RecordWithBacktrack:
    def __init__(self, root,parent):

        self.root=root
        self.parent = parent
        self.audioInstance = Autoload().getInstanceAudio()

        self.nbOfLoops=2
        self.backtrack= None

        self.window = tk.Toplevel(self.root)
        self.window.attributes('-fullscreen', True)
        self.window.geometry("320x480")
        self.window["bg"]="black"

        self.window.btnWithBacktrack = BtnBlack12(self.window, text="WITH Backtrack")
        self.window.btnWithBacktrack.config(command=self.nextWindow)
        self.window.nbOfLoops = MyLabel40(self.window, text=self.nbOfLoops)
        self.window.btnLess = BtnBlack12(self.window, text="<")
        self.window.btnMore = BtnBlack12(self.window, text=">")
        self.currentTrack = self.audioInstance.getCurrentTrack()
        self.window.lblBacktrack = MyLabel12(self.window, text="length one loop {} sec.".format(str(round(self.currentTrack[1],2))))
        self.window.btnWithoutBacktrack = BtnBlack12(self.window, text="WITHOUT Backtrack")


        # PLACEMENT
        yplacement=40
        self.window.btnWithBacktrack.place(x=40, y=yplacement, width=240, height=60)
        yplacement+=80
        self.window.btnLess.place(x=0,y=yplacement, width=40,height=60)
        self.window.nbOfLoops.place(x=40, y=yplacement, width=240, height=60)
        self.window.btnMore.place(x=280,y=yplacement, width=40,height=60)
        yplacement+=80
        self.window.lblBacktrack.place(x=20,y=yplacement, width=280, height=60)
        yplacement+=80
        self.window.btnWithoutBacktrack.place(x=40, y=yplacement,width=240, height=60)



    def nextWindow(self):
        self.window.destroy()
        self.parent.showSetupWindow(self.currentTrack[0], self.currentTrack[1], self.nbOfLoops)

