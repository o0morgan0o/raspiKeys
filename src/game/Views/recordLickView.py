import tkinter as tk
from tkinter import ttk
import os

from PIL import Image, ImageTk

from src.game.ViewModels.recordLickViewModel import RecordLickViewModel
from src.game.utils.colors import Colors
from src.game.utils.customElements.customElements import CustomButton, DEFAULT_FONT_NAME
from src.game.utils.customElements.customElements import CustomStylesNames
from src.game import env

DEFAULT_PADDING_X = 20
DEFAULT_PADDING_Y = 20

LBL_BACKTRACK_FONT_SIZE = 18
LBL_DEFAULT_FONT_SIZE = 24
LBL_ERROR_FONT_SIZE = 18
LBL_FONT_SIZE_VERY_BIG = 40
BTN_NUMBER_OF_LOOPS_PADDING_X = 20


class ViewImages:
    def __init__(self):
        self.IMAGE_RECORD_IMAGE = ImageTk.PhotoImage(Image.open(env.RECORD_IMAGE))


class RecordLickView:
    def __init__(self, record_frame, current_backtrack_file: str):
        self.recordFrame = record_frame
        self.recordFrame.config(bg=Colors.BACKGROUND)
        self.currentBacktrack = current_backtrack_file

        self.images = ViewImages()

        self.recordFrame.grid_rowconfigure(0)
        self.recordFrame.grid_rowconfigure(1, weight=1)
        self.recordFrame.grid_rowconfigure(2)
        self.recordFrame.grid_rowconfigure(3)
        self.recordFrame.grid_rowconfigure(4)
        self.recordFrame.grid_columnconfigure(0, weight=1)

        # ==============================
        # Frame containing error message
        self.frameError = tk.Frame(self.recordFrame, bg=Colors.ERROR)
        self.frameError.grid(row=4, column=0, sticky=tk.NSEW)
        self.lblError = tk.Label(self.frameError,
                                 text="",
                                 font=(DEFAULT_FONT_NAME, LBL_ERROR_FONT_SIZE),
                                 bg=Colors.ERROR,
                                 foreground=Colors.TEXT_WHITE
                                 )
        self.lblError.pack(side=tk.BOTTOM, fill=tk.BOTH, )

        # ==============================
        # Frame containing main logic
        self.frameGetKey = tk.Frame(self.recordFrame, bg=Colors.BACKGROUND)
        self.frameGetKey.grid(row=0, rowspan=2, column=0, sticky=tk.NSEW)
        self.lblLickKeyIndication = tk.Label(self.frameGetKey,
                                             background=Colors.BACKGROUND,
                                             foreground=Colors.TEXT_WHITE,
                                             text="Choose a Key", font=(DEFAULT_FONT_NAME, LBL_DEFAULT_FONT_SIZE))
        self.lblLickKeyIndication.pack(expand=1)
        self.lblLickKey = tk.Label(self.frameGetKey,
                                   background=Colors.BACKGROUND,
                                   foreground=Colors.TEXT_WHITE,
                                   text="?", font=(DEFAULT_FONT_NAME, LBL_FONT_SIZE_VERY_BIG))
        self.lblLickKey.pack(expand=1)

        # ==============================
        # Inner Frame for Number of loops settings
        self.frameRow1 = tk.Frame(self.frameGetKey, background=Colors.BACKGROUND)
        self.frameRow1.pack(expand=1)
        self.lblNumberOfLoopsIndicator = tk.Label(self.frameRow1,
                                                  background=Colors.BACKGROUND,
                                                  foreground=Colors.TEXT_WHITE,
                                                  text="Nb of loops:", font=(DEFAULT_FONT_NAME, LBL_DEFAULT_FONT_SIZE))
        self.lblNumberOfLoopsIndicator.pack(side=tk.LEFT)
        self.btnMinusNumberOfLoops = CustomButton(self.frameRow1, text="-")
        self.btnMinusNumberOfLoops.pack(side=tk.LEFT, padx=BTN_NUMBER_OF_LOOPS_PADDING_X)
        self.lblNumberOfLoops = tk.Label(self.frameRow1,
                                         background=Colors.BACKGROUND,
                                         foreground=Colors.TEXT_WHITE,
                                         text="", font=(DEFAULT_FONT_NAME, LBL_FONT_SIZE_VERY_BIG))
        self.lblNumberOfLoops.pack(side=tk.LEFT)
        self.btnPlusNumberOfLoops = CustomButton(self.frameRow1, text="+")
        self.btnPlusNumberOfLoops.pack(side=tk.LEFT, padx=BTN_NUMBER_OF_LOOPS_PADDING_X)
        # End of Inner Frame
        # ==============================

        self.btnReadyForRecording = CustomButton(self.frameGetKey, text="Record Chords")
        self.btnReadyForRecording.pack(expand=1)

        # ==============================
        # frame containing chord record logic
        self.frameRecordKey = tk.Frame(self.recordFrame, background=Colors.BACKGROUND)
        self.lblRecordReady = tk.Label(self.frameRecordKey,
                                       foreground=Colors.TEXT_WHITE,
                                       background=Colors.BACKGROUND,
                                       font=(DEFAULT_FONT_NAME, LBL_BACKTRACK_FONT_SIZE),
                                       text="READY, Pick a note to start")
        self.lblRecordReady.pack(expand=1)
        # self.lblRecordingInProgress = tk.Label(self.frameRecordKey, text="Recording in progress")
        self.lblRecordingInProgress = tk.Label(self.frameRecordKey,
                                               background=Colors.BACKGROUND,
                                               image=self.images.IMAGE_RECORD_IMAGE)

        # ==============================
        # frame containing finished recording
        self.frameFinishedRecording = tk.Frame(self.recordFrame,
                                               background=Colors.BACKGROUND
                                               )
        self.lblFinishedRecording = tk.Label(self.frameFinishedRecording,
                                             foreground=Colors.TEXT_WHITE,
                                             background=Colors.BACKGROUND,
                                             font=(DEFAULT_FONT_NAME, LBL_BACKTRACK_FONT_SIZE),
                                             text="Recording Finished !")
        self.lblFinishedRecording.pack(expand=1, fill=tk.BOTH)
        self.btnSave = CustomButton(self.frameFinishedRecording, text="Save Lick")
        self.btnSave.pack(expand=1)

        # ==============================
        # frame containing cancel button
        self.frameCancel = tk.Frame(self.recordFrame, bg="yellow")
        self.frameCancel.grid(row=0, column=0, sticky=tk.NW, padx=DEFAULT_PADDING_X, pady=DEFAULT_PADDING_Y)
        self.btnCancel = CustomButton(self.frameCancel, text="Cancel")
        self.btnCancel.pack()

        # Backtrack must be already visible so we pack it in the global recordFrame
        self.lblBacktrackName = tk.Label(self.recordFrame,
                                         text="Backtrack : BACKTRACK_NAME",
                                         font=(DEFAULT_FONT_NAME, LBL_BACKTRACK_FONT_SIZE),
                                         height=3,
                                         wraplength=500,
                                         background=Colors.BACKGROUND,
                                         foreground=Colors.TEXT_WHITE
                                         )
        self.lblBacktrackName.grid(row=2, sticky=tk.NSEW)
        self.progressBar = ttk.Progressbar(self.recordFrame, style=CustomStylesNames.STYLE_CUSTOM_PROGRESSBAR.value, value=0)
        self.progressBar.grid(row=3, sticky=tk.NSEW, padx=DEFAULT_PADDING_X, pady=DEFAULT_PADDING_Y)

        # =========== CREATION OF THE VIEW_MODEL ====================
        self.viewModel = RecordLickViewModel(self, current_backtrack_file)
        # ===========================================================
        self.btnReadyForRecording.config(command=lambda: self.viewModel.onBtnReadyForRecordingClick())
        self.btnMinusNumberOfLoops.config(command=lambda: self.viewModel.onBtnMinusNumberOfLoopsClick())
        self.btnPlusNumberOfLoops.config(command=lambda: self.viewModel.onBtnPlusNumberOfLoopsClick())
        self.btnCancel.config(command=lambda: self.viewModel.onBtnCancelClick())
        self.btnSave.config(command=lambda: self.viewModel.onBtnSaveClick())

        self.resetLblError()

    def resetLblError(self):
        self.frameError.grid_forget()
        self.lblError.config(text="")
        self.lblError.pack()

    def setUiShowMessage(self, message_string: str):
        pass

    def setUiShowError(self, error_string: str):
        self.frameError.grid(row=4, column=0, sticky=tk.NSEW)
        self.lblError.config(text=error_string)
        self.lblError.pack()

    def setUiInitializeView(self, backtrack_readable_name: str, number_of_loops_recording: int):
        filename = os.path.basename(backtrack_readable_name)
        self.lblBacktrackName.config(text="Backtrack:   {}".format(filename))
        self.lblNumberOfLoops.config(text=str(number_of_loops_recording))

    def setUiShowLickKey(self, human_readable_note: str):
        self.lblLickKey.config(text=human_readable_note)

    def setUiUpdateProgress(self, percentage_played: float):
        self.progressBar.config(value=percentage_played)

    def setUiFrameRecordingStarted(self):
        self.lblRecordReady.pack_forget()
        self.lblRecordingInProgress.pack(expand=1)

    def showUiFrameReadyForRecordingChords(self):
        self.frameGetKey.grid_forget()
        self.frameRecordKey.grid(row=0, rowspan=2, column=0, sticky=tk.NSEW)

    def showUiFrameFinishedRecording(self):
        self.frameRecordKey.grid_forget()
        self.frameFinishedRecording.grid(row=0, rowspan=2, column=0, sticky=tk.NSEW)
