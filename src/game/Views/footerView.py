from src.game.GamesNames import GameNames
from src.game.ViewModels.FooterViewModel import FooterViewModel
from src.game.utils.customElements.customElements import *
from src.customtkinter import CTkButton


class ViewStrings(Enum):
    STRING_LBL_AUDIO_VOLUME = "AUDIO VOLUME : "
    STRING_LBL_MIDI_VOLUME = "MIDI VOLUME : "
    STRING_BTN_OPTIONS = "Opts"


class CustomFooterButton(CTkButton):
    def __init__(self,
                 corner_radius=18,
                 *args,
                 **kwargs,
                 ):
        super().__init__(*args,
                         corner_radius=corner_radius,
                         text_color=Colors.TEXT_WHITE,
                         fg_color=Colors.DARK,
                         bg_color=Colors.BACKGROUND,
                         text_font=(DEFAULT_FONT_NAME, 24, "bold"),
                         **kwargs)


class FooterView:

    def __init__(self, master, game_frame: tk.Frame):
        self.master = master
        self.gameFrame = game_frame

        FRAME_PADDING_X = 10
        FRAME_PADDING_Y = 20

        BTN_PADDING_X = 1
        BTN_PADDING_Y = 10

        self.footerFrame1 = tk.Frame(self.gameFrame, bg=Colors.BACKGROUND)
        self.footerFrame1.pack(side=tk.LEFT, fill=tk.BOTH, expand=1,
                               padx=(FRAME_PADDING_X, FRAME_PADDING_X / 2))
        self.footerFrame2 = tk.Frame(self.gameFrame, bg=Colors.BACKGROUND)
        self.footerFrame2.pack(side=tk.RIGHT, fill=tk.BOTH, expand=1,
                               padx=(FRAME_PADDING_X / 2, FRAME_PADDING_X))

        self.lblAudioVolume = ttk.Label(self.footerFrame1, text=ViewStrings.STRING_LBL_AUDIO_VOLUME, style=CustomStylesNames.STYLE_LBL_FULL.value, padding=0)
        self.lblAudioVolume.pack(side=tk.TOP, fill=tk.BOTH)
        self.btnAudioMinus = CustomFooterButton(master=self.footerFrame1, text="-", command=lambda: self.viewModel.audioMinusClicked())
        self.btnAudioPlus = CustomFooterButton(master=self.footerFrame1, text="+", command=lambda: self.viewModel.audioPlusClicked())
        self.btnAudioMinus.pack(side=tk.LEFT, expand=1, fill=tk.BOTH,
                                padx=BTN_PADDING_X,
                                pady=BTN_PADDING_Y)
        self.btnAudioPlus.pack(side=tk.RIGHT, expand=1, fill=tk.BOTH,
                               padx=BTN_PADDING_X,
                               pady=BTN_PADDING_Y)

        self.lblMidiVolume = ttk.Label(self.footerFrame2, text=ViewStrings.STRING_LBL_MIDI_VOLUME, style=CustomStylesNames.STYLE_LBL_FULL.value, padding=0)
        self.lblMidiVolume.pack(side=tk.TOP, fill=tk.X)
        self.btnMidiMinus = CustomFooterButton(master=self.footerFrame2, text="-", command=lambda: self.viewModel.midiMinusClicked())
        self.btnMidiMinus.pack(side=tk.LEFT, expand=1, fill=tk.BOTH,
                               padx=BTN_PADDING_X,
                               pady=BTN_PADDING_Y)
        self.btnMidiPlus = CustomFooterButton(master=self.footerFrame2, text="+", command=lambda: self.viewModel.midiPlusClicked())
        self.btnMidiPlus.pack(side=tk.RIGHT, expand=1, fill=tk.BOTH,
                              padx=BTN_PADDING_X,
                              pady=BTN_PADDING_Y)

        # =========== CREATION OF THE VIEW_MODEL ====================
        self.viewModel = FooterViewModel(self)
        # ===========================================================

    def setUiInitialization(self, audio_volume: int, midi_volume: int):
        self.lblAudioVolume.config(text=ViewStrings.STRING_LBL_AUDIO_VOLUME.value + str(round(audio_volume, 2)))
        self.lblMidiVolume.config(text=ViewStrings.STRING_LBL_MIDI_VOLUME.value + str(midi_volume))

    def updateLblAudioVolume(self, audio_volume: float):
        self.lblAudioVolume.config(text=ViewStrings.STRING_LBL_AUDIO_VOLUME.value + str(round(audio_volume, 2)))

    def updateLblMidiVolume(self, midi_volume: int):
        self.lblMidiVolume.config(text=ViewStrings.STRING_LBL_MIDI_VOLUME.value + str(midi_volume))
