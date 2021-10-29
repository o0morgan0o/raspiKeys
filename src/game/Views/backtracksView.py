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

        self.gameFrame.grid_rowconfigure(0, weight=0)
        self.gameFrame.grid_rowconfigure(1, weight=0)
        self.gameFrame.grid_rowconfigure(2, weight=0)
        self.gameFrame.grid_rowconfigure(3, weight=0)
        self.gameFrame.grid_rowconfigure(4, weight=0)

        self.gameFrame.grid_columnconfigure(0, weight=1)
        self.gameFrame.grid_columnconfigure(1, weight=2)
        self.gameFrame.grid_columnconfigure(2, weight=2)
        self.gameFrame.grid_columnconfigure(3, weight=2)

        current_row = 0
        self.lblTrackTitle = ttk.Label(self.gameFrame, text=ViewStrings.STRING_LBL_TRACK_TITLE.value)
        self.lblTrackTitle.grid(row=current_row, column=0)
        current_row += 1
        self.lblCategory = ttk.Label(self.gameFrame, text=ViewStrings.STRING_LBL_TRACK_CATEGORY.value)
        self.lblCategory.grid(row=current_row, column=0)
        current_row += 1
        # this canvas contains the red bar progression
        self.canvas = tk.Canvas(self.gameFrame, height=10, bd=0, highlightthickness=0)
        self.canvas.grid(row=current_row, column=0)
        current_row += 1

        self.btnRecord = CustomButton(self.gameFrame, text="Record")
        self.btnRecord.grid(row=current_row, column=0)

        # Metro btn
        self.btnMetro = CustomButton(self.gameFrame, text="Metro")
        self.btnMetro.grid(row=current_row, column=1)
        self.btnBpmMinus = CustomButton(self.gameFrame, text="-")
        self.btnBpmMinus.grid(row=current_row, column=2)
        self.btnBpmPlus = CustomButton(self.gameFrame, text="+")
        self.btnBpmPlus.grid(row=current_row, column=3)
        current_row += 1

        # getting all folders in user wav
        self.wav_folders = self.getAllWavFolders()
        print('found folders : ', self.wav_folders)
        self.category_buttons = []
        for folder in self.wav_folders:
            all_files_in_folder = glob(env.PROCESSED_WAV_FOLDER + '/' + folder + '/*')
            button_text = folder + "\n(" + str(len(all_files_in_folder)) + ")"
            self.category_buttons.append(CustomButton(self.gameFrame, text=button_text))

        startColumn = 1
        columnCounter = startColumn
        for m_button in self.category_buttons:
            if columnCounter >= startColumn + 3:
                columnCounter = startColumn
                current_row += 1
            m_button.grid(row=current_row, column=columnCounter, sticky=tk.NSEW)
            columnCounter += 1

        # =========== CREATION OF THE VIEW_MODEL ====================
        self.viewModel = BacktracksViewModel(self)
        # ===========================================================

        # loop after creation of the viewModel for settings clickListeners
        for m_button in self.category_buttons:
            print(m_button)
            m_button.config(command=partial(self.viewModel.onBtnCategoryClick, id(m_button)))


        # self.game = BacktracksViewModel(self.master, self.gameFrame, config, app)
        # self.btnPlay = BtnBlack20(self.gameFrame, text="Play", activebackground="black")
        # self.btnRandom = BtnBlack20(self.gameFrame, text="Random", activebackground="black")
        # self.btnLick = BtnBlack20(self.gameFrame, text="Rec", wraplength="280", activebackground="black")

    @staticmethod
    def getAllWavFolders():
        raw_wav_folders = glob(env.PROCESSED_WAV_FOLDER + '/*/')
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

    def __del__(self):
        # self.destroy()
        pass

    # def activateListening(self):
    #     self.game.isListening = True

    # def destroy(self):
    #     print("trying destroy mode 2")
    #     self.game.destroy()
    #     del self
    #     pass
