import tkinter as tk
from tkinter import ttk

from src.game.ViewModels.recordLickViewModel import RecordLickViewModel
from src.game.utils.colors import Colors
from src.game.utils.customElements.customElements import CustomButton
from src.game.utils.customElements.customElements import CustomStylesNames


class RecordLickView:
    def __init__(self, record_frame, current_backtrack_file: str):
        self.recordFrame = record_frame
        self.recordFrame.config(bg=Colors.BACKGROUND)
        self.currentBacktrack = current_backtrack_file

        self.recordFrame.grid_rowconfigure(0)
        self.recordFrame.grid_rowconfigure(1, weight=1)
        self.recordFrame.grid_rowconfigure(2, weight=1)
        self.recordFrame.grid_rowconfigure(3)
        self.recordFrame.grid_rowconfigure(4)
        self.recordFrame.grid_columnconfigure(0, weight=1)

        # ==============================
        # Frame containing error message
        self.frameError = tk.Frame(self.recordFrame)
        self.frameError.grid(row=4, column=0, sticky=tk.NSEW)
        self.lblError = tk.Label(self.frameError, text="")
        self.lblError.pack(side=tk.BOTTOM, fill=tk.BOTH)

        # ==============================
        # Frame containing main logic
        self.frameGetKey = tk.Frame(self.recordFrame, bg="green")
        self.frameGetKey.grid(row=0, rowspan=2, column=0, sticky=tk.NSEW)
        self.lblLickKeyIndication = tk.Label(self.frameGetKey, text="What is the key ? (Pick note)")
        self.lblLickKeyIndication.pack(expand=1)
        self.lblLickKey = tk.Label(self.frameGetKey, text="?")
        self.lblLickKey.pack(expand=1)

        # ==============================
        # Inner Frame for Number of loops settings
        self.frameRow1 = tk.Frame(self.frameGetKey)
        self.frameRow1.pack(expand=1)
        self.lblNumberOfLoopsIndicator = tk.Label(self.frameRow1, text="Nb of loops:")
        self.lblNumberOfLoopsIndicator.pack(side=tk.LEFT)
        self.btnMinusNumberOfLoops = CustomButton(self.frameRow1, text="-")
        self.btnMinusNumberOfLoops.pack(side=tk.LEFT)
        self.lblNumberOfLoops = tk.Label(self.frameRow1, text="")
        self.lblNumberOfLoops.pack(side=tk.LEFT)
        self.btnPlusNumberOfLoops = CustomButton(self.frameRow1, text="+")
        self.btnPlusNumberOfLoops.pack(side=tk.LEFT)
        # End of Inner Frame
        # ==============================

        self.btnReadyForRecording = CustomButton(self.frameGetKey, text="Record Chords")
        self.btnReadyForRecording.pack(expand=1)

        # ==============================
        # frame containing chord record logic
        self.frameRecordKey = tk.Frame(self.recordFrame, bg="orange")
        self.lblRecordReady = tk.Label(self.frameRecordKey, text="READY, Pick a note to start")
        self.lblRecordReady.pack(expand=1)
        self.lblRecordingInProgress = tk.Label(self.frameRecordKey, text="Recording in progress")

        # ==============================
        # frame containing finished recording
        self.frameFinishedRecording = tk.Frame(self.recordFrame, bg="green")
        self.lblFinishedRecording = tk.Label(self.frameFinishedRecording, text="Finished recording")
        self.lblFinishedRecording.pack(expand=1)
        self.btnSave = CustomButton(self.frameFinishedRecording, text="Save Lick")
        self.btnSave.pack(expand=1)

        # ==============================
        # frame containing cancel button
        self.frameCancel = tk.Frame(self.recordFrame, bg="yellow")
        self.frameCancel.grid(row=0, column=0, sticky=tk.NW)
        self.btnCancel = tk.Button(self.frameCancel, text="Cancel")
        self.btnCancel.pack()

        # Backtrack must be already visible so we pack it in the global recordFrame
        self.lblBacktrackName = tk.Label(self.recordFrame, text="Backtrack : BACKTRACK_NAME")
        self.lblBacktrackName.grid(row=2, sticky=tk.NSEW)
        self.progressBar = ttk.Progressbar(self.recordFrame, style=CustomStylesNames.STYLE_PROGRESSBAR_RED.value, value=0)
        self.progressBar.grid(row=3, sticky=tk.NSEW)

        # =========== CREATION OF THE VIEW_MODEL ====================
        self.viewModel = RecordLickViewModel(self, current_backtrack_file)
        # ===========================================================
        self.btnReadyForRecording.config(command=lambda: self.viewModel.onBtnReadyForRecordingClick())
        self.btnMinusNumberOfLoops.config(command=lambda: self.viewModel.onBtnMinusNumberOfLoopsClick())
        self.btnPlusNumberOfLoops.config(command=lambda: self.viewModel.onBtnPlusNumberOfLoopsClick())
        self.btnCancel.config(command=lambda: self.viewModel.onBtnCancelClick())
        self.btnSave.config(command= lambda :self.viewModel.onBtnSaveClick())

    def resetLblError(self):
        self.lblError.config(text="")
        self.lblError.pack()

    def setUiShowMessage(self, message_string:str):
        pass

    def setUiShowError(self, error_string: str):
        self.lblError.config(text=error_string, bg="red")
        self.lblError.pack()

    def setUiInitializeView(self, backtrack_readable_name: str, number_of_loops_recording: int):
        self.lblBacktrackName.config(text=backtrack_readable_name)
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

    # def destroy(self):
        # print('DELLLLLLLLLLLLLLLLL')
        # self.master.setUiUnspawnRecordWindow()
        # self.recordFrame.setUiShowMetronomeSection()
        # self.recordFrame.quit()
        # del self
        # pass
