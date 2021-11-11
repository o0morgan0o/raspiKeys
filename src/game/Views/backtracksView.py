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

WAVEFORM_TIMELINE_HEIGHT = 240


class ViewStrings(Enum):
    STRING_LBL_TRACK_TITLE = "Title : "
    STRING_LBL_TRACK_CATEGORY = "Category :"
    STRING_LBL_SLIDER_BACKTRACK = "Change tempo: "


class ViewImages:
    def __init__(self):
        self.IMAGE_PLAY_IMAGE = ImageTk.PhotoImage(Image.open(env.PLAY_IMAGE))
        self.IMAGE_PAUSE_IMAGE = ImageTk.PhotoImage(Image.open(env.PAUSE_IMAGE))
        self.IMAGE_SHUFFLE_IMAGE = ImageTk.PhotoImage(Image.open(env.SHUFFLE_IMAGE))
        self.IMAGE_METRONOME_IMAGE = ImageTk.PhotoImage(Image.open(env.METRONOME_IMAGE))
        self.IMAGE_RECORD_IMAGE = ImageTk.PhotoImage(Image.open(env.RECORD_IMAGE))
        self.IMAGE_ARROW_LEFT = ImageTk.PhotoImage(Image.open(env.ARROW_LEFT_IMAGE))
        self.IMAGE_ARROW_RIGHT = ImageTk.PhotoImage(Image.open(env.ARROW_RIGHT_IMAGE))


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

        # Backtrack Section
        self.animation = None
        self.tempRecordView = None
        self.backtracksCategoryContainer = tk.Frame(self.gameFrame, bg=Colors.BACKGROUND)
        self.backtracksCategoryContainer.pack(side=tk.TOP, fill=tk.BOTH)
        self.btnRandom = tk.Button(self.backtracksCategoryContainer, image=self.images.IMAGE_SHUFFLE_IMAGE, bg=Colors.BACKGROUND)
        self.btnRandom.pack(side=tk.RIGHT, fill=tk.BOTH, expand=1, ipadx=14 )

        self.waveFormContainer = tk.Frame(self.gameFrame, bg=Colors.BACKGROUND)
        self.waveformTimeline = tk.Button(self.waveFormContainer, image=self.waveformImage, height=WAVEFORM_TIMELINE_HEIGHT, borderwidth=0, highlightthickness=0)
        self.waveformTimeline.grid(row=0, column=0, sticky=tk.NSEW)
        self.popMessage = tk.Label(self.waveFormContainer,
                                   font=(DEFAULT_FONT_NAME, DEFAULT_FONT_SIZE, tkinter.font.ITALIC),
                                   text="Converting", bg=Colors.POPUP_BACKGROUND, fg=Colors.TEXT_WHITE)
        self.lblTrackTitle = tk.Label(self.waveFormContainer, text=ViewStrings.STRING_LBL_TRACK_TITLE.value,
                                      bg=Colors.WAVEFORM_BACKGROUND_COLOR, fg=Colors.TEXT_WHITE,
                                      font=(DEFAULT_FONT_NAME, 8, tkinter.font.ITALIC))
        self.lblTrackTitle.grid(row=0, column=0, sticky=tk.SW, padx=10)
        self.lblCategory = tk.Label(self.waveFormContainer,
                                    font=(DEFAULT_FONT_NAME, 8, tkinter.font.ITALIC),
                                    bg=Colors.WAVEFORM_BACKGROUND_COLOR, fg=Colors.TEXT_WHITE, )
        self.lblCategory.grid(row=0, column=0, sticky=tk.SE, padx=10)
        self.progressBar = ttk.Progressbar(self.waveFormContainer, style=CustomStylesNames.STYLE_CUSTOM_PROGRESSBAR.value, value=0)
        self.progressBar.grid(row=1, column=0, sticky=tk.NSEW)

        # Metronome section
        BTN_MINUS_PLUS_METRO_PADDING_INNER = 40
        self.metronomeContainer = tk.Frame(self.gameFrame, bg=Colors.BACKGROUND, height=WAVEFORM_TIMELINE_HEIGHT, )
        self.btnBpmMinus = tk.Button(self.metronomeContainer, image=self.images.IMAGE_ARROW_LEFT, background=Colors.BACKGROUND)
        self.btnBpmMinus.pack(side=tk.LEFT, ipadx=BTN_MINUS_PLUS_METRO_PADDING_INNER, ipady=BTN_MINUS_PLUS_METRO_PADDING_INNER)
        self.lblMetro = tk.Label(self.metronomeContainer,
                                 background=Colors.BACKGROUND, foreground=Colors.TEXT_WHITE,
                                 font=(DEFAULT_FONT_NAME, 80))
        self.lblMetro.pack(side=tk.LEFT, expand=1, fill=tk.BOTH)
        self.btnBpmPlus = tk.Button(self.metronomeContainer, image=self.images.IMAGE_ARROW_RIGHT, background=Colors.BACKGROUND)
        self.btnBpmPlus.pack(side=tk.LEFT, ipadx=BTN_MINUS_PLUS_METRO_PADDING_INNER, ipady=BTN_MINUS_PLUS_METRO_PADDING_INNER)

        # Bottom section
        self.bottomControlsContainer = tk.Frame(self.gameFrame, bg=Colors.BACKGROUND)
        self.bottomControlsContainer.pack(side=tk.BOTTOM, expand=0, fill=tk.BOTH, padx=20, pady=(6, 6))

        # slider for backtracks
        self.backtrackSliderContainer = tk.Frame(self.bottomControlsContainer, bg=Colors.BACKGROUND)
        self.lblSpeedVariation = tk.Label(self.backtrackSliderContainer, text="{}1x".format(ViewStrings.STRING_LBL_SLIDER_BACKTRACK.value), fg=Colors.TEXT_WHITE, bg=Colors.BACKGROUND, anchor=tk.W)
        self.lblSpeedVariation.pack(fill=tk.BOTH, ipady=0, pady=(20, 0))
        self.slSpeedVariation = CustomScale(self.backtrackSliderContainer, from_=-1, to=1, resolution=.05)
        self.slSpeedVariation.pack(side=tk.BOTTOM, expand=1, fill=tk.X, pady=(0, 0))

        # slider for metronome
        self.metronomeSliderContainer = tk.Frame(self.bottomControlsContainer, bg=Colors.BACKGROUND)
        self.lblMetronomeSlider = tk.Label(self.metronomeSliderContainer, text="Tempo: ", fg=Colors.TEXT_WHITE, bg=Colors.BACKGROUND, anchor=tk.W)
        self.lblMetronomeSlider.pack(fill=tk.BOTH, pady=(20, 0))
        self.slTempo = CustomScale(self.metronomeSliderContainer,
                                   from_=BacktracksConstants.TEMPO_MIN_BPM.value, to=BacktracksConstants.TEMPO_MAX_BPM.value,
                                   command=lambda event: self.lblMetro.config(text=str(event))
                                   )
        self.slTempo.pack(side=tk.LEFT, expand=1, fill=tk.X, pady=(0, 0))

        self.btnPlay = CustomButton(self.bottomControlsContainer, image=self.images.IMAGE_PLAY_IMAGE, width=100)
        self.btnPlay.pack(side=tk.RIGHT, fill=tk.BOTH)
        self.btnMetro = CustomButton(self.bottomControlsContainer, image=self.images.IMAGE_METRONOME_IMAGE)
        self.btnMetro.pack(side=tk.RIGHT, fill=tk.BOTH)
        self.btnRecord = CustomButton(self.bottomControlsContainer, image=self.images.IMAGE_RECORD_IMAGE, background=Colors.BACKGROUND, height=80)
        self.btnRecord.pack(side=tk.RIGHT, fill=tk.BOTH)

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

        # play a random backtrack when loading
        self.viewModel.onBtnRandomClick()


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

    def setUiUpdateSpeedVariationSlider(self, value):
        self.lblSpeedVariation.config(text="{}{:.1f}x".format(ViewStrings.STRING_LBL_SLIDER_BACKTRACK.value, 1+value/2))

    def setUiUnspawnRecordWindow(self):
        if self.tempRecordView is not None:
            self.tempRecordView.destroy()

    def setUiShowMetronomeSection(self):
        self.waveFormContainer.pack_forget()
        self.backtrackSliderContainer.pack_forget()

        self.metronomeSliderContainer.pack(side=tk.LEFT, expand=1, fill=tk.BOTH, padx=(0, 20))
        self.metronomeContainer.pack(expand=1, fill=tk.BOTH)

    def setUiShowBacktrackSection(self):
        self.metronomeSliderContainer.pack_forget()
        self.metronomeContainer.pack_forget()

        self.waveFormContainer.pack(side=tk.TOP, expand=1, fill=tk.BOTH)
        self.backtrackSliderContainer.pack(side=tk.LEFT, expand=1, fill=tk.BOTH, padx=(0, 20))

    def setUiLblMetronome(self, tempo: int):
        self.lblMetro.config(text=str(tempo))
        self.slTempo.set(tempo)

    def setUiUpdateProgress(self, percentage):
        self.progressBar.config(value=percentage)

    def setUiCurrentBacktrack(self, category: str, filename: str, index: int, category_length: int):
        category_text = "{} ({}/{})".format(category.upper(), index + 1, category_length)
        self.lblCategory.config(text=category_text)
        compressed_filename = filename[:110] + "..."
        text = "{}".format(compressed_filename)
        self.lblTrackTitle.config(text=text)

    def setUiAddBtnCategory(self, category_id: int, category_name: str, quantity: int):
        btnLabel = category_name + " (" + str(quantity) + ")"
        self.backtracksCategoriesTuples.append((category_id, category_name, CustomButton(self.backtracksCategoryContainer, text=btnLabel), quantity))

    def setUiPlaceAllBtnCategories(self):
        starting_row = 0
        starting_column = 0
        columns_per_row = 2
        row_counter = starting_row
        column_counter = starting_column
        numberOfCategories = len(self.backtracksCategoriesTuples)
        numberOfRows = math.ceil(numberOfCategories / columns_per_row)
        for (category_id, category_name, category_btn, category_quantity) in self.backtracksCategoriesTuples:
            category_btn.config(command=partial(self.viewModel.onBtnCategoryClick, category_name))
            category_btn.pack(side=tk.LEFT, expand=1, fill=tk.BOTH)
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
        waveform_raw = Image.open(waveform_png_file)
        waveform_resized = waveform_raw.resize((env.GAME_SCREEN_W, WAVEFORM_TIMELINE_HEIGHT), Image.ANTIALIAS)
        self.waveformImage = ImageTk.PhotoImage(waveform_resized)
        print(self.waveformImage)
        self.waveformTimeline.config(image=self.waveformImage)

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
