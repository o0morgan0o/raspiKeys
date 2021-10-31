from glob import glob
from functools import partial

from PIL import Image, ImageTk
from src.game import env
from src.game.Views.navbarView import GameNames
from src.game.utils.customElements.customElements import *
from src.game.utils.customElements.labels import *
from src.game.ViewModels.backtracksViewModel import BacktracksViewModel
from enum import Enum


# from src.game.ViewModels.backtracksViewModel import BacktracksViewModel
BTN_PADDING_X = 3
BTN_PADDING_Y = 4
LEFT_PANEL_PADDING_X = 20


class ViewStrings(Enum):
    STRING_LBL_TRACK_TITLE = "Title : "
    STRING_LBL_TRACK_CATEGORY = "Categ. :"


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
        self.gameFrame.grid_rowconfigure(5, uniform='row_height', weight=1)
        self.gameFrame.grid_rowconfigure(6, uniform='row_height', weight=1)
        self.gameFrame.grid_rowconfigure(7, uniform='row_height', weight=1)
        self.gameFrame.grid_rowconfigure(8, uniform='row_height', weight=1)

        self.gameFrame.grid_columnconfigure(0)
        self.gameFrame.grid_columnconfigure(1, uniform='column_width', weight=1)
        self.gameFrame.grid_columnconfigure(2, uniform='column_width', weight=1)
        self.gameFrame.grid_columnconfigure(3, uniform='column_width', weight=1)

        self.lblTrackTitle = tk.Label(self.gameFrame, text=ViewStrings.STRING_LBL_TRACK_TITLE.value, justify="center", width=40, wraplength=200)
        self.lblTrackTitle.grid(row=3, rowspan=1, column=0, sticky=tk.NSEW, padx=LEFT_PANEL_PADDING_X)

        self.lblCategory = ttk.Label(self.gameFrame, text=ViewStrings.STRING_LBL_TRACK_CATEGORY.value)
        self.lblCategory.grid(row=4, column=0, padx=LEFT_PANEL_PADDING_X)

        self.progress = ttk.Progressbar(self.gameFrame, style="danger.Horizontal.TProgressbar", value=0)
        self.progress.grid(row=5, column=0, sticky=tk.NSEW, padx=LEFT_PANEL_PADDING_X)

        self.btnRecord = CustomButton(self.gameFrame, text="Record")
        self.btnRecord.grid(row=7, column=0,sticky=tk.NSEW, padx=LEFT_PANEL_PADDING_X)

        self.lblMetro = ttk.Label(self.gameFrame, style=CustomStylesNames.STYLE_LBL_FULL.value, text="metroValue")
        self.lblMetro.grid(row=0, column=2, padx=LEFT_PANEL_PADDING_X)

        # Metro btn
        current_row = 1
        self.btnMetro = CustomButton(self.gameFrame, text="Metro")
        self.btnMetro.grid(row=current_row, column=1, sticky=tk.NSEW, padx=BTN_PADDING_X, pady=BTN_PADDING_Y)

        self.btnBpmMinus = CustomButton(self.gameFrame, text="-")
        self.btnBpmMinus.grid(row=current_row, column=2, sticky=tk.NSEW, padx=BTN_PADDING_X, pady=BTN_PADDING_Y)
        self.btnBpmPlus = CustomButton(self.gameFrame, text="+")
        self.btnBpmPlus.grid(row=current_row, column=3,sticky=tk.NSEW, padx=BTN_PADDING_X,pady=BTN_PADDING_Y)

        current_row = 6
        self.btnRandom = CustomButton(self.gameFrame, text="Random")
        self.btnRandom.grid(row=current_row, column=1, sticky=tk.NSEW, padx=BTN_PADDING_X, pady=BTN_PADDING_Y)

        self.btnPlay = CustomButton(self.gameFrame, text="PLAY/STOP")
        self.btnPlay.grid(row=current_row, column=2, columnspan=2, sticky=tk.NSEW, padx=BTN_PADDING_X, pady=BTN_PADDING_Y)


        # =========== CREATION OF THE VIEW_MODEL ====================
        self.viewModel = BacktracksViewModel(self)
        # ===========================================================

        # after we have sent all the categories to the view, we trigger a function to the view which place all the category buttons on the ui
        self.setUiPlaceAllBtnCategories()

        self.btnPlay.config(command=self.viewModel.onBtnPlayClick)
        self.btnRandom.config(command=self.viewModel.onBtnRandom)

        self.btnMetro.config(command=self.viewModel.onBtnMetronomeClick)
        self.btnBpmPlus.config(command=self.viewModel.onBtnBpmPlusClick)
        self.btnBpmMinus.config(command=self.viewModel.onBtnBpmMinusClick)

        # self.game = BacktracksViewModel(self.master, self.gameFrame, config, app)
        # self.btnPlay = BtnBlack20(self.gameFrame, text="Play", activebackground="black")
        # self.btnRandom = BtnBlack20(self.gameFrame, text="Random", activebackground="black")
        # self.btnLick = BtnBlack20(self.gameFrame, text="Rec", wraplength="280", activebackground="black")

    def setUiLblMetronome(self, tempo: int):
        self.lblMetro.config(text=str(tempo))

    def setUiUpdateProgress(self, percentage):
        self.progress.config(value=percentage)

    def setUiCurrentBacktrack(self, category: str, filename: str, index: int, category_length: int):
        self.lblCategory.config(text=category)
        text = "Playing {}\n({}/{})".format(filename, index + 1, category_length)
        self.lblTrackTitle.config(text=text)

    def setUiAddBtnCategory(self, category_id: int, category_name: str, quantity: int):
        btnLabel = category_name + " (" + str(quantity) + ")"
        self.backtracksCategoriesTuples.append((category_id, CustomButton(self.gameFrame, text=btnLabel), quantity))

    def setUiPlaceAllBtnCategories(self):
        starting_row = 3
        starting_column = 1
        columns_per_row = 3
        row_counter = starting_row
        column_counter = starting_column
        for (category_id, category_btn, category_quantity) in self.backtracksCategoriesTuples:
            category_btn.config(command=partial(self.viewModel.onBtnCategoryClick, category_id))
            category_btn.grid(row=row_counter, column=column_counter, sticky=tk.NSEW, padx=BTN_PADDING_X, pady=BTN_PADDING_Y)
            column_counter += 1
            if column_counter >= starting_column + columns_per_row:
                column_counter = starting_column
                row_counter += 1

    def __del__(self):
        # self.destroy()
        pass

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

    # def activateListening(self):
    #     self.game.isListening = True

    # def destroy(self):
    #     print("trying destroy mode 2")
    #     self.game.destroy()
    #     del self
    #     pass
