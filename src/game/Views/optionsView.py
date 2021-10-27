from src.game.Views.navbarView import GameNames

from src.game.autoload import Autoload
from src.game.utils.customElements.buttons import *
from src.game.utils.customElements.labels import *
from src.game.utils.customElements.scales import *
from src.game.ViewModels.optionsViewModel import OptionsViewModel, ViewStrings




class OptionsView:
    def __init__(self, master, game_frame: tk.Frame, config: dict):
        print("launching game {}".format(GameNames.GAME_OPTIONS))
        self.game = None
        self.config = config
        self.master = master
        self.gameFrame = game_frame
        self.gameFrame.config(bg="black")

        DEFAULT_PADDING = 3

        self.gameFrame.grid_rowconfigure(0, weight=1, pad=DEFAULT_PADDING)
        self.gameFrame.grid_rowconfigure(1, weight=1, pad=DEFAULT_PADDING)
        self.gameFrame.grid_rowconfigure(2, weight=1, pad=DEFAULT_PADDING)
        self.gameFrame.grid_rowconfigure(3, weight=1, pad=DEFAULT_PADDING)
        self.gameFrame.grid_rowconfigure(4, weight=1, pad=DEFAULT_PADDING)

        self.gameFrame.grid_columnconfigure(0, weight=1, pad=DEFAULT_PADDING)
        self.gameFrame.grid_columnconfigure(1, weight=1, pad=DEFAULT_PADDING)

        current_row: int = 0

        self.section1 = MyLabel12(self.gameFrame, text=ViewStrings.LABEL_HEADER_OPTIONS.value)
        self.section1.grid(row=current_row, column=0, sticky=tk.NW)

        current_row += 1

        self.currentMidiIn = MyLabel12(self.gameFrame)
        self.currentMidiIn.grid(row=current_row, column=0, sticky=tk.W, padx=20)

        self.currentMidiOut = MyLabel12(self.gameFrame)
        self.currentMidiOut.grid(row=current_row, column=1, sticky=tk.W, padx=20)

        current_row += 1

        self.midiInListbox= tk.Listbox(self.gameFrame, selectmode='single', exportselection=0)
        self.midiInListbox.grid(row=current_row, column=0, sticky=tk.NSEW, padx=20)

        self.midiOutListbox = tk.Listbox(self.gameFrame, selectmode='single', exportselection=0)
        self.midiOutListbox.grid(row=current_row, column=1, sticky=tk.NSEW, padx=20)

        current_row += 1

        self.btnConfig = BtnDefault(self.gameFrame, text="Return Default")
        self.btnConfig.grid(row=current_row, column=1, sticky=tk.SE, padx=20)

        self.game = OptionsViewModel(self, self.config)
        self.midiInListbox.bind("<<ListboxSelect>>", self.game.midiInChangeCallback)
        self.midiOutListbox.bind("<<ListboxSelect>>", self.game.midiOutChangeCallback)

    def updateConfig(self, value):
        difficulty = self.slider1_2.get()
        times_each_transpose = self.slider2_1.get()
        nb_of_transpose_before_change = self.slider2_2.get()

        # self.parent.config(["default_mode"])=default_mode
        old_config = self.config
        old_config["default_mode"] = 1
        old_config["question_delay"] = question_delay
        old_config["difficulty"] = difficulty
        old_config["times_each_transpose"] = times_each_transpose
        old_config["nb_of_transpose_before_change"] = nb_of_transpose_before_change

        self.config = old_config
        # self.parent.config(["question_delay"])=question_delay

    def update(self):
        print("updating UI")

    def destroy(self):
        pass
        # if self.game is not None:
        #     self.game.destroy()

    def __del__(self):
        print("trying destroy")
