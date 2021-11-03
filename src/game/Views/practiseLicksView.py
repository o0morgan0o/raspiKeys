import tkinter as tk
from tkinter import ttk

from src.game.GamesNames import GameNames
from src.game.ViewModels.practiseLicksViewModel import PractiseLicksViewModel, JsonLickFields
from src.game.utils.customElements.customElements import CustomStylesNames, CustomButton, CustomScale
from src.game.utils.midiToNotenames import noteNameFull


class PractiseLicksView:
    def __init__(self, master, game_frame: tk.Frame):
        print("launching game {}".format(GameNames.GAME_LICKS_PRACTISE))
        self.master = master
        self.viewModel = None
        self.gameFrame = game_frame

        self.gameFrame.grid_rowconfigure(0, weight=1)
        self.gameFrame.grid_columnconfigure(0, weight=1)
        self.gameFrame.grid_columnconfigure(1, weight=1)

        self.frameLeft = tk.Frame(self.gameFrame)
        self.frameLeft.grid(row=0, column=0, sticky=tk.NSEW)

        self.frameRight = tk.Frame(self.gameFrame)
        self.frameRight.grid(row=0, column=1)

        self.treeView = ttk.Treeview(self.frameLeft, selectmode=tk.BROWSE)
        self.configTreeView()
        self.treeView.pack(expand=1, fill=tk.BOTH)

        self.btnDeleteLick = CustomButton(self.frameRight, text="DELETE")
        self.btnDeleteLick.pack(anchor=tk.NE)

        self.lblLickKey = tk.Label(self.frameRight, text="LICK_KEY")
        self.lblLickKey.pack()

        self.progressBar = ttk.Progressbar(self.frameRight, style=CustomStylesNames.STYLE_PROGRESSBAR_RED.value, value=0)
        self.progressBar.pack(fill=tk.BOTH)

        self.rowCycles = tk.Frame(self.frameRight)
        self.btnChangeKeyManual = CustomButton(self.rowCycles, text="MANUAL")
        self.btnChangeKeyManual.pack(side=tk.LEFT, expand=1)
        self.btnChangeKeyAfter1Cycle = CustomButton(self.rowCycles, text="1cycle")
        self.btnChangeKeyAfter1Cycle.pack(side=tk.LEFT, expand=1)
        self.btnChangeKeyAfter2Cycles = CustomButton(self.rowCycles, text="2cycles")
        self.btnChangeKeyAfter2Cycles.pack(side=tk.LEFT, expand=1)
        self.btnChangeKeyAfter4Cycles = CustomButton(self.rowCycles, text="4cycles")
        self.btnChangeKeyAfter4Cycles.pack(side=tk.LEFT, expand=1)
        self.rowCycles.pack()

        self.rowRandom = tk.Frame(self.frameRight)
        self.btnRandomLick = CustomButton(self.rowRandom, text="RANDOM")
        self.btnRandomLick.pack(side=tk.LEFT)

        self.btnNextKey = CustomButton(self.rowRandom, text="NEXT_KEY")
        self.btnNextKey.pack(side=tk.LEFT)
        self.rowRandom.pack()
        # #

        # =========== CREATION OF THE VIEW_MODEL ====================
        self.viewModel = PractiseLicksViewModel(self)
        # ===========================================================

        # self.gameFrame.pack_propagate(0)
        # self.gameFrame.config(bg="black")

        # self.gameFrame.btnRecord = BtnBlack10(self.gameFrame, text="record")
        # self.gameFrame.btnDeleteSelected = tk.Button(self.gameFrame, text="Delete lick")
        # self.gameFrame.btnDeleteSelected.config(bg="red")
        # self.gameFrame.btnPractiseLick = tk.Button(self.gameFrame, text="Practise Lick")
        # self.gameFrame.btnRandomLick = tk.Button(self.gameFrame, text="Practise All")
        # self.gameFrame.lblMessage = tk.Label(self.gameFrame, text="there are no licks in the base")
        # self.gameFrame.lblStatic1 = tk.Label(self.gameFrame, text="licks found: ")
        #
        # self.gameFrame.lblKey = tk.Label(self.gameFrame, text="")
        # self.gameFrame.lblKey.config(font=("Courier", 30, "bold"))
        # self.gameFrame.lblNotes = tk.Label(self.gameFrame, text="notes....", wraplength=180)
        # self.gameFrame.lblFollowing = tk.Label(self.gameFrame, text="")
        #
        # self.gameFrame.btnNext = tk.Button(self.gameFrame, text=">")
        # self.gameFrame.btnNext.config(font=("Courier", 12, "bold"))
        # self.gameFrame.btnPrev = tk.Button(self.gameFrame, text="<")
        # self.gameFrame.btnPrev.config(font=("Courier", 12, "bold"))

        # placement
        # self.placeElements()
        # self.game = PractiseLicksViewModel(self.globalRoot, self.gameFrame, config, app)

    def configTreeView(self):
        self.treeView['columns'] = ('NAME', 'KEY', 'DATE')
        self.treeView.column('#0', width=0, stretch=tk.NO)
        self.treeView.column('NAME', anchor=tk.CENTER, width=40)
        self.treeView.column('KEY', anchor=tk.CENTER, width=40)
        self.treeView.column('DATE', anchor=tk.CENTER, width=40)

        self.treeView.heading('#0', text='', anchor=tk.CENTER)
        self.treeView.heading('NAME', text='NAME', anchor=tk.CENTER)
        self.treeView.heading('KEY', text='KEY', anchor=tk.CENTER)
        self.treeView.heading('DATE', text='DATE', anchor=tk.CENTER)

    def setUiInitializeTreeView(self, licks_data: list):
        for lick in licks_data:
            lick_name = lick[JsonLickFields.FIELD_LICK_NAME.value]
            lick_key = noteNameFull(lick[JsonLickFields.FIELD_LICK_KEY.value])[:-1] # substring for removing the octave number (not needed)
            lick_date = lick[JsonLickFields.FIELD_LICK_DATE.value]
            licks_readable_name = "{} - {} - {}".format(lick_name, lick_key, lick_date)
            self.treeView.insert(parent='', index=tk.END, values=(lick_name, lick_key, lick_date))
