import tkinter as tk
from tkinter import ttk

from src.game import env
from src.game.GamesNames import GameNames
from src.game.ViewModels.practiseLicksViewModel import PractiseLicksViewModel, JsonLickFields
from src.game.utils.colors import Colors
from src.game.utils.customElements.customElements import CustomStylesNames, CustomButton, DEFAULT_FONT_NAME
from src.game.utils.midiToNotenames import noteNameFull

DEFAULT_PADDING_X = 20
DEFAULT_PADDING_Y = 20


class PractiseLicksView:
    def __init__(self, master, game_frame: tk.Frame):
        print("launching game {}".format(GameNames.GAME_LICKS_PRACTISE))
        self.master = master
        self.viewModel = None
        self.gameFrame = game_frame

        percentageLeft = 40 / 100
        self.frameLeft = tk.Frame(self.gameFrame, bg=Colors.BACKGROUND)
        self.frameLeft.place(x=0, y=0, width=env.GAME_SCREEN_W * percentageLeft, height=env.GAME_SCREEN_H)
        self.frameRight = tk.Frame(self.gameFrame, bg=Colors.BACKGROUND)
        self.frameRight.place(x=env.GAME_SCREEN_W * percentageLeft, y=0, width=env.GAME_SCREEN_W * (1 - percentageLeft), height=env.GAME_SCREEN_H)

        self.treeView = ttk.Treeview(self.frameLeft, selectmode=tk.BROWSE)
        self.configTreeView()
        self.treeView.pack(expand=1, fill=tk.BOTH, padx=DEFAULT_PADDING_X, pady=DEFAULT_PADDING_Y)

        self.btnDeleteLick = CustomButton(self.frameRight, text="DELETE")
        self.btnDeleteLick.pack(anchor=tk.NE, padx=(0, DEFAULT_PADDING_X), pady=(DEFAULT_PADDING_Y, 0))

        self.lblLickKey = tk.Label(self.frameRight, text="LICK_KEY", font=(DEFAULT_FONT_NAME, 40), fg=Colors.TEXT_WHITE, bg=Colors.BACKGROUND)
        self.lblLickKey.pack(expand=1, fill=tk.BOTH, padx=(0, DEFAULT_PADDING_X))

        self.progressBar = ttk.Progressbar(self.frameRight, style=CustomStylesNames.STYLE_PROGRESSBAR_RED.value, value=0)
        self.progressBar.pack(fill=tk.X, padx=DEFAULT_PADDING_X, pady=8)

        self.rowCycles = tk.Frame(self.frameRight)
        self.btnChangeKeyManual = CustomButton(self.rowCycles, text="MANUAL")
        self.btnChangeKeyManual.pack(side=tk.LEFT, expand=1, fill=tk.X)
        self.btnChangeKeyAfter1Cycle = CustomButton(self.rowCycles, text="x1")
        self.btnChangeKeyAfter1Cycle.pack(side=tk.LEFT, expand=1, fill=tk.X)
        self.btnChangeKeyAfter2Cycles = CustomButton(self.rowCycles, text="x2")
        self.btnChangeKeyAfter2Cycles.pack(side=tk.LEFT, expand=1, fill=tk.X)
        self.btnChangeKeyAfter4Cycles = CustomButton(self.rowCycles, text="x4")
        self.btnChangeKeyAfter4Cycles.pack(side=tk.LEFT, expand=1, fill=tk.X)
        self.rowCycles.pack(expand=0, fill=tk.X, padx=(0, DEFAULT_PADDING_X))

        self.rowRandom = tk.Frame(self.frameRight)
        self.btnRandomLick = CustomButton(self.rowRandom, text="RANDOM")
        self.btnRandomLick.pack(side=tk.LEFT, expand=1, fill=tk.X)
        self.btnNextKey = CustomButton(self.rowRandom, text="NEXT_KEY")
        self.btnNextKey.pack(side=tk.LEFT, expand=1, fill=tk.X)
        self.btnPlay = CustomButton(self.rowRandom, text="PLAY")
        self.btnPlay.pack(side=tk.LEFT, expand=1, fill=tk.X)
        self.rowRandom.pack(side=tk.BOTTOM, fill=tk.X, padx=(0, DEFAULT_PADDING_X), pady=(0, DEFAULT_PADDING_Y))

        # =========== CREATION OF THE VIEW_MODEL ====================
        self.viewModel = PractiseLicksViewModel(self)
        # ===========================================================

    def configTreeView(self):
        style = ttk.Style()
        style.configure("Treeview.Heading", font=(DEFAULT_FONT_NAME, 8))
        style.configure("Treeview", font=(DEFAULT_FONT_NAME, 10))
        self.treeView['columns'] = ('FILENAME', 'KEY', 'NAME', 'DATE')
        self.treeView.column('#0', width=0, stretch=tk.NO)
        self.treeView.column('FILENAME', anchor=tk.W, width=0, stretch=0)
        self.treeView.column('KEY', anchor=tk.W, width=35, stretch=0)
        self.treeView.column('NAME', anchor=tk.W, width=100, stretch=0)
        self.treeView.column('DATE', anchor=tk.W, width=110, stretch=0)

        self.treeView.heading('#0', text='', anchor=tk.CENTER)
        self.treeView.heading('FILENAME', text='', anchor=tk.CENTER)
        self.treeView.heading('KEY', text='KEY', anchor=tk.CENTER)
        self.treeView.heading('NAME', text='NAME', anchor=tk.CENTER)
        self.treeView.heading('DATE', text='DATE', anchor=tk.CENTER)
        self.treeView.bind('<<TreeviewSelect>>', self.identifySelectedItemInTreeView)

    def setUiUpdateLblForLickSelected(self, lick_key: str, lick_name: str, lick_date: str):
        self.lblLickKey.config(text=lick_key)

    def identifySelectedItemInTreeView(self, event):
        selected_item = self.treeView.selection()[0]
        values = self.treeView.item(selected_item)['values']
        self.viewModel.onLickSelectedInTreeView(values)

    def setUiInitializeTreeView(self, licks_data: list):
        counter = 0
        for lick in licks_data:
            lick_id = lick[JsonLickFields.FIELD_LICK_ID.value]
            lick_name = lick[JsonLickFields.FIELD_LICK_NAME.value]
            lick_key = noteNameFull(lick[JsonLickFields.FIELD_LICK_KEY.value])[:-1]  # substring for removing the octave number (not needed)
            lick_date = lick[JsonLickFields.FIELD_LICK_DATE.value]
            # licks_readable_name = "{} - {} - {}".format(lick_name, lick_key, lick_date)
            tag = 'odd'
            if counter % 2 == 0:
                tag = 'even'
            self.treeView.insert(parent='', index=tk.END, values=(lick_id, lick_key, lick_name, lick_date), tags=tag)
        self.treeView.insert(parent='', index=tk.END, values=('filename11', 'aa', 'bb', 'dd'))
        self.treeView.insert(parent='', index=tk.END, values=('filename11', 'aa', 'bb', 'dd'))
        self.treeView.insert(parent='', index=tk.END, values=('filename11', 'aa', 'bb', 'dd'))
        self.treeView.tag_configure('odd', background='#E8E8E8')
        self.treeView.tag_configure('even', background='#DFDFDF')
