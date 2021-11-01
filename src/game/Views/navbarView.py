import tkinter

from PIL import Image, ImageTk

from src.game import env
from src.game.GamesNames import GameNames
from src.game.ViewModels.navbarViewModel import NavbarViewModel
from src.game.utils.customElements.scales import *
from src.game.utils.colors import Colors


class NavBarView:

    def __init__(self, master, parent: tkinter.Frame):
        self.master = master
        self.parent = parent
        self.viewModel = None

        # images
        self.volumeImage = ImageTk.PhotoImage(Image.open(env.VOLUME_IMAGE))
        self.configImage = ImageTk.PhotoImage(Image.open(env.SETTINGS_IMAGE))
        self.mode0ImageBlack = ImageTk.PhotoImage(Image.open(env.MODE0_IMAGE_BLACK))
        self.mode1ImageBlack = ImageTk.PhotoImage(Image.open(env.MODE1_IMAGE_BLACK))
        self.mode2ImageBlack = ImageTk.PhotoImage(Image.open(env.MODE2_IMAGE_BLACK))
        self.mode3ImageBlack = ImageTk.PhotoImage(Image.open(env.MODE3_IMAGE_BLACK))
        self.mode0ImageWhite = ImageTk.PhotoImage(Image.open(env.MODE0_IMAGE_WHITE))
        self.mode1ImageWhite = ImageTk.PhotoImage(Image.open(env.MODE1_IMAGE_WHITE))
        self.mode2ImageWhite = ImageTk.PhotoImage(Image.open(env.MODE2_IMAGE_WHITE))
        self.mode3ImageWhite = ImageTk.PhotoImage(Image.open(env.MODE3_IMAGE_WHITE))

        PADDING_FOR_VERTICAL_SPACE = 60
        BUTTON_HEIGHT = 80

        # ///////// btn
        self.btnEarTrainingNote = tk.Button(self.parent, image=self.mode0ImageBlack, height=BUTTON_HEIGHT)
        self.btnEarTrainingNote.pack(fill=tk.BOTH, expand=True, pady=(PADDING_FOR_VERTICAL_SPACE, 0))
        # ///////// btn
        self.btnEarTrainingChord = tk.Button(self.parent, image=self.mode1ImageBlack, height=BUTTON_HEIGHT)
        self.btnEarTrainingChord.pack(fill=tk.BOTH, expand=True)
        # ///////// btn
        self.btnBacktracks = tk.Button(self.parent, image=self.mode2ImageBlack, height=BUTTON_HEIGHT)
        self.btnBacktracks.pack(fill=tk.BOTH, expand=True)
        # ///////// btn
        self.btnPractiseLicks = tk.Button(self.parent, image=self.mode3ImageBlack, height=BUTTON_HEIGHT)
        self.btnPractiseLicks.pack(fill=tk.BOTH, expand=True, pady=(0, PADDING_FOR_VERTICAL_SPACE))

        # =========== CREATION OF THE VIEW_MODEL ====================
        self.viewModel = NavbarViewModel(self)
        # ===========================================================

        self.btnEarTrainingNote.config(command=lambda: self.master.new_window(GameNames.GAME_EAR_TRAINING_NOTE))
        self.btnEarTrainingChord.config(command=lambda: self.master.new_window(GameNames.GAME_EAR_TRAINING_CHORDS))
        self.btnBacktracks.config(command=lambda: self.master.new_window(GameNames.GAME_BACKTRACKS))
        # self.button4["command"] = lambda: self.new_window(3)

    def resetAllButtonsBackgroundColor(self):
        self.btnEarTrainingNote.configure(background=Colors.BTN_SIDEBAR_NEUTRAL)
        self.btnEarTrainingChord.configure(background=Colors.BTN_SIDEBAR_NEUTRAL)
        self.btnBacktracks.configure(background=Colors.BTN_SIDEBAR_NEUTRAL)
        self.btnPractiseLicks.configure(background=Colors.BTN_SIDEBAR_NEUTRAL)

    def highLightActiveMode(self, game_mode: GameNames):
        self.resetAllButtonsBackgroundColor()
        if game_mode.value == GameNames.GAME_EAR_TRAINING_NOTE.value:
            self.btnEarTrainingNote.configure(background=Colors.BTN_SIDEBAR_PUSHED)
        elif game_mode.value == GameNames.GAME_EAR_TRAINING_CHORDS.value:
            self.btnEarTrainingChord.configure(background=Colors.BTN_SIDEBAR_PUSHED)
        elif game_mode.value == GameNames.GAME_BACKTRACKS.value:
            self.btnBacktracks.configure(background=Colors.BTN_SIDEBAR_PUSHED)
        elif game_mode.value == GameNames.GAME_LICKS_PRACTISE.value:
            self.btnPractiseLicks.configure(background=Colors.BTN_SIDEBAR_PUSHED)
        else:
            pass
