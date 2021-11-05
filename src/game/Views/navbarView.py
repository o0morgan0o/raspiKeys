import tkinter
import tkinter.font
from functools import partial

from PIL import Image, ImageTk

from src.game import env
from src.game.GamesNames import GameNames
from src.game.ViewModels.navbarViewModel import NavbarViewModel
from src.game.utils.colors import Colors
from src.game.utils.customElements.customElements import DEFAULT_FONT_NAME
from src.game.utils.customElements.scales import *


class NavBarView:

    def __init__(self, master, parent: tkinter.Frame):
        self.master = master
        self.parent = parent
        self.viewModel = None

        # images
        self.volumeImage = ImageTk.PhotoImage(Image.open(env.VOLUME_IMAGE))
        self.configImage = ImageTk.PhotoImage(Image.open(env.SETTINGS_IMAGE))
        self.imageBlackEarTrainingNote = ImageTk.PhotoImage(Image.open(env.IMAGE_BLACK_EAR_TRAINING_NOTE))
        self.imageBlackEarTrainingChord = ImageTk.PhotoImage(Image.open(env.IMAGE_BLACK_EAR_TRAINING_CHORD))
        self.imageBlackBacktracks = ImageTk.PhotoImage(Image.open(env.IMAGE_BLACK_BACKTRACKS))
        self.imageBlackPractiseLicks = ImageTk.PhotoImage(Image.open(env.IMAGE_BLACK_PRACTISE_LICKS))
        self.imageWhiteEarTrainingNote = ImageTk.PhotoImage(Image.open(env.IMAGE_WHITE_EAR_TRAINING_NOTE))
        self.imageWhiteEarTrainingChord = ImageTk.PhotoImage(Image.open(env.IMAGE_WHITE_EAR_TRAINING_CHORD))
        self.imageWhiteBacktracks = ImageTk.PhotoImage(Image.open(env.IMAGE_WHITE_BACKTRACKS))
        self.imageWhitePractiseLicks = ImageTk.PhotoImage(Image.open(env.IMAGE_WHITE_PRACTISE_LICKS))

        PADDING_FOR_VERTICAL_SPACE = 60
        BUTTON_HEIGHT = 80

        self.container = tk.Frame(self.parent)
        self.container.pack(fill=tk.BOTH, expand=1)

        self.btnEarTrainingNote = tk.Label(self.container, image=self.imageBlackEarTrainingNote, height=BUTTON_HEIGHT, bg=Colors.BTN_SIDEBAR_NEUTRAL)
        self.btnEarTrainingNote.pack(side=tk.TOP, fill=tk.X)

        self.btnEarTrainingChord = tk.Label(self.container, image=self.imageBlackEarTrainingChord, height=BUTTON_HEIGHT, bg=Colors.BTN_SIDEBAR_NEUTRAL)
        self.btnEarTrainingChord.pack(side=tk.TOP, fill=tk.X)

        self.btnBacktracks = tk.Label(self.container, image=self.imageBlackBacktracks, height=BUTTON_HEIGHT, bg=Colors.BTN_SIDEBAR_NEUTRAL)
        self.btnBacktracks.pack(side=tk.TOP, fill=tk.X)

        self.btnPractiseLicks = tk.Label(self.container, image=self.imageBlackPractiseLicks, height=BUTTON_HEIGHT, bg=Colors.BTN_SIDEBAR_NEUTRAL)
        self.btnPractiseLicks.pack(side=tk.TOP, fill=tk.X)

        self.btnOpts = tk.Label(self.container, text='Opts', font=(DEFAULT_FONT_NAME, 14, tkinter.font.BOLD),
                                bg=Colors.BTN_SIDEBAR_NEUTRAL, pady=28)
        self.btnOpts.pack(side=tk.TOP, fill=tk.X)

        # =========== CREATION OF THE VIEW_MODEL ====================
        self.viewModel = NavbarViewModel(self)
        # ===========================================================

        self.btnEarTrainingNote.bind('<Button-1>', partial(self.master.new_window, GameNames.GAME_EAR_TRAINING_NOTE))
        self.btnEarTrainingChord.bind('<Button-1>', partial(self.master.new_window, GameNames.GAME_EAR_TRAINING_CHORDS))
        self.btnBacktracks.bind('<Button-1>', partial(self.master.new_window, GameNames.GAME_BACKTRACKS))
        self.btnPractiseLicks.bind('<Button-1>', partial(self.master.new_window, GameNames.GAME_LICKS_PRACTISE))
        self.btnOpts.bind('<Button-1>', partial(self.master.new_window, GameNames.GAME_OPTIONS))

    def resetAllButtonsBackgroundColor(self):
        self.btnEarTrainingNote.configure(background=Colors.BTN_SIDEBAR_NEUTRAL, image=self.imageBlackEarTrainingNote)
        self.btnEarTrainingChord.configure(background=Colors.BTN_SIDEBAR_NEUTRAL, image=self.imageBlackEarTrainingChord)
        self.btnBacktracks.configure(background=Colors.BTN_SIDEBAR_NEUTRAL, image=self.imageBlackBacktracks)
        self.btnPractiseLicks.configure(background=Colors.BTN_SIDEBAR_NEUTRAL, image=self.imageBlackPractiseLicks)
        self.btnOpts.configure(background=Colors.BTN_SIDEBAR_NEUTRAL, foreground=Colors.TEXT_BLACK)

    def highLightActiveMode(self, game_mode: GameNames):
        self.resetAllButtonsBackgroundColor()
        if game_mode.value == GameNames.GAME_EAR_TRAINING_NOTE.value:
            self.btnEarTrainingNote.configure(background=Colors.BTN_SIDEBAR_PUSHED, image=self.imageWhiteEarTrainingNote)
        elif game_mode.value == GameNames.GAME_EAR_TRAINING_CHORDS.value:
            self.btnEarTrainingChord.configure(background=Colors.BTN_SIDEBAR_PUSHED, image=self.imageWhiteEarTrainingChord)
        elif game_mode.value == GameNames.GAME_BACKTRACKS.value:
            self.btnBacktracks.configure(background=Colors.BTN_SIDEBAR_PUSHED, image=self.imageWhiteBacktracks)
        elif game_mode.value == GameNames.GAME_LICKS_PRACTISE.value:
            self.btnPractiseLicks.configure(background=Colors.BTN_SIDEBAR_PUSHED, image=self.imageWhitePractiseLicks)
        elif game_mode.value== GameNames.GAME_OPTIONS.value:
            self.btnOpts.configure(background=Colors.BTN_SIDEBAR_PUSHED, foreground=Colors.TEXT_WHITE)
        else:
            pass
