from src.game.autoload import Autoload
from src.game.mode2.recordSetupGui import RecordSetupGui
from src.game.utils.customElements.customElements import *
from src.game.utils.customElements.labels import *


class RecordWithBacktrack:
    def __init__(self, globalRoot, app):

        self.globalRoot = globalRoot
        self.audioInstance = Autoload.get_instance().getAudioInstance()
        self.app = app

        self.nbOfLoops = 2
        self.backtrack = None

        self.window = tk.Toplevel(self.globalRoot)
        # self.window.config(cursor="none")
        self.window.attributes('-fullscreen', True)
        self.window.geometry("320x480")
        self.window["bg"] = "black"

        self.currentTrack = self.audioInstance.getCurrentTrack()
        self.category = self.audioInstance.activeFolder
        trackName = self.currentTrack[0].split("/")[-1]
        trackLength = "{0:.2f}".format(self.currentTrack[1])

        self.window.lblStatic1 = MyLabel24(self.window, text="How many bars?")
        self.window.btnWithBacktrack = BtnBlack12(self.window, text="OK")
        self.window.btnWithBacktrack.config(command=self.nextWindow)
        self.window.nbOfLoops = MyLabel40(self.window, text=self.nbOfLoops)
        self.window.btnLess = BtnBlack12(self.window, text="<", command=self.lessLoops)
        self.window.btnMore = BtnBlack12(self.window, text=">", command=self.moreLoops)
        # self.window.lblBacktrack = MyLabel12(self.window, text="length one loop {} sec.".format(str(round(self.currentTrack[1],2))))
        self.window.lblBacktrack = MyLabel12(self.window, text="")
        self.window.btnWithoutBacktrack = BtnBlack12(self.window, text="Cancel", command=self.cancel)
        self.window.lblStatic2 = MyLabel12(self.window,
                                           wraplength=320,
                                           text="current backtrack:\n{}\n({} ms)".format(trackName, trackLength))

        # PLACEMENT
        yplacement = 40
        self.window.lblStatic1.place(x=0, y=yplacement, width=320, height=50)
        yplacement += 60
        self.window.btnLess.place(x=0, y=yplacement, width=80, height=60)
        self.window.nbOfLoops.place(x=40, y=yplacement, width=240, height=60)
        self.window.btnMore.place(x=240, y=yplacement, width=80, height=60)
        yplacement += 80
        self.window.lblStatic2.place(x=0, y=yplacement, width=320, height=80)
        yplacement += 100
        # self.window.lblBacktrack.place(x=20,y=yplacement, width=280, height=60)
        self.window.btnWithBacktrack.place(x=40, y=yplacement, width=240, height=60)
        yplacement += 80
        self.window.btnWithoutBacktrack.place(x=40, y=yplacement, width=240, height=60)

    def lessLoops(self):
        self.nbOfLoops += -1
        if self.nbOfLoops <= 1:
            self.nbOfLoops = 1
        self.window.nbOfLoops.config(text=self.nbOfLoops)

    def moreLoops(self):
        self.nbOfLoops += 1
        if self.nbOfLoops >= 24:
            self.nbOfLoops = 24
        self.window.nbOfLoops.config(text=self.nbOfLoops)

    def nextWindow(self):
        self.window.destroy()
        try:
            self.globalRoot.recordFrame.destroy()
        except Exception as e:
            print(e)
        try:
            del self.globalRoot.recordFrame
        except Exception as e:
            print(e)

        self.globalRoot.recordFrame = RecordSetupGui(
            self.globalRoot,
            self.currentTrack[0],
            self.currentTrack[1],
            self.nbOfLoops,
            self.app)
        del self

    def cancel(self):
        self.window.destroy()
        self.app.new_window(2)

    def destroy(self):
        pass
