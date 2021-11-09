import os
import tkinter.font
import tkinter as tk
from tkinter import ttk

from src.game.GamesNames import GameNames
from src.game.ViewModels.earTrainingNoteViewModel import EarTrainingNoteViewModel
from src.game.utils.customElements.customElements import *
from src.game.utils.customElements.labels import *
from src.game.utils.utilFunctions import formatOutputIntervalUnsigned


class GameStrings(Enum):
    LABEL_SLIDER_INTERVAL = "Max interval : "
    LABEL_SLIDER_NOTE_DELAY = "Delay (s) : "
    LABEL_PICK_NOTE = "Pick a starting note"
    LABEL_LISTEN = "Listen ..."
    LABEL_SCORE = "Score"
    LABEL_WHAT_IS_YOUR_ANSWER = "What is your answer ?"


class EarTrainingNoteView:
    def __init__(self, master, game_frame: tk.Frame):
        print("launching game {}".format(GameNames.GAME_EAR_TRAINING_NOTE))
        self.master = master
        self.viewModel = None
        self.gameFrame = game_frame
        if os.name != 'nt':
            self.gameFrame.config(cursor='none')

        DEFAULT_PADDING = 2
        current_row = 0

        self.gameFrame.grid_rowconfigure(0, weight=0, pad=DEFAULT_PADDING)
        self.gameFrame.grid_rowconfigure(1, weight=0)
        self.gameFrame.grid_rowconfigure(2, weight=1, pad=DEFAULT_PADDING)
        self.gameFrame.grid_rowconfigure(3, weight=1, pad=DEFAULT_PADDING)
        self.gameFrame.grid_rowconfigure(4, weight=1, pad=DEFAULT_PADDING)
        self.gameFrame.grid_columnconfigure(0, weight=1, uniform="col_width")
        self.gameFrame.grid_columnconfigure(1, weight=1, uniform="col_width")

        self.lblInterval = ttk.Label(self.gameFrame, text=GameStrings.LABEL_SLIDER_INTERVAL, style=CustomStylesNames.STYLE_LBL_FULL.value)
        self.lblInterval.grid(row=0, column=0, sticky=tk.EW, padx=10, pady=0)
        self.lblDelay = ttk.Label(self.gameFrame, text=GameStrings.LABEL_SLIDER_NOTE_DELAY, style=CustomStylesNames.STYLE_LBL_FULL.value)
        self.lblDelay.grid(row=0, column=1, sticky=tk.EW, padx=10, pady=0)

        current_row += 1

        self.slInterval = CustomScale(self.gameFrame, from_=3, to=18)
        self.slInterval.grid(row=current_row, column=0, sticky=tk.EW, padx=(10, 10))
        self.slDelay = CustomScale(self.gameFrame, from_=0.2, to=1, resolution=0.05)
        self.slDelay.grid(row=current_row, column=1, sticky=tk.EW, padx=(10, 10))

        current_row += 1

        self.pickNote = CustomLabel(self.gameFrame, text=GameStrings.LABEL_PICK_NOTE)  # for user instructions
        self.pickNote.grid(row=current_row, columnspan=2)

        current_row += 1

        self.lblNoteUser = CustomLabel(self.gameFrame, justify=tk.LEFT, font=(DEFAULT_FONT_NAME, 90, tk.font.BOLD), text="", padx=32)
        self.lblNoteUser.grid(row=current_row, column=1, sticky=tk.NSEW)

        self.lblNote = CustomLabel(self.gameFrame, justify=tk.RIGHT, font=(DEFAULT_FONT_NAME, 90, tk.font.BOLD), text="?", padx=32)
        self.lblNote.grid(row=current_row, column=0, columnspan=2, sticky=tk.NSEW)

        current_row += 1

        self.result = CustomLabel(self.gameFrame, padx=10, pady=10, font=(DEFAULT_FONT_NAME, 18, tk.font.BOLD), text="", height=2)
        self.result.grid(row=current_row, columnspan=2)

        current_row += 1

        # self.btnSkip = CustomButton(self.gameFrame, text="SKIP", filename="btn_round.png")
        self.btnSkip = CustomButton(self.gameFrame, text="Skip")
        self.btnSkip.grid(row=0, rowspan=current_row, column=0, columnspan=2, sticky=tk.SE, padx=12, pady=12)

        self.score = CustomLabel(self.gameFrame, font=(DEFAULT_FONT_NAME, DEFAULT_FONT_SIZE, tk.font.BOLD), text=GameStrings.LABEL_SCORE.value)
        self.score.grid(row=0, rowspan=current_row, column=0, sticky=tk.SW, padx=12, pady=12)

        # =========== CREATION OF THE VIEW_MODEL ====================
        self.viewModel = EarTrainingNoteViewModel(self)
        # ===========================================================
        self.btnSkip.config(command=self.viewModel.skipQuestionCallback)
        self.slInterval.bind("<ButtonRelease-1>", self.viewModel.updateSliderIntervalCallback)
        self.slDelay.bind("<ButtonRelease-1>", self.viewModel.updateSliderDelayCallback)

        self.lblInterval.config(text=GameStrings.LABEL_SLIDER_INTERVAL.value + formatOutputIntervalUnsigned(self.slInterval.get()))
        self.lblDelay.config(text=GameStrings.LABEL_SLIDER_NOTE_DELAY.value + str(self.slDelay.get()))

    def reinitializeUi(self):
        self.pickNote.config(text=GameStrings.LABEL_PICK_NOTE.value)

    def updateLblMaxInterval(self, value: int):
        self.lblInterval.config(text=GameStrings.LABEL_SLIDER_INTERVAL.value + formatOutputIntervalUnsigned(value))

    def updateLblNoteDelay(self, value: float):
        self.lblDelay.config(text=GameStrings.LABEL_SLIDER_NOTE_DELAY.value + str(value))

    def setUiStateSetNoteQuestion(self, origin_note_readable: str):
        self.pickNote.config(text=GameStrings.LABEL_LISTEN.value)
        self.lblNote.config(text=origin_note_readable)
        self.lblNote.grid(column=0, columnspan=2, sticky=tk.NSEW)
        self.lblNoteUser.config(text="")
        self.result.config(text="", background=Colors.BACKGROUND)

    def setUiStateWaitingAnswer(self):
        self.pickNote.config(text=GameStrings.LABEL_WHAT_IS_YOUR_ANSWER.value)
        self.result.config(text="", background=Colors.BACKGROUND)
        self.lblNoteUser.config(text="")

        self.lblNote.config(justify=tk.CENTER)
        self.lblNote.grid(column=0, columnspan=2, sticky=tk.NSEW)

    def setUiStateShowingResult(self, note_user_readable: str):
        self.lblNoteUser.config(text=note_user_readable)

    def setUiStateWin(self, question_note_readable: str, interval_readable_text: str):
        self.result.config(text="correct ;->\n{}".format(interval_readable_text), bg=Colors.SUCCESS)
        self.lblNoteUser.config(text=question_note_readable, fg=Colors.SUCCESS, justify=tk.LEFT)
        self.lblNoteUser.grid(sticky=tk.W + tk.NS)
        # we move the lblNote from center to the left, because we want to see both notes labels
        self.lblNote.config(justify=tk.RIGHT)
        self.lblNote.grid(column=0, columnspan=1, sticky=tk.E + tk.NS)

    def setUiStateLoose(self, user_note_readable: str, interval_readable_text: str):
        # self.result.config(text="incorrect \n{}".format(interval_readable_text), bg=Colors.ERROR)
        # self.lblNoteUser.config(text=user_note_readable, fg=Colors.ERROR)
        pass

    def setUiStateSkippedQuestion(self, question_note_readable: str, interval_readable_text: str):
        self.result.config(text="It was ;->\n{}".format(interval_readable_text), bg=Colors.WARNING)
        self.lblNoteUser.config(text=question_note_readable, fg=Colors.WARNING)
        # we move the lblNote from center to the left, because we want to see both notes labels
        self.lblNote.config(justify=tk.RIGHT)
        self.lblNote.grid(column=0, columnspan=1, sticky=tk.NSEW)

    def destroy(self):
        print('Delete EarTrainingNoteView')
        self.viewModel.destroyViewModel()
