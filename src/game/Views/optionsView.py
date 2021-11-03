from src.game.GamesNames import GameNames
from src.game.ViewModels.optionsViewModel import OptionsViewModel
from src.game.utils.customElements.customElements import *
from src.game.utils.customElements.labels import *
from src.game.utils.customElements.scales import *


class ViewStrings(Enum):
    NO_MIDI_IN_INTERFACE_SELECTED = "No Midi-in interface selected !!"
    NO_MIDI_OUT_INTERFACE_SELECTED = "No Midi-out interface selected !!"
    CURRENT_MIDI_IN = "MIDI in: "
    CURRENT_MIDI_OUT = "MIDI out: "
    LABEL_HEADER_OPTIONS = "OPTIONS:"


class OptionsView:
    def __init__(self, master, game_frame: tk.Frame):
        print("launching game {}".format(GameNames.GAME_OPTIONS))
        self.game = None
        self.master = master
        self.gameFrame = game_frame
        self.gameFrame.config(bg="black")

        DEFAULT_PADDING = 3

        self.gameFrame.grid_rowconfigure(0, weight=1, pad=DEFAULT_PADDING)
        self.gameFrame.grid_rowconfigure(1, weight=1, pad=DEFAULT_PADDING)
        self.gameFrame.grid_rowconfigure(2, weight=1, pad=DEFAULT_PADDING)
        self.gameFrame.grid_rowconfigure(3, weight=1, pad=DEFAULT_PADDING)
        self.gameFrame.grid_rowconfigure(4, weight=1, pad=DEFAULT_PADDING)

        self.gameFrame.grid_columnconfigure(0, weight=1, uniform="column_size", pad=DEFAULT_PADDING)
        self.gameFrame.grid_columnconfigure(1, weight=1, uniform="column_size", pad=DEFAULT_PADDING)

        current_row: int = 0

        self.section1 = MyLabel12(self.gameFrame, text=ViewStrings.LABEL_HEADER_OPTIONS.value)
        self.section1.grid(row=current_row, column=0, sticky=tk.NW)

        current_row += 1

        self.currentMidiIn = MyLabel12(self.gameFrame)
        self.currentMidiIn.grid(row=current_row, column=0, sticky=tk.W, padx=20)

        self.currentMidiOut = MyLabel12(self.gameFrame)
        self.currentMidiOut.grid(row=current_row, column=1, sticky=tk.W, padx=20)

        current_row += 1

        self.midiInListbox = tk.Listbox(self.gameFrame, selectmode='single', exportselection=0)
        self.midiInListbox.grid(row=current_row, column=0, sticky=tk.NSEW, padx=20)

        self.midiOutListbox = tk.Listbox(self.gameFrame, selectmode='single', exportselection=0)
        self.midiOutListbox.grid(row=current_row, column=1, sticky=tk.NSEW, padx=20)

        current_row += 1

        self.btnConfig = tk.Button(self.gameFrame, text="Return Default")
        self.btnConfig.grid(row=current_row, column=1, sticky=tk.SE, padx=20)

        # =========== CREATION OF THE VIEW_MODEL ====================
        self.game = OptionsViewModel(self)
        # ===========================================================
        self.midiInListbox.bind("<<ListboxSelect>>", self.game.midiInChangeCallback)
        self.midiOutListbox.bind("<<ListboxSelect>>", self.game.midiOutChangeCallback)

    def updateUiMidiInAndOut(self, new_midi_in, new_midi_out):
        # ternary operator
        self.currentMidiIn.config(text=(new_midi_in, ViewStrings.NO_MIDI_IN_INTERFACE_SELECTED.value)[new_midi_in == ""])
        self.currentMidiOut.config(text=(new_midi_out, ViewStrings.NO_MIDI_OUT_INTERFACE_SELECTED.value)[new_midi_out == ""])

    def updateUiMidiIn(self, new_midi_in):
        self.currentMidiIn.config(text=ViewStrings.CURRENT_MIDI_IN.value + new_midi_in)

    def updateUiMidiOut(self, new_midi_out):
        self.currentMidiOut.config(text=ViewStrings.CURRENT_MIDI_OUT.value + new_midi_out)

    def destroy(self):
        pass

    def __del__(self):
        pass
