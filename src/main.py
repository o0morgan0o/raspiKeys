#!/usr/bin/python3

from game import env
from game.autoload import Autoload
from game.footer.footer import Footer
from game.mode0.mode0gui import Mode0
from game.mode1.mode1gui import Mode1
from game.mode2.mode2gui import Mode2
from game.mode3.mode3gui import Mode3
from game.modeOptions.modeOptionsGui import ModeOptions
from game.navbar.navbar import SideNavbar, GameNames
from game.utils.audio import Audio
from game.utils.customElements.scales import *
from game.utils.utilFunctions import loadConfig


# TODO improvements
# - It would be nice to have a server running for uploading musics,
# - Folder in backtracks view could be made automatically according to all files in folder

class MainApplication(tk.Frame):

    def __init__(self, master, tag="", **kw):
        super().__init__(master, **kw)
        self.body = None
        self.config = loadConfig()

        # initialisation of default mode, this tracks the current active state of the application
        self.currentGameMode = GameNames.GAME_OPTIONS
        # self.currentGameMode = GameNames.GAME_EAR_TRAINING_NOTE
        self.master = master
        self.app = None
        self.audioInstance = None

        # Main Frame
        self.master.title("RaspyKeys")
        self.master.geometry("%sx%s" % (env.FULL_SCREEN_W, env.FULL_SCREEN_H))
        self.frame = None
        self.master.bodyLeft = None
        self.master.bodyRight = None

        # keyboard shortcuts for dev
        self.master.bind("<Escape>", lambda event: self.master.quit())

        self.sideNavBarFrame = tk.Frame(self.master, width=env.NAVBAR_WIDTH, height=env.FULL_SCREEN_H, bg="red")
        self.sideNavBarFrame.place(x=0, y=0, width=env.NAVBAR_WIDTH, height=env.FULL_SCREEN_H)
        self.sideNavBar = SideNavbar(self, self.sideNavBarFrame)

        self.footerFrame = tk.Frame(self.master, bg="green")
        self.footerFrame.place(x=env.NAVBAR_WIDTH, y=env.FULL_SCREEN_H - env.FOOTER_HEIGHT,
                               width=env.FULL_SCREEN_W - env.NAVBAR_WIDTH, height=env.FOOTER_HEIGHT)
        self.footer = Footer(self, self.footerFrame)

        # self.button5 = BtnMenu(self.master.footer, text="Opts")
        # self.button5["command"] = lambda: self.new_window(4)
        # self.button5.place(x=240, y=0, width=80, height=80)

        # self.volumeSlider = VolumeSliderScale(self.master.footer, command=self.sliderMoved)
        # self.volumeSlider.place(x=80, y=0, width=160, height=80)

        # load default volume
        # volume = int(self.config["volume"])
        # self.volumeSlider.set(volume)

        # storage of the current Game Classe
        self.currentGameClass = None

        # initialization
        # Load default Screen
        self.new_window(self.currentGameMode)
        # TODO make a way to retrieve the last open tab (config file load at startup ? )

    @staticmethod
    def changeVolume(offset: float):
        actual_vol = Audio.getVolume()
        if actual_vol + offset <= 0.01:
            Autoload().getInstanceAudio().setVolume(0)
        else:
            Autoload().getInstanceAudio().setVolume(actual_vol + offset)

    @staticmethod
    def sliderMoved(value: float):
        mSound = Audio.setVolume(None, value)

    # method to load a new game mode
    def new_window(self, new_game_mode: GameNames):
        self.audioInstance = Autoload().getInstanceAudio()  # in order to create the first instance of audio file

        if self.body is not None:
            self.body.destroy()
        print("Creating new game window")

        # recreation of the body frame (middle frame)
        self.body = tk.Frame(self.master, bg="yellow")
        self.body.place(x=env.NAVBAR_WIDTH, y=0, width=env.FULL_SCREEN_W - env.NAVBAR_WIDTH,
                        height=env.FULL_SCREEN_H - env.FOOTER_HEIGHT)

        if self.app is not None:
            print("Deleting app : ", self.app)
            del self.app

        if new_game_mode.value == GameNames.GAME_EAR_TRAINING_NOTE.value:
            self.app = Mode0(self.master, self.body, self.config)
            # specific to mode0 in order to skip all midi notes during another mode
            self.app.activateListening()
        elif new_game_mode.value == GameNames.GAME_EAR_TRAINING_CHORDS.value:
            self.app = Mode1(self.body, self.config)
            self.app.activateListening()
        # elif self.sideNavBar.currentGameMode == GameNames.GAME
        #     self.app = Mode2(self.master, self.master.bodyLeft, self.config, self)
        # elif self.sideNavBar.currentGameMode == 3:
        #     self.app = Mode3(self.master, self.master.bodyLeft, self.config, self)
        elif new_game_mode.value == GameNames.GAME_OPTIONS.value:
            self.app = ModeOptions(self.master, self.body, self.config)
        else:
            return

        self.sideNavBar.highLightActiveMode(new_game_mode)

    @staticmethod
    def toggleMidiListen():
        instance = Autoload().getInstance()
        instance.panic()
        instance.toggleListening()
        # if instance.isListening == True:
        # self.buttonMidiListen.config(background="grey", text="MIDILis")
        # else:
        # self.buttonMidiListen.config(background="red", text="OFF")


if __name__ == "__main__":
    root = tk.Tk()
    # root.config(cursor="none")
    root.config()
    MainApplication(root)

    root.mainloop()
