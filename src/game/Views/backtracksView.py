from functools import partial
from glob import glob
import os

from PIL import Image, ImageTk

from src.game import env
from src.game.GamesNames import GameNames
from src.game.ViewModels.backtracksViewModel import BacktracksViewModel, BacktracksConstants
from src.game.utils.customElements.customElements import *
from src.game.utils.customElements.labels import *

# from src.game.ViewModels.backtracksViewModel import BacktracksViewModel
BTN_PADDING_X = 3
BTN_PADDING_Y = 4
LEFT_PANEL_PADDING_X = 20


class ViewStrings(Enum):
    STRING_LBL_TRACK_TITLE = "Title : "
    STRING_LBL_TRACK_CATEGORY = "Category :"


class ViewImages:
    def __init__(self):
        IMAGE_PLAY_IMAGE = ImageTk.PhotoImage(Image.open(env.PLAY_IMAGE))
        IMAGE_PAUSE_IMAGE = ImageTk.PhotoImage(Image.open(env.PAUSE_IMAGE))
        IMAGE_SHUFFLE_IMAGE = ImageTk.PhotoImage(Image.open(env.SHUFFLE_IMAGE))


class BacktracksView:
    def __init__(self, master, game_frame: tk.Frame):
        print("launching game {}".format(GameNames.GAME_BACKTRACKS))
        self.master = master
        self.viewModel = None
        self.gameFrame = game_frame
        self.backtracksCategoriesTuples = []

        self.gameFrame.grid_rowconfigure(0, uniform='row_height', weight=1)
        self.gameFrame.grid_rowconfigure(1, uniform='row_height', weight=1)
        self.gameFrame.grid_rowconfigure(2, uniform='row_height', weight=1)
        self.gameFrame.grid_rowconfigure(3, uniform='row_height', weight=1)
        self.gameFrame.grid_rowconfigure(4, uniform='row_height', weight=1)

        self.gameFrame.grid_columnconfigure(0, weight=2)
        self.gameFrame.grid_columnconfigure(1, weight=1)
        self.gameFrame.grid_columnconfigure(2, weight=2)
        self.gameFrame.grid_columnconfigure(3, uniform='column_width', weight=1)
        self.gameFrame.grid_columnconfigure(4, uniform='column_width', weight=1)
        self.gameFrame.grid_columnconfigure(5, uniform='column_width', weight=1)

        # Backtrack Section
        self.lblTrackTitle = tk.Label(self.gameFrame, text=ViewStrings.STRING_LBL_TRACK_TITLE.value, justify="center", width=20, wraplength=200)
        self.lblCategory = ttk.Label(self.gameFrame, text=ViewStrings.STRING_LBL_TRACK_CATEGORY.value)
        self.progress = ttk.Progressbar(self.gameFrame, style="danger.Horizontal.TProgressbar", value=0)
        self.btnRecord = CustomButton(self.gameFrame, text="Record")

        # Metronome section
        self.btnBpmMinus = CustomButton(self.gameFrame, text="-", style=CustomStylesNames.STYLE_BTN_CONTROLS_PLUS_MINUS.value)
        self.lblMetro = tk.Label(self.gameFrame, text="metroValue", font=(DEFAULT_FONT_NAME, 80))
        self.btnBpmPlus = CustomButton(self.gameFrame, text="+", style=CustomStylesNames.STYLE_BTN_CONTROLS_PLUS_MINUS.value)
        self.slTempo = CustomScale(self.gameFrame, from_=BacktracksConstants.TEMPO_MIN_BPM.value, to=BacktracksConstants.TEMPO_MAX_BPM.value)

        # Right Section
        current_row = 0
        self.btnMetro = CustomButton(self.gameFrame, text="Metro")
        self.btnMetro.grid(row=current_row, column=3, columnspan=3, sticky=tk.NSEW, padx=BTN_PADDING_X, pady=BTN_PADDING_Y)

        current_row = 4
        self.btnRandom = CustomButton(self.gameFrame, text="Random")
        self.btnRandom.grid(row=current_row, rowspan=1, column=3, sticky=tk.NSEW, padx=BTN_PADDING_X, pady=BTN_PADDING_Y)

        self.btnPlay = CustomButton(self.gameFrame, text="PLAY/STOP")
        self.btnPlay.grid(row=current_row, rowspan=1, column=4, columnspan=2, sticky=tk.NSEW, padx=BTN_PADDING_X, pady=BTN_PADDING_Y)

        self.setUiShowMetronomeSection()

        # =========== CREATION OF THE VIEW_MODEL ====================
        self.viewModel = BacktracksViewModel(self)
        # ===========================================================

        # after we have sent all the categories to the view, we trigger a function to the view which place all the category buttons on the ui
        self.setUiPlaceAllBtnCategories()

        self.btnPlay.config(command=self.viewModel.onBtnPlayClick)
        self.btnRandom.config(command=self.viewModel.onBtnRandomClick)

        self.btnMetro.config(command=self.viewModel.onBtnMetronomeClick)
        self.btnBpmPlus.config(command=self.viewModel.onBtnBpmPlusClick)
        self.btnBpmMinus.config(command=self.viewModel.onBtnBpmMinusClick)
        self.slTempo.bind("<ButtonRelease-1>", self.viewModel.onSliderTempoMoved)

    def setUiShowMetronomeSection(self):
        self.lblTrackTitle.grid_remove()
        self.lblCategory.grid_remove()
        self.progress.grid_remove()
        self.btnRecord.grid_remove()

        self.btnBpmMinus.grid(row=1, rowspan=3, column=0, sticky=tk.EW, padx=(LEFT_PANEL_PADDING_X, 0), pady=BTN_PADDING_Y)
        self.lblMetro.grid(row=1, rowspan=3, column=1, padx=0)
        self.btnBpmPlus.grid(row=1, rowspan=3, column=2, sticky=tk.EW, padx=(0, LEFT_PANEL_PADDING_X), pady=BTN_PADDING_Y)
        self.slTempo.grid(row=4, column=0, columnspan=3, sticky=tk.EW, padx=LEFT_PANEL_PADDING_X)

    def setUiShowBacktrackSection(self):
        self.btnBpmMinus.grid_remove()
        self.lblMetro.grid_remove()
        self.btnBpmPlus.grid_remove()
        self.slTempo.grid_remove()

        self.lblTrackTitle.grid(row=1, rowspan=1, column=0, columnspan=3, sticky=tk.NSEW, padx=LEFT_PANEL_PADDING_X)
        self.lblCategory.grid(row=2, column=0, columnspan=3, padx=LEFT_PANEL_PADDING_X)
        self.progress.grid(row=3, column=0, columnspan=3, sticky=tk.EW, padx=LEFT_PANEL_PADDING_X)
        self.btnRecord.grid(row=4, column=0, columnspan=3, sticky=tk.NSEW, padx=BTN_PADDING_X, pady=BTN_PADDING_Y)

    def setUiLblMetronome(self, tempo: int):
        self.lblMetro.config(text=str(tempo))
        self.slTempo.set(tempo)

    def setUiUpdateProgress(self, percentage):
        self.progress.config(value=percentage)

    def setUiCurrentBacktrack(self, category: str, filename: str, index: int, category_length: int):
        self.lblCategory.config(text=category)
        text = "Playing {}\n({}/{})".format(filename, index + 1, category_length)
        self.lblTrackTitle.config(text=text)

    def setUiAddBtnCategory(self, category_id: int, category_name: str, quantity: int):
        btnLabel = category_name + " (" + str(quantity) + ")"
        self.backtracksCategoriesTuples.append((category_id, category_name, CustomButton(self.gameFrame, text=btnLabel), quantity))

    def setUiPlaceAllBtnCategories(self):
        starting_row = 1
        starting_column = 3
        columns_per_row = 3
        row_counter = starting_row
        column_counter = starting_column
        for (category_id, category_name, category_btn, category_quantity) in self.backtracksCategoriesTuples:
            category_btn.config(command=partial(self.viewModel.onBtnCategoryClick, category_name))
            category_btn.grid(row=row_counter, column=column_counter, sticky=tk.NSEW, padx=BTN_PADDING_X, pady=BTN_PADDING_Y)
            column_counter += 1
            if column_counter >= starting_column + columns_per_row:
                column_counter = starting_column
                row_counter += 1

    @staticmethod
    def getAllWavFolders():
        raw_wav_folders = glob(env.PROCESSED_WAV_BASE_FOLDER + '/*/')
        wav_folders = []
        # We want to extract just the names of the folders for the display
        for folder in raw_wav_folders:
            # check if we are running on windows(dev) or linux(prod)
            if os.name == 'nt':
                wav_folders.append(folder.split('\\')[-2])
            elif os.name == 'posix':
                wav_folders.append(folder.split('/')[-2])
            else:
                raise Exception("Unknown operating system")
        return wav_folders
