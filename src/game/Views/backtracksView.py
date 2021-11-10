import math
import os
import tkinter.font
from functools import partial
from glob import glob
from tkinter import ttk

from PIL import Image, ImageTk

from src.game import env
from src.game.GamesNames import GameNames
from src.game.ViewModels.backtracksViewModel import BacktracksViewModel, BacktracksConstants
from src.game.Views.recordLickView import RecordLickView
from src.game.utils.customElements.customElements import *
from src.game.utils.customElements.labels import *
from src.game.utils.animations import DotsAnimations

BTN_PADDING_X = 0
BTN_PADDING_Y = 0
LEFT_PANEL_PADDING_X = 18
RIGHT_PANEL_PADDING_X = 18
RIGHT_PANEL_PADDING_Y = 18

FONT_SIZE_BTN_PLUS_AND_MINUS = 28


class ViewStrings(Enum):
    STRING_LBL_TRACK_TITLE = "Title : "
    STRING_LBL_TRACK_CATEGORY = "Category :"


class ViewImages:
    def __init__(self):
        self.IMAGE_PLAY_IMAGE = ImageTk.PhotoImage(Image.open(env.PLAY_IMAGE))
        self.IMAGE_PAUSE_IMAGE = ImageTk.PhotoImage(Image.open(env.PAUSE_IMAGE))
        self.IMAGE_SHUFFLE_IMAGE = ImageTk.PhotoImage(Image.open(env.SHUFFLE_IMAGE))
        self.IMAGE_METRONOME_IMAGE = ImageTk.PhotoImage(Image.open(env.METRONOME_IMAGE))
        self.IMAGE_RECORD_IMAGE = ImageTk.PhotoImage(Image.open(env.RECORD_IMAGE))


class BacktracksView:

    def __init__(self, master, game_frame: tk.Frame):
        print("launching game {}".format(GameNames.GAME_BACKTRACKS))
        self.images = ViewImages()
        self.master = master
        self.viewModel = None
        self.gameFrame = game_frame
        self.waveformImage = ImageTk.PhotoImage(Image.open(os.path.join(env.TEMP_FOLDER_FOR_WAVEFORM_TIMELINE_PNG, "empty_waveform_black.png")))
        if os.name != 'nt':
            self.gameFrame.config(cursor="none")
        self.backtracksCategoriesTuples = []

        self.animation = None
        self.tempRecordView = None
        self.container = tk.Frame(self.gameFrame, bg='red')
        self.container.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.popMessage = tk.Label(self.gameFrame,
                                   font=(DEFAULT_FONT_NAME, DEFAULT_FONT_SIZE, tkinter.font.ITALIC),
                                   text="Converting", bg=Colors.POPUP_BACKGROUND, fg=Colors.TEXT_WHITE)

        percentageLeft = 40 / 100
        self.frameLeft = tk.Frame(self.container, bg=Colors.BACKGROUND, padx=LEFT_PANEL_PADDING_X)
        self.frameLeft.place(x=0, y=0, width=env.GAME_SCREEN_W * percentageLeft, height=env.GAME_SCREEN_H)
        self.frameRight = tk.Frame(self.container, bg=Colors.BACKGROUND, padx=RIGHT_PANEL_PADDING_X, pady=RIGHT_PANEL_PADDING_Y)
        self.frameRight.place(x=env.GAME_SCREEN_W * percentageLeft, y=0, width=env.GAME_SCREEN_W * (1 - percentageLeft), height=env.GAME_SCREEN_H)

        # Backtrack Section
        self.lblTrackTitle = tk.Label(self.frameLeft, text=ViewStrings.STRING_LBL_TRACK_TITLE.value, justify=tk.CENTER,
                                      bg=Colors.BACKGROUND, fg=Colors.TEXT_WHITE,
                                      font=(DEFAULT_FONT_NAME, 14),
                                      width=20, wraplength=250, height=4)
        self.waveformFrame = tk.Button(self.frameLeft, image=self.waveformImage, bg='red', height=70)
        self.lblCategory = tk.Label(self.frameLeft,
                                    font=(DEFAULT_FONT_NAME, 24, tkinter.font.BOLD),
                                    bg=Colors.BACKGROUND,
                                    fg=Colors.TEXT_WHITE,
                                    # text=ViewStrings.STRING_LBL_TRACK_CATEGORY.value,
                                    justify=tk.CENTER)
        self.slSpeedVariation = CustomScale(self.frameLeft, from_=-1, to=1, resolution=.05, width=40)
        self.progressBar = ttk.Progressbar(self.frameLeft, style=CustomStylesNames.STYLE_CUSTOM_PROGRESSBAR.value, value=0)
        self.btnRecord = CustomButton(self.frameLeft, image=self.images.IMAGE_RECORD_IMAGE,
                                      background=Colors.BACKGROUND, height=80)

        # Metronome section
        self.btnBpmMinus = CustomButton(self.frameLeft, text="-", font=(DEFAULT_FONT_NAME, FONT_SIZE_BTN_PLUS_AND_MINUS, tkinter.font.BOLD))
        self.lblMetro = tk.Label(self.frameLeft,
                                 background=Colors.BACKGROUND, foreground=Colors.TEXT_WHITE,
                                 font=(DEFAULT_FONT_NAME, 80))
        self.btnBpmPlus = CustomButton(self.frameLeft, text="+", font=(DEFAULT_FONT_NAME, FONT_SIZE_BTN_PLUS_AND_MINUS, tkinter.font.BOLD))
        self.slTempo = CustomScale(self.frameLeft,
                                   from_=BacktracksConstants.TEMPO_MIN_BPM.value, to=BacktracksConstants.TEMPO_MAX_BPM.value,
                                   command=lambda event: self.lblMetro.config(text=str(event))
                                   )

        # Right Section
        self.frameCategoryContainers = tk.Frame(self.frameRight, bg=Colors.BACKGROUND)
        self.frameCategoryContainers.pack(expand=1, fill=tk.BOTH, pady=(0, RIGHT_PANEL_PADDING_Y))

        self.rowControls = tk.Frame(self.frameRight)
        self.rowControls.grid_rowconfigure(0, weight=1)
        self.rowControls.grid_rowconfigure(1, weight=2)
        self.rowControls.grid_columnconfigure(0, weight=1)
        self.rowControls.grid_columnconfigure(1, weight=1)
        self.btnMetro = CustomButton(self.rowControls, image=self.images.IMAGE_METRONOME_IMAGE)
        self.btnMetro.grid(row=0, column=0, sticky=tk.NSEW)
        self.btnRandom = CustomButton(self.rowControls, image=self.images.IMAGE_SHUFFLE_IMAGE)
        self.btnRandom.grid(row=1, column=0, sticky=tk.NSEW)
        self.btnPlay = CustomButton(self.rowControls, image=self.images.IMAGE_PLAY_IMAGE)
        self.btnPlay.grid(row=0, rowspan=2, column=1, sticky=tk.NSEW)
        self.rowControls.pack(expand=0, fill=tk.BOTH)

        # =========== CREATION OF THE VIEW_MODEL ====================
        self.viewModel = BacktracksViewModel(self)
        # ===========================================================

        # after we have sent all the categories to the view, we trigger a function to the view which place all the category buttons on the ui
        self.setUiPlaceAllBtnCategories()
        self.viewModel.switchToBacktrackGameMode()

        self.btnPlay.config(command=self.viewModel.onBtnPlayClick)
        self.btnRandom.config(command=self.viewModel.onBtnRandomClick)
        self.btnRecord.config(command=self.viewModel.onBtnRecordClick)
        self.btnMetro.config(command=self.viewModel.onBtnMetronomeClick)
        self.btnBpmPlus.config(command=self.viewModel.onBtnBpmPlusClick)
        self.btnBpmMinus.config(command=self.viewModel.onBtnBpmMinusClick)
        self.slTempo.bind("<ButtonRelease-1>", self.viewModel.onSliderTempoMoved)
        self.slSpeedVariation.bind("<ButtonRelease-1>", self.viewModel.onSliderSpeedVariationMoved)

    def setUiSpawnRecordWindow(self, current_backtrack_file: str):
        self.tempRecordView = tk.Toplevel()
        self.tempRecordView.geometry("%sx%s" % (env.FULL_SCREEN_W, env.FULL_SCREEN_H))
        if os.name != 'nt':
            self.tempRecordView.attributes('-fullscreen', True)
        RecordLickView(self.tempRecordView, current_backtrack_file)

    def resetSpeedVariationSlider(self):
        self.slSpeedVariation.set(0)

    def resetProgressBar(self):
        # TODO Doesn't work, i don't know why
        self.progressBar.config(value=0)
        self.progressBar.stop()

    def setUiUnspawnRecordWindow(self):
        if self.tempRecordView is not None:
            self.tempRecordView.destroy()

    def setUiShowMetronomeSection(self):
        self.lblTrackTitle.pack_forget()
        self.waveformFrame.pack_forget()
        self.lblCategory.pack_forget()
        self.progressBar.pack_forget()
        self.btnRecord.pack_forget()
        self.slSpeedVariation.pack_forget()

        self.btnBpmPlus.pack(expand=1, fill=tk.BOTH, padx=LEFT_PANEL_PADDING_X, pady=LEFT_PANEL_PADDING_X)
        self.lblMetro.pack(expand=1)
        self.slTempo.pack(expand=1, fill=tk.X, padx=LEFT_PANEL_PADDING_X)
        self.btnBpmMinus.pack(expand=1, fill=tk.BOTH, padx=LEFT_PANEL_PADDING_X, pady=LEFT_PANEL_PADDING_X)

    def setUiShowBacktrackSection(self):
        self.btnBpmMinus.pack_forget()
        self.lblMetro.pack_forget()
        self.btnBpmPlus.pack_forget()
        self.slTempo.pack_forget()

        self.lblCategory.pack(expand=1, fill=tk.X)
        self.lblTrackTitle.pack(expand=1, fill=tk.BOTH)
        self.slSpeedVariation.pack(expand=0, fill=tk.BOTH)
        self.waveformFrame.pack(expand=0, fill=tk.X)
        self.progressBar.pack(expand=0, fill=tk.X)
        self.btnRecord.pack(expand=1, fill=tk.X)

    def setUiLblMetronome(self, tempo: int):
        self.lblMetro.config(text=str(tempo))
        self.slTempo.set(tempo)

    def setUiUpdateProgress(self, percentage):
        self.progressBar.config(value=percentage)
        # self.progressBar.set(percentage/100)

    def setUiCurrentBacktrack(self, category: str, filename: str, index: int, category_length: int):
        category_text = "{} ({}/{})".format(category.upper(), index + 1, category_length)
        self.lblCategory.config(text=category_text)
        compressed_filename = filename[:50] + "..."
        text = "{}".format(compressed_filename)
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
        for i in range(0, numberOfRows):
            self.frameCategoryContainers.grid_rowconfigure(i, weight=1)
        for (category_id, category_name, category_btn, category_quantity) in self.backtracksCategoriesTuples:
            category_btn.config(command=partial(self.viewModel.onBtnCategoryClick, category_name))
            category_btn.grid(row=row_counter, column=column_counter, sticky=tk.NSEW, padx=BTN_PADDING_X, pady=BTN_PADDING_Y)
            column_counter += 1
            if column_counter >= starting_column + columns_per_row:
                column_counter = starting_column
                row_counter += 1

    def setUiChangePlayingIcons(self, is_playing: bool):
        if is_playing:
            self.btnPlay.config(image=self.images.IMAGE_PLAY_IMAGE)
        else:
            self.btnPlay.config(image=self.images.IMAGE_PAUSE_IMAGE)

    def setUiConvertInProgress(self):
        self.popMessage.place(relx=0.5, rely=0.5, relwidth=1, relheight=0.4, anchor=tk.CENTER)
        self.animation = DotsAnimations(self.popMessage, ["Converting", "Converting .", "Converting ..", "Converting ..."])
        self.animation.animate()

    def setUiConvertFinished(self):
        self.animation.stop()
        self.popMessage.place_forget()

    def setUiShowWaveform(self, waveform_png_file):
        print("SUCCCCCCCCCCESSSSS", waveform_png_file)
        # waveform_png_file = "D:\\aa.png"
        waveform_raw = Image.open(waveform_png_file)
        waveform_resized = waveform_raw.resize((self.waveformFrame.winfo_width(), self.waveformFrame.winfo_height()), Image.ANTIALIAS)
        self.waveform_image = ImageTk.PhotoImage(waveform_resized)
        print(self.waveform_image)
        # self.lblTrackTitle.config(image=waveform_image)
        self.waveformFrame.config(image=self.waveform_image)

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

    def destroy(self):
        print("Delete BacktracksView")
        self.viewModel.destroyViewModel()
