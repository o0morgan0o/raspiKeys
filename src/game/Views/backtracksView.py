import math
import os
from functools import partial
from glob import glob

from PIL import Image, ImageTk

from src.game import env
from src.game.GamesNames import GameNames
from src.game.ViewModels.backtracksViewModel import BacktracksViewModel, BacktracksConstants
from src.game.Views.recordLickView import RecordLickView
from src.game.utils.customElements.customElements import *
from src.game.utils.customElements.labels import *

# from src.game.ViewModels.backtracksViewModel import BacktracksViewModel
BTN_PADDING_X = 4
BTN_PADDING_Y = 4
LEFT_PANEL_PADDING_X = 20
RIGHT_PANEL_PADDING_X = 20
RIGHT_PANEL_PADDING_Y = 20


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
        if os.name != 'nt':
            self.gameFrame.config(cursor="none")
        self.backtracksCategoriesTuples = []

        self.tempRecordView = None

        # self.gameFrame.grid_rowconfigure(0, uniform='row_height', weight=1)
        # self.gameFrame.grid_columnconfigure(0, minsize=200, weight=1)
        # self.gameFrame.grid_columnconfigure(1, minsize=300, weight=1)
        # self.gameFrame.grid_propagate(0)

        percentageLeft= 40/100
        self.frameLeft = tk.Frame(self.gameFrame, bg=Colors.BACKGROUND, padx=LEFT_PANEL_PADDING_X)
        self.frameLeft.place(x=0, y=0,width=env.GAME_SCREEN_W*percentageLeft, height=env.GAME_SCREEN_H)
        self.frameRight = tk.Frame(self.gameFrame, bg=Colors.BACKGROUND, padx=RIGHT_PANEL_PADDING_X, pady=RIGHT_PANEL_PADDING_Y)
        self.frameRight.place(x=env.GAME_SCREEN_W*percentageLeft, y=0, width=env.GAME_SCREEN_W*(1-percentageLeft), height=env.GAME_SCREEN_H)
        # self.frameRight.grid(row=0, column=1, sticky=tk.E)

        # Backtrack Section
        self.lblTrackTitle = tk.Label(self.frameLeft, text=ViewStrings.STRING_LBL_TRACK_TITLE.value, justify="center", width=20, wraplength=200)
        self.lblCategory = tk.Label(self.frameLeft, text=ViewStrings.STRING_LBL_TRACK_CATEGORY.value, justify="center")
        self.progressBar = ttk.Progressbar(self.frameLeft, style=CustomStylesNames.STYLE_PROGRESSBAR_RED.value, value=0)
        self.btnRecord = CustomButton(self.frameLeft, text="Record")

        # Metronome section
        self.btnBpmMinus = CustomButton(self.frameLeft, text="-")
        self.lblMetro = tk.Label(self.frameLeft, text="metroValue", font=(DEFAULT_FONT_NAME, 80))
        self.btnBpmPlus = CustomButton(self.frameLeft, text="+")
        self.slTempo = CustomScale(self.frameLeft, from_=BacktracksConstants.TEMPO_MIN_BPM.value, to=BacktracksConstants.TEMPO_MAX_BPM.value)

        # Right Section
        self.btnMetro = CustomButton(self.frameRight, text="Metro")
        self.btnMetro.pack(fill=tk.X)

        self.frameCategoryContainers = tk.Frame(self.frameRight,bg=Colors.BACKGROUND, pady=RIGHT_PANEL_PADDING_Y)
        self.frameCategoryContainers.pack(expand=1, fill=tk.BOTH)

        self.btnRandom = CustomButton(self.frameRight, text="Random")
        self.btnRandom.pack(expand=1, fill=tk.BOTH, side=tk.LEFT, anchor=tk.SW)

        self.btnPlay = CustomButton(self.frameRight, text="PLAY/STOP")
        self.btnPlay.pack(expand=1, fill=tk.BOTH, side=tk.LEFT, anchor=tk.SE)

        # =========== CREATION OF THE VIEW_MODEL ====================
        self.viewModel = BacktracksViewModel(self)
        # ===========================================================

        # after we have sent all the categories to the view, we trigger a function to the view which place all the category buttons on the ui
        self.setUiPlaceAllBtnCategories()
        # self.setUiShowMetronomeSection()
        self.setUiShowBacktrackSection()

        self.btnPlay.config(command=self.viewModel.onBtnPlayClick)
        self.btnRandom.config(command=self.viewModel.onBtnRandomClick)
        self.btnRecord.config(command=self.viewModel.onBtnRecordClick)

        self.btnMetro.config(command=self.viewModel.onBtnMetronomeClick)
        self.btnBpmPlus.config(command=self.viewModel.onBtnBpmPlusClick)
        self.btnBpmMinus.config(command=self.viewModel.onBtnBpmMinusClick)
        self.slTempo.bind("<ButtonRelease-1>", self.viewModel.onSliderTempoMoved)

    def setUiSpawnRecordWindow(self, current_backtrack_file: str):
        self.tempRecordView = tk.Toplevel()
        self.tempRecordView.geometry("%sx%s" % (env.FULL_SCREEN_W, env.FULL_SCREEN_H))
        if os.name != 'nt':
            self.tempRecordView.attributes('-fullscreen', True)
        RecordLickView(self.tempRecordView, current_backtrack_file)
        # self.tempRecordView.destroy()

    def setUiUnspawnRecordWindow(self):
        if self.tempRecordView is not None:
            self.tempRecordView.destroy()

    def setUiShowMetronomeSection(self):
        self.lblTrackTitle.pack_forget()
        self.lblCategory.pack_forget()
        self.progressBar.pack_forget()
        self.btnRecord.pack_forget()

        self.btnBpmPlus.pack(expand=1)
        self.lblMetro.pack(expand=1)
        self.btnBpmMinus.pack(expand=1)
        self.slTempo.pack(expand=1, fill=tk.X)

    def setUiShowBacktrackSection(self):
        self.btnBpmMinus.pack_forget()
        self.lblMetro.pack_forget()
        self.btnBpmPlus.pack_forget()
        self.slTempo.pack_forget()

        self.lblCategory.pack(expand=1, fill=tk.X)
        self.lblTrackTitle.pack(expand=1, fill=tk.BOTH)
        self.progressBar.pack(expand=1, fill=tk.X)
        self.btnRecord.pack(expand=1, fill=tk.X)

    def setUiLblMetronome(self, tempo: int):
        self.lblMetro.config(text=str(tempo))
        self.slTempo.set(tempo)

    def setUiUpdateProgress(self, percentage):
        self.progressBar.config(value=percentage)

    def setUiCurrentBacktrack(self, category: str, filename: str, index: int, category_length: int):
        self.lblCategory.config(text=category)
        text = "Playing {}\n({}/{})".format(filename, index + 1, category_length)
        self.lblTrackTitle.config(text=text)

    def setUiAddBtnCategory(self, category_id: int, category_name: str, quantity: int):
        btnLabel = category_name + " (" + str(quantity) + ")"
        self.backtracksCategoriesTuples.append((category_id, category_name, CustomButton(self.frameCategoryContainers, text=btnLabel), quantity))

    def setUiPlaceAllBtnCategories(self):
        starting_row = 0
        starting_column = 0
        columns_per_row = 2
        row_counter = starting_row
        column_counter = starting_column
        numberOfCategories = len(self.backtracksCategoriesTuples)
        numberOfRows = math.ceil(numberOfCategories / columns_per_row)
        for i in range(0, columns_per_row):
            self.frameCategoryContainers.grid_columnconfigure(i, weight=1)
        for i in range(0,numberOfRows):
            self.frameCategoryContainers.grid_rowconfigure(i, weight=1)
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
