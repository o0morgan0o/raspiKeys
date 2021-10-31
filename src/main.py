#!/usr/bin/python3
import logging

from src.game import env
from src.game.Styles.customStyles import CustomButtonStyle
from src.game.Views.earTrainingNoteView import EarTrainingNoteView
from src.game.Views.backtracksView import BacktracksView
from src.game.Views.footerView import FooterView
from src.game.Views.navbarView import NavBarView, GameNames
from src.game.Views.optionsView import OptionsView
from src.game.autoload import Autoload
from src.game.utils.config import loadConfig
from src.game.utils.customElements.customElements import *


# TODO improvements
# - It would be nice to have a server running for uploading musics,
# - Folder in backtracks view could be made automatically according to all files in folder

class MainApplication(tk.Tk):

    def __init__(self):
        super().__init__()
        self.body = None
        self.config = loadConfig()

        # use my own styles
        style = CustomButtonStyle()

        # initialisation of default mode, this tracks the current active state of the application
        # self.currentGameMode = GameNames.GAME_OPTIONS
        # self.currentGameMode = GameNames.GAME_EAR_TRAINING_NOTE
        self.currentGameMode = GameNames.GAME_BACKTRACKS
        self.app = None
        self.audioInstance = Autoload.get_instance().getAudioInstance()

        # Main Frame
        self.title("RaspyKeys")
        self.geometry("%sx%s" % (env.FULL_SCREEN_W, env.FULL_SCREEN_H))
        # self.style = ttk.Style(self)
        # print("ALL_THEMES" , self.style.theme_names())

        self.frame = None

        # keyboard shortcuts for dev
        self.bind("<Escape>", lambda event: self.cleanWindow())
        self.protocol('WM_DELETE_WINDOW', self.cleanWindow)

        self.sideNavBarFrame = tk.Frame(self, width=env.NAVBAR_WIDTH, height=env.FULL_SCREEN_H, bg="red")
        self.sideNavBarFrame.place(x=0, y=0, width=env.NAVBAR_WIDTH, height=env.FULL_SCREEN_H)
        self.sideNavBar = NavBarView(self, self.sideNavBarFrame)

        self.footerFrame = tk.Frame(self, background=Colors.BACKGROUND)
        self.footerFrame.place(x=env.NAVBAR_WIDTH, y=env.FULL_SCREEN_H - env.FOOTER_HEIGHT,
                               width=env.FULL_SCREEN_W - env.NAVBAR_WIDTH, height=env.FOOTER_HEIGHT)
        self.footer = FooterView(self, self.footerFrame)

        # initialization
        # Load default Screen
        self.new_window(self.currentGameMode)

    # method to load a new game mode
    def new_window(self, new_game_mode: GameNames):
        # Import style for ttk.bootstrap styles
        getCustomStyles()
        if self.body is not None:
            self.body.destroy()

        # recreation of the body frame (middle frame)
        print("[GAME CHANGE] Creating new game window")
        self.body = tk.Frame(self, bg='yellow')
        # self.body = tk.Frame(self, bg=Colors.BACKGROUND)
        self.body.place(x=env.NAVBAR_WIDTH, y=0, width=env.FULL_SCREEN_W - env.NAVBAR_WIDTH, height=env.FULL_SCREEN_H - env.FOOTER_HEIGHT)

        if self.app is not None:
            print("Deleting app : ", self.app)
            del self.app

        if new_game_mode.value == GameNames.GAME_EAR_TRAINING_NOTE.value:
            self.app = EarTrainingNoteView(self, self.body)

        # elif new_game_mode.value == GameNames.GAME_EAR_TRAINING_CHORDS.value:
        #     self.app = Mode1(self.body, self.config)
        #     self.app.activateListening()

        elif new_game_mode.value == GameNames.GAME_BACKTRACKS.value:
            self.app = BacktracksView(self.master, self.body)
        # elif self.sideNavBar.currentGameMode == 3:
        #     self.app = Mode3(self.master, self.master.bodyLeft, self.config, self)
        elif new_game_mode.value == GameNames.GAME_OPTIONS.value:
            self.app = OptionsView(self, self.body, self.config)
        else:
            return
        self.sideNavBar.highLightActiveMode(new_game_mode)

    def cleanWindow(self):
        self.audioInstance.stopPlay()
        self.destroy()



if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()
