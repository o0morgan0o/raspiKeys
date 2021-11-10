import os
import tkinter.font
from tkinter import ttk

from src.game.GamesNames import GameNames
from src.game.ViewModels.earTrainingChordViewModel import EarTrainingChordViewModel
from src.game.utils.customElements.customElements import *
from src.game.utils.customElements.labels import *


class GameStrings(Enum):
    LABEL_SLIDER_NOTE_DELAY = "Delay (s): "
    LABEL_SLIDER_NOTE_DURATION = "Note duration (s): "
    LABEL_PICK_NOTE = "Pick a starting note"
    LABEL_LISTEN = "Listen ..."
    LABEL_SCORE = "Score"
    LABEL_WHAT_IS_YOUR_ANSWER = "What is your answer ?"


# TODO add keyboard View

class EarTrainingChordView:
    def __init__(self, master, game_frame: tk.Frame):
        print("launching game {}".format(GameNames.GAME_EAR_TRAINING_CHORDS))
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

        self.lblDelay = ttk.Label(self.gameFrame, text=GameStrings.LABEL_SLIDER_NOTE_DELAY, style=CustomStylesNames.STYLE_LBL_FULL.value)
        self.lblDelay.grid(row=0, column=1, sticky=tk.EW, padx=10, pady=0)

        self.lblNoteDuration = ttk.Label(self.gameFrame, text=GameStrings.LABEL_SLIDER_NOTE_DURATION, style=CustomStylesNames.STYLE_LBL_FULL.value)
        self.lblNoteDuration.grid(row=0,column=0, sticky=tk.EW, padx=10,pady=10)

        current_row += 1

        self.slDelay = CustomScale(self.gameFrame, from_=0.05, to=1, resolution=0.05)
        self.slDelay.grid(row=current_row, column=1, sticky=tk.EW, padx=(10, 10))

        self.slDuration = CustomScale(self.gameFrame, from_=.05, to=1.5, resolution=0.05)
        self.slDuration.grid(row=current_row, column=0, sticky=tk.EW, padx=(10,10))

        current_row += 1

        self.pickNote = CustomLabel(self.gameFrame, text=GameStrings.LABEL_PICK_NOTE)  # for user instructions
        self.pickNote.grid(row=current_row, columnspan=2)

        current_row += 1

        self.lblNoteUser = CustomLabel(self.gameFrame, justify=tk.LEFT, font=(DEFAULT_FONT_NAME, 90, tkinter.font.BOLD), text="", padx=32)
        self.lblNoteUser.grid(row=current_row, column=1, sticky=tk.NSEW)

        self.lblNote = CustomLabel(self.gameFrame, justify=tk.RIGHT, font=(DEFAULT_FONT_NAME, 90, tkinter.font.BOLD), text="?", padx=32)
        self.lblNote.grid(row=current_row, column=0, columnspan=2, sticky=tk.NSEW)

        current_row += 1

        self.result = CustomLabel(self.gameFrame, padx=10, pady=10, font=(DEFAULT_FONT_NAME, 18, tkinter.font.BOLD), text="", height=2)
        self.result.grid(row=current_row, columnspan=2)

        current_row += 1

        self.btnSkip = CustomButton(self.gameFrame, text="Skip")
        self.btnSkip.grid(row=0, rowspan=current_row, column=0, columnspan=2, sticky=tk.SE, padx=12, pady=12)

        self.score = CustomLabel(self.gameFrame, font=(DEFAULT_FONT_NAME, DEFAULT_FONT_SIZE, tkinter.font.BOLD), text=GameStrings.LABEL_SCORE.value)
        self.score.grid(row=0, rowspan=current_row, column=0, sticky=tk.SW, padx=12, pady=12)

        # =========== CREATION OF THE VIEW_MODEL ====================
        self.viewModel = EarTrainingChordViewModel(self)
        # ===========================================================
        self.slDelay.bind('<ButtonRelease-1>', self.viewModel.onSliderDelayMoved)
        self.slDuration.bind('<ButtonRelease-1>', self.viewModel.onSliderDurationMoved)

    def reinitializeUi(self):
        self.pickNote.config(text=GameStrings.LABEL_PICK_NOTE.value)

    def updateLblNoteDelay(self, value: float):
        self.lblDelay.config(text=GameStrings.LABEL_SLIDER_NOTE_DELAY.value + str(value))

    def updateLblNoteDuration(self, value: float):
        self.lblNoteDuration.config(text=GameStrings.LABEL_SLIDER_NOTE_DURATION.value + str(value))

    def setUiStateChordQuestion(self, origin_note_readable: str):
        self.pickNote.config(text=GameStrings.LABEL_LISTEN.value)
        self.lblNote.config(text=origin_note_readable)
        self.result.config(text="")

    def setUiStateWaitingAnswer(self):
        self.pickNote.config(text=GameStrings.LABEL_WHAT_IS_YOUR_ANSWER.value)

    def setUiStateWin(self, origin_note: str, chord_quality: str, human_readable_notes: list):
        text_answer = "{} {}".format(origin_note, chord_quality)
        note_list = ""
        for note in human_readable_notes:
            note_list += "{} ".format(note)
        self.result.config(text="correct {}\n({})".format(text_answer, note_list), bg=Colors.SUCCESS)

    def setUiStateLoose(self):
        self.result.config(text="INCORRECT", bg=Colors.ERROR)

    def destroy(self):
        print('Delete EarTrainingChordView')
        self.viewModel.destroyViewModel()
