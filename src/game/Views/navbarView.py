import tkinter
from functools import partial

from PIL import Image, ImageTk

from src.game import env
from src.game.GamesNames import GameNames
from src.game.ViewModels.navbarViewModel import NavbarViewModel
from src.game.utils.colors import Colors
from src.game.utils.customElements.scales import *


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

        self.btnEarTrainingNote = tk.Label(self.parent, image=self.mode0ImageBlack, height=BUTTON_HEIGHT, bg=Colors.BTN_SIDEBAR_NEUTRAL)
        self.btnEarTrainingNote.pack(side=tk.TOP, fill=tk.X)

        self.btnEarTrainingChord = tk.Label(self.parent, image=self.mode1ImageBlack, height=BUTTON_HEIGHT, bg=Colors.BTN_SIDEBAR_NEUTRAL)
        self.btnEarTrainingChord.pack(side=tk.TOP, fill=tk.X)

        self.btnBacktracks = tk.Label(self.parent, image=self.mode2ImageBlack, height=BUTTON_HEIGHT, bg=Colors.BTN_SIDEBAR_NEUTRAL)
        self.btnBacktracks.pack(side=tk.TOP, fill=tk.X)

        self.btnPractiseLicks = tk.Label(self.parent, image=self.mode3ImageBlack, height=BUTTON_HEIGHT, bg=Colors.BTN_SIDEBAR_NEUTRAL)
        self.btnPractiseLicks.pack(side=tk.TOP, fill=tk.X)

        # =========== CREATION OF THE VIEW_MODEL ====================
        self.viewModel = NavbarViewModel(self)
        # ===========================================================

        self.btnEarTrainingNote.bind('<Button-1>', partial(self.master.new_window, GameNames.GAME_EAR_TRAINING_NOTE))
        self.btnEarTrainingChord.bind('<Button-1>', partial(self.master.new_window, GameNames.GAME_EAR_TRAINING_CHORDS))
        self.btnBacktracks.bind('<Button-1>', partial(self.master.new_window, GameNames.GAME_BACKTRACKS))
        self.btnPractiseLicks.bind('<Button-1>', partial(self.master.new_window, GameNames.GAME_LICKS_PRACTISE))

    def resetAllButtonsBackgroundColor(self):
        self.btnEarTrainingNote.configure(background=Colors.BTN_SIDEBAR_NEUTRAL, image=self.mode0ImageBlack)
        self.btnEarTrainingChord.configure(background=Colors.BTN_SIDEBAR_NEUTRAL, image=self.mode1ImageBlack)
        self.btnBacktracks.configure(background=Colors.BTN_SIDEBAR_NEUTRAL, image=self.mode2ImageBlack)
        self.btnPractiseLicks.configure(background=Colors.BTN_SIDEBAR_NEUTRAL, image=self.mode3ImageBlack)

    def highLightActiveMode(self, game_mode: GameNames):
        self.resetAllButtonsBackgroundColor()
        if game_mode.value == GameNames.GAME_EAR_TRAINING_NOTE.value:
            self.btnEarTrainingNote.configure(background=Colors.BTN_SIDEBAR_PUSHED, image=self.mode0ImageWhite)
        elif game_mode.value == GameNames.GAME_EAR_TRAINING_CHORDS.value:
            self.btnEarTrainingChord.configure(background=Colors.BTN_SIDEBAR_PUSHED, image=self.mode1ImageWhite)
        elif game_mode.value == GameNames.GAME_BACKTRACKS.value:
            self.btnBacktracks.configure(background=Colors.BTN_SIDEBAR_PUSHED, image=self.mode2ImageWhite)
        elif game_mode.value == GameNames.GAME_LICKS_PRACTISE.value:
            self.btnPractiseLicks.configure(background=Colors.BTN_SIDEBAR_PUSHED, image=self.mode3ImageWhite)
        else:
            pass
