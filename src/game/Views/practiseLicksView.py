import logging
import os
import tkinter as tk
from functools import partial
from tkinter import ttk, messagebox

from PIL import Image, ImageTk

from src.game import env
from src.game.GamesNames import GameNames
from src.game.ViewModels.practiseLicksViewModel import PractiseLicksViewModel, JsonLickFields
from src.game.utils.colors import Colors
from src.game.utils.customElements.customElements import CustomStylesNames, CustomButton, DEFAULT_FONT_NAME
from src.game.utils.midiToNotenames import noteNameFull
from src.game.ViewModels.practiseLicksViewModel import TranspositionMode
from src.game.Views.keyboardCanvasView import KeyboardCanvasView
from src.game.utils.customElements.customElements import CustomRadioButton

DEFAULT_PADDING_X = 20
DEFAULT_PADDING_Y = 20


class ViewImages:
    def __init__(self):
        self.IMAGE_PLAY_IMAGE = ImageTk.PhotoImage(Image.open(env.PLAY_IMAGE))
        self.IMAGE_PAUSE_IMAGE = ImageTk.PhotoImage(Image.open(env.PAUSE_IMAGE))
        self.IMAGE_SHUFFLE_IMAGE = ImageTk.PhotoImage(Image.open(env.SHUFFLE_IMAGE))
        self.IMAGE_METRONOME_IMAGE = ImageTk.PhotoImage(Image.open(env.METRONOME_IMAGE))
        self.IMAGE_ARROW_UP = ImageTk.PhotoImage(Image.open(env.ARROW_UP_IMAGE))
        self.IMAGE_ARROW_DOWN = ImageTk.PhotoImage(Image.open(env.ARROW_DOWN_IMAGE))
        self.IMAGE_DELETE_IMAGE = ImageTk.PhotoImage(Image.open(env.DELETE_IMAGE))
        self.IMAGE_RANDOM_KEY = ImageTk.PhotoImage(Image.open(env.RANDOM_KEY_IMAGE))
        self.IMAGE_NEXT_KEY = ImageTk.PhotoImage(Image.open(env.NEXT_KEY_IMAGE))


class PractiseLicksView:
    def __init__(self, master, game_frame: tk.Frame):
        print("launching game {}".format(GameNames.GAME_LICKS_PRACTISE))
        self.master = master
        self.viewModel = None
        self.gameFrame = game_frame
        if os.name != 'nt':
            self.gameFrame.config(cursor='none')

        self.images = ViewImages()

        self.gameFrame.rowconfigure(0, weight=0)
        self.gameFrame.rowconfigure(1, weight=1)
        self.gameFrame.rowconfigure(2)
        self.gameFrame.grid_columnconfigure(0)
        self.gameFrame.grid_columnconfigure(1)
        self.gameFrame.grid_columnconfigure(2, weight=3)

        LBL_LICK_FONT_SIZE = 65
        # ================== FRAME CONTAINING KEY INDICATIONS =============================
        self.frameKeyIndicationContainer = tk.Frame(self.gameFrame, bg=Colors.BACKGROUND)
        self.frameKeyIndicationContainer.grid(row=0, column=0, columnspan=3, sticky=tk.NSEW)
        self.rowKeyContainer = tk.Frame(self.frameKeyIndicationContainer, )
        self.rowKeyContainer.pack(pady=(0, 0))
        self.lblLickKey = tk.Label(self.rowKeyContainer, text="", font=(DEFAULT_FONT_NAME, LBL_LICK_FONT_SIZE), fg=Colors.TEXT_WHITE, bg=Colors.BACKGROUND)
        self.lblLickKey.pack(side=tk.LEFT, expand=1, fill=tk.BOTH)
        self.lblLickNextKey = tk.Label(self.rowKeyContainer, text="RAND_KEY", font=(DEFAULT_FONT_NAME, LBL_LICK_FONT_SIZE), fg=Colors.PRIMARY, bg=Colors.BACKGROUND)
        self.lblCurrentLickInfo = tk.Label(self.frameKeyIndicationContainer, text="INFO", font=(DEFAULT_FONT_NAME, 12), fg=Colors.TEXT_WHITE, bg=Colors.BACKGROUND)
        self.lblCurrentLickInfo.pack(side=tk.BOTTOM)

        # ================== FRAME CONTAINING PROGRESSBAR AND KEYBOARD CANVAS ==============
        self.keyboardCanvasContainer = tk.Frame(self.gameFrame, bg=Colors.BACKGROUND)
        self.keyboardCanvasContainer.grid(row=1, column=0, columnspan=3, sticky=tk.NSEW, padx=10, pady=10)
        self.progressBar = ttk.Progressbar(self.keyboardCanvasContainer, style=CustomStylesNames.STYLE_CUSTOM_PROGRESSBAR.value, value=0)
        self.progressBar.config(value=0)
        self.progressBar.pack(side=tk.TOP, fill=tk.X)
        self.keyboardCanvas = KeyboardCanvasView(self.keyboardCanvasContainer)
        # self.keyboardCanvasContainer.pack()

        # =================== FRAME CONTAINING TREEVIEW =================================
        self.licksTreeViewContainer = tk.Frame(self.gameFrame)
        self.licksTreeViewContainer.grid(row=2, column=0, columnspan=1, sticky=tk.NSEW, padx=(10, 0), pady=(10, 10))
        self.treeView = ttk.Treeview(self.licksTreeViewContainer, selectmode=tk.BROWSE, show='tree', height=6)
        self.treeView.pack(side=tk.TOP, expand=0, fill=tk.BOTH)
        self.configTreeView()

        # =================== FRAME CONTAINING TREE CONTROLS =============================
        self.lickTreeViewControlsContainer = tk.Frame(self.gameFrame, bg=Colors.BACKGROUND)
        self.lickTreeViewControlsContainer.grid(row=2, column=1, columnspan=1, sticky=tk.NSEW, padx=0, pady=(10, 10))
        self.btnTreeViewItemPlus = tk.Button(self.lickTreeViewControlsContainer, image=self.images.IMAGE_ARROW_UP,
                                             background=Colors.PRIMARY, command=lambda: self.selectTreeViewNextItem())
        self.btnTreeViewItemPlus.pack()
        self.btnTreeViewItemMinus = tk.Button(self.lickTreeViewControlsContainer, image=self.images.IMAGE_ARROW_DOWN,
                                              background=Colors.PRIMARY, command=lambda: self.selectTreeViewPreviousItem())
        self.btnTreeViewItemMinus.pack()
        self.btnDeleteLick = tk.Button(self.lickTreeViewControlsContainer, image=self.images.IMAGE_DELETE_IMAGE,
                                       background=Colors.PRIMARY, command=self.onBtnDeleteLickClick)
        self.btnDeleteLick.pack(side=tk.BOTTOM)

        self.radioButtonValue = tk.IntVar()

        # =================== FRAME CONTAINING BTN CONTROLS ========================#
        self.controlsContainer = tk.Frame(self.gameFrame)
        self.controlsContainer.grid(row=2, column=2, sticky=tk.NSEW, padx=10, pady=10)
        # ================= ROW 1 IN CONTROLS ==========================
        self.rowCycles = tk.Frame(self.controlsContainer)
        self.rowCycles.pack(expand=1, fill=tk.BOTH)
        self.btnChangeKeyManual = CustomRadioButton(self.rowCycles, text="x0", value=-1, variable=self.radioButtonValue)
        self.btnChangeKeyManual.pack(side=tk.LEFT, expand=1, fill=tk.BOTH)
        self.btnChangeKeyAfter1Cycle = CustomRadioButton(self.rowCycles, text="x1", value=1, variable=self.radioButtonValue)
        self.btnChangeKeyAfter1Cycle.pack(side=tk.LEFT, expand=1, fill=tk.BOTH)
        self.btnChangeKeyAfter2Cycles = CustomRadioButton(self.rowCycles, text="x2", value=2, variable=self.radioButtonValue)
        self.btnChangeKeyAfter2Cycles.pack(side=tk.LEFT, expand=1, fill=tk.BOTH)
        self.btnChangeKeyAfter4Cycles = CustomRadioButton(self.rowCycles, text="x4", value=4, variable=self.radioButtonValue)
        self.btnChangeKeyAfter4Cycles.pack(side=tk.LEFT, expand=1, fill=tk.BOTH)
        # ================= ROW 2 IN CONTROLS ==========================
        self.rowRandom = tk.Frame(self.controlsContainer)
        self.rowRandom.pack(expand=1, fill=tk.BOTH)
        self.btnTransposeNow = CustomButton(self.rowRandom, image=self.images.IMAGE_RANDOM_KEY)
        self.btnTransposeNow.pack(side=tk.LEFT, expand=1, fill=tk.BOTH)
        self.btnTransposeMode = CustomButton(self.rowRandom, image=self.images.IMAGE_NEXT_KEY)
        self.btnTransposeMode.pack(side=tk.LEFT, expand=1, fill=tk.BOTH)
        self.btnPlay = CustomButton(self.rowRandom, image=self.images.IMAGE_PLAY_IMAGE, command=lambda: self.viewModel.onBtnPlayClick())
        self.btnPlay.pack(side=tk.LEFT, expand=1, fill=tk.BOTH)

        # =========== CREATION OF THE VIEW_MODEL ====================
        self.viewModel = PractiseLicksViewModel(self)
        # ===========================================================

        self.btnChangeKeyManual.config(command=partial(self.viewModel.onBtnChangeNumberOfCyclesBeforeTransposeClick, -1))
        self.btnChangeKeyAfter1Cycle.config(command=partial(self.viewModel.onBtnChangeNumberOfCyclesBeforeTransposeClick, 1))
        self.btnChangeKeyAfter2Cycles.config(command=partial(self.viewModel.onBtnChangeNumberOfCyclesBeforeTransposeClick, 2))
        self.btnChangeKeyAfter4Cycles.config(command=partial(self.viewModel.onBtnChangeNumberOfCyclesBeforeTransposeClick, 4))
        self.btnTransposeMode.config(command=partial(self.viewModel.setTransposeMode, TranspositionMode.TRANSPOSE_SEQUENTIAL.value))

        # self.btnTransposeNow.config(command=partial(self.viewModel.setTransposeMode, TranspositionMode.TRANSPOSE_RANDOM.value))
        self.btnTransposeNow.config(command=self.viewModel.destroyViewModel)

    def selectTreeViewPreviousItem(self):
        self.moveTreeViewSelectionItem(+1)

    def selectTreeViewNextItem(self):
        self.moveTreeViewSelectionItem(-1)

    def moveTreeViewSelectionItem(self, offset: int):
        all_items = self.treeView.get_children()
        current_item = self.treeView.focus()
        found_index = -99
        counter = 0
        for item in all_items:
            if item == current_item:
                found_index = counter
            counter += 1
        new_index = found_index + offset
        if new_index < 0:
            new_index = len(all_items) - 1
        if new_index >= len(all_items):
            new_index = 0
        new_item = all_items[new_index]
        self.setTreeViewSelectItem(new_item)

    def getFirstTreeViewItem(self):
        treeView_children = self.treeView.get_children()
        if len(treeView_children) == 0:
            return None
        try:
            return treeView_children[0]
        except Exception as e:
            print("Empty treeView")
            logging.exception(e)
        return None

    def setTreeViewSelectItem(self, item):
        self.treeView.focus(item)
        self.treeView.selection_set(item)

    def configTreeView(self):
        style = ttk.Style()
        style.configure("Treeview.Heading", font=(DEFAULT_FONT_NAME, 8))
        style.configure("Treeview", font=(DEFAULT_FONT_NAME, 10))
        self.treeView['columns'] = ('FILENAME', 'KEY', 'NAME', 'DATE')
        self.treeView.column('#0', width=0, stretch=tk.NO)
        self.treeView.column('FILENAME', anchor=tk.W, width=0, stretch=0)
        self.treeView.column('KEY', anchor=tk.W, width=35, stretch=0)
        self.treeView.column('NAME', anchor=tk.W, width=220, stretch=0)
        self.treeView.column('DATE', anchor=tk.W, width=0, stretch=0)

        self.treeView.heading('#0', text='', anchor=tk.CENTER)
        self.treeView.heading('FILENAME', text='', anchor=tk.CENTER)
        self.treeView.heading('KEY', text='KEY', anchor=tk.CENTER)
        self.treeView.heading('NAME', text='NAME', anchor=tk.CENTER)
        self.treeView.heading('DATE', text='DATE', anchor=tk.CENTER)
        self.treeView.bind('<<TreeviewSelect>>', self.identifySelectedItemInTreeView)

    def setUiNumberOfLoopsBeforeTranspose(self, number_of_loops: int):
        self.radioButtonValue.set(number_of_loops)

        # if number_of_loops == 4:
        #     self.btnChangeKeyAfter4Cycles.config(background=Colors.PRIMARY, state='normal')
        # pass

    def setUiUpdateProgress(self, value: int):
        self.progressBar.config(value=value)

    def setUiUpdateLblForLickSelected(self, lick_key: str, lick_name: str = None, lick_date: str = None):
        self.lblLickKey.config(text=lick_key)

    def setUiUpdateLblForCyclesInfo(self, current_cycle: int, number_of_cycles_per_transpose):
        if number_of_cycles_per_transpose == -1:
            self.lblCurrentLickInfo.config(text="No transposition")
            self.setUiResetLblNextKeyIndication()
            return
        if current_cycle > number_of_cycles_per_transpose:
            self.lblCurrentLickInfo.config(text="Starting at next loop...")
            self.setUiResetLblNextKeyIndication()
        else:
            self.lblCurrentLickInfo.config(text="Loop {}/{} before transposition.".format(current_cycle, number_of_cycles_per_transpose))
        # easiest way to transpose at the right moment is to call the transpose function from here
        # if current_cycle == number_of_cycles_per_transpose, we  can transpose, else we should not transpose
        self.viewModel.updateShouldTransposeNext(current_cycle == number_of_cycles_per_transpose)

    def setUiUpdateLblNextKeyIndication(self, next_key: str):
        self.lblLickNextKey.config(text="Next {}...".format(next_key))
        self.lblLickNextKey.pack()
        self.lblLickKey.pack_forget()
        # self.lblLickKey.pack()

    def setUiResetLblNextKeyIndication(self):
        self.lblLickNextKey.pack_forget()
        self.lblLickKey.pack()

    def identifySelectedItemInTreeView(self, event):
        selected_item = self.treeView.selection()[0]
        values = self.treeView.item(selected_item)['values']
        self.viewModel.onLickSelectedInTreeView(values)

    def onBtnDeleteLickClick(self):
        delete_lick_confirm = messagebox.askyesno(title="Delete Lick", message="Delete Lick ?", icon='warning')
        if delete_lick_confirm:
            item_selected = self.treeView.selection()[0]
            item_data = self.getItemTreeViewDataByItem(item_selected)
            self.viewModel.onBtnDeleteLickClick(item_data)

    def getItemTreeViewDataByItem(self, user_item):
        for item in self.treeView.get_children():
            if item == user_item:
                item_data = self.treeView.item(item)
                return item_data
        return None

    def setUiInitializeTreeView(self, licks_data: list):
        if licks_data is None:
            print('No Data')
            self.lblLickKey.config(text="NOTHING")
            return
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
        self.treeView.tag_configure('odd', background=Colors.TREEVIEW_BACKGROUND_ODD)
        self.treeView.tag_configure('even', background=Colors.TREEVIEW_BACKGROUND_EVEN)

    def clearTreeView(self):
        self.treeView.delete(*self.treeView.get_children())

    def destroy(self):
        print("Deleting PractiseLicksView")
        self.viewModel.destroyViewModel()
        self.keyboardCanvas.destroy()
