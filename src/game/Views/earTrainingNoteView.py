from src.game.Views.navbarView import GameNames
from src.game.utils.colors import Colors
from src.game.utils.customElements.buttons import *
from src.game.utils.customElements.labels import *
from src.game.ViewModels.earTrainingNoteViewModel import EarTrainingNoteViewModel
from enum import Enum
from tkinter import ttk


class GameStrings(Enum):
    LABEL_PICK_NOTE = "Pick a starting note"
    LABEL_LISTEN = "Listen ..."
    LABEL_WHAT_IS_YOUR_ANSWER = "What is your answer ?"


class EarTrainingNoteView:
    def __init__(self, master, game_frame: tk.Frame):
        print("launching game {}".format(GameNames.GAME_EAR_TRAINING_NOTE))
        self.master = master
        self.viewModel = None
        self.gameFrame = game_frame

        DEFAULT_PADDING = 3
        current_row = 0

        self.gameFrame.grid_rowconfigure(0, weight=1, pad=DEFAULT_PADDING)
        self.gameFrame.grid_rowconfigure(1, weight=1, pad=DEFAULT_PADDING)
        self.gameFrame.grid_rowconfigure(2, weight=1, pad=DEFAULT_PADDING)
        self.gameFrame.grid_columnconfigure(0, weight=1, pad=DEFAULT_PADDING)
        self.gameFrame.grid_columnconfigure(1, weight=1, pad=DEFAULT_PADDING)

        self.slInterval = tk.Scale(self.gameFrame, from_=3, to=18, orient=tk.HORIZONTAL, width=40, label="Interval Max", showvalue=0)
        self.slInterval.grid(row=0, column=0, sticky=tk.EW, padx=(10, 10))

        self.slDelay = tk.Scale(self.gameFrame, from_=200, to=1000, orient=tk.HORIZONTAL, width=40, label="Note Delay", showvalue=0)
        self.slDelay.grid(row=0, column=1, sticky=tk.EW, padx=(10, 10))

        current_row += 1

        self.pickNote = MyLabel18(self.gameFrame)  # for user instructions
        self.pickNote.config(font=("Courier", 24), text="pickNote")
        self.pickNote.grid(row=current_row, columnspan=2)

        current_row += 1

        self.lblNote = MyLabel40(self.gameFrame, justify="right")
        self.lblNote.config(font=("Courier", 120, "bold"), text="?")
        self.lblNote.grid(row=current_row, column=0, sticky=tk.E, padx=(0, 12))

        self.lblNoteUser = MyLabel40(self.gameFrame)
        self.lblNoteUser.config(font=("Courier", 120, "bold"), text="", justify="left")
        self.lblNoteUser.grid(row=current_row, column=1, sticky=tk.W, padx=(12, 0))

        current_row += 1

        self.result = MyLabel18(self.gameFrame, padx=10, pady=10)
        self.result.config(font=("Courier", 18, "bold"), text="")
        self.result.grid(row=current_row, columnspan=2)

        current_row += 1

        self.btnSkip = BtnBlack20(self.gameFrame, text="SKIP >")
        self.btnSkip.config(bd=0, highlightthickness=0)
        self.btnSkip.grid(row=current_row, column=1, sticky=tk.SE, padx=12, pady=12)

        self.score = MyLabel30(self.gameFrame, )  # for global score
        self.score.config(font=("Courier", 10, "bold"), text="SCORE")
        self.score.grid(row=current_row, column=0, sticky=tk.SW, padx=12,pady=12)

        current_row += 1

        self.viewModel = EarTrainingNoteViewModel(self)
        self.slInterval.bind("<ButtonRelease-1>", self.viewModel.updateSliderIntervalCallback)
        self.slDelay.bind("<ButtonRelease-1>", self.viewModel.updateSliderDelayCallback)

    def reinitializeUi(self):
        self.pickNote.config(text=GameStrings.LABEL_PICK_NOTE.value)

    def setUiStateSetNoteQuestion(self, origin_note_readable: str):
        self.pickNote.config(text=GameStrings.LABEL_LISTEN.value)
        self.lblNote.config(text=origin_note_readable)
        self.lblNoteUser.config(text="")

    def setUiStateWaitingAnswer(self):
        self.pickNote.config(text=GameStrings.LABEL_WHAT_IS_YOUR_ANSWER.value)
        self.result.config(text="")
        self.lblNoteUser.config(text="")

    def setUiStateShowingResult(self, note_user_readable: str):
        self.lblNoteUser.config(text=note_user_readable)

    def setUiStateWin(self, question_note_readable:str, interval_readable_text: str):
        self.result.config(text="correct ;->\n{}".format(interval_readable_text), bg=Colors.success)
        self.lblNoteUser.config(text=question_note_readable, fg=Colors.success)

    def setUiStateLoose(self, user_note_readable:str, interval_readable_text: str):
        self.result.config(text="incorrect \n{}".format(interval_readable_text), bg=Colors.error)
        self.lblNoteUser.config(text=user_note_readable, fg=Colors.error)

    def __del__(self):
        pass
