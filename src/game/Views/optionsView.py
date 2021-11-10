import os

from src.game.GamesNames import GameNames
from src.game.ViewModels.optionsViewModel import OptionsViewModel
from src.game.utils.customElements.customElements import *
from src.game.utils.customElements.scales import *
from src.game.utils.questionNote import playWinMelody
from src.game import env


class ViewStrings(Enum):
    NO_MIDI_IN_INTERFACE_SELECTED = "No Midi-in interface selected !!"
    NO_MIDI_OUT_INTERFACE_SELECTED = "No Midi-out interface selected !!"
    CURRENT_MIDI_IN = "MIDI in: "
    CURRENT_MIDI_OUT = "MIDI out: "
    LABEL_HEADER_OPTIONS = "OPTIONS:"


class OptionsView:
    def __init__(self, master, game_frame: tk.Frame):
        print("launching game {}".format(GameNames.GAME_OPTIONS))
        self.viewModel = None
        self.master = master
        self.gameFrame = game_frame
        if os.name != 'nt':
            self.gameFrame.config(cursor='none')
        self.gameFrame.config(bg=Colors.BACKGROUND)

        DEFAULT_PADDING = 3

        self.container=tk.Frame(self.gameFrame, bg=Colors.BACKGROUND)
        self.container.pack(side="top", fill="both", expand=True, padx=20, pady=(10,20))

        self.title = CustomLabel(self.container, text=ViewStrings.LABEL_HEADER_OPTIONS.value)
        self.title.pack(fill=tk.X, pady=(0,20))

        self.row1 = tk.Frame(self.container)
        self.row1.pack(fill=tk.X)
        self.currentMidiIn = CustomLabel(self.row1)
        self.currentMidiIn.pack(side=tk.LEFT, expand=1, fill=tk.X)

        self.currentMidiOut = CustomLabel(self.row1)
        self.currentMidiOut.pack(side=tk.LEFT, expand=1, fill=tk.X)

        self.row2 = tk.Frame(self.container,bg='red')
        self.row2.pack(fill=tk.X, expand=1)
        self.row2.grid_columnconfigure(0,weight=1, uniform='column_size')
        self.row2.grid_columnconfigure(1,weight=1, uniform='column_size')

        self.midiInListbox = tk.Listbox(self.row2, selectmode='single', exportselection=0)
        self.midiInListbox.grid(row=0, column=0,sticky=tk.NSEW)
        self.midiOutListbox = tk.Listbox(self.row2, selectmode='single', exportselection=0)
        self.midiOutListbox.grid(row=0,column=1, sticky=tk.NSEW)

        self.row3 = tk.Frame(self.container,bg='red')
        self.row3.pack(fill=tk.X, expand=1)
        self.row3.grid_columnconfigure(0,weight=1, uniform='column_size')
        self.row3.grid_columnconfigure(1,weight=1, uniform='column_size')

        self.lblNoteInIndication = tk.Label(self.row3, text="Input ?", bg=Colors.BACKGROUND, fg=Colors.TEXT_WHITE)
        self.lblNoteInIndication.grid(row=0, column=0,sticky=tk.NSEW)
        self.btnPlayNote = CustomButton(self.row3, text="Test note", background=Colors.BACKGROUND, foreground=Colors.TEXT_WHITE)
        self.btnPlayNote.grid(row=0,column=1,sticky=tk.NSEW)

        self.btnConfig = CustomButton(self.container, text="Return Default")
        self.btnConfig.pack(side=tk.RIGHT)
        # self.btnConfig.grid(row=current_row, column=1, sticky=tk.SE, padx=20)

        # =========== CREATION OF THE VIEW_MODEL ====================
        self.viewModel = OptionsViewModel(self)
        # ===========================================================
        self.midiInListbox.bind("<<ListboxSelect>>", self.viewModel.midiInChangeCallback)
        self.midiOutListbox.bind("<<ListboxSelect>>", self.viewModel.midiOutChangeCallback)
        self.btnPlayNote.config(command=self.viewModel.playTestNotes)

    def updateUiMidiInAndOut(self, new_midi_in, new_midi_out):
        # ternary operator
        self.currentMidiIn.config(text=(new_midi_in, ViewStrings.NO_MIDI_IN_INTERFACE_SELECTED.value)[new_midi_in == ""])
        self.currentMidiOut.config(text=(new_midi_out, ViewStrings.NO_MIDI_OUT_INTERFACE_SELECTED.value)[new_midi_out == ""])

    def updateUiMidiIn(self, new_midi_in):
        self.currentMidiIn.config(text=ViewStrings.CURRENT_MIDI_IN.value + new_midi_in)

    def updateUiMidiOut(self, new_midi_out):
        self.currentMidiOut.config(text=ViewStrings.CURRENT_MIDI_OUT.value + new_midi_out)

    def updateUiMIDIMessageReceived(self, message):
        self.lblNoteInIndication.config(text=message)

    def didYouHearMelody(self):
        print('did you heared')

    def destroy(self):
        pass

    def __del__(self):
        pass
