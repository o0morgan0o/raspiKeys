import tkinter as tk
from enum import Enum
from tkinter import ttk

from ttkbootstrap import Style

from src.game.utils.colors import Colors

my_font = "Courier"
DEFAULT_FONT_NAME = "Helvetica"
DEFAULT_FONT_SIZE = 14
DEFAULT_FONT = (DEFAULT_FONT_NAME, DEFAULT_FONT_SIZE)
DEFAULT_PADDING_X = 20
DEFAULT_PADDING_Y = 5


class CustomStylesNames(Enum):
    STYLE_BTN_WARNING_OUTLINE = "custom.warning.Outline.TButton"
    STYLE_BTN_DARK = "custom.TButton"
    STYLE_BTN_FOOTER_PLUS_MINUS = "custom_footer_plus_minus.TButton"
    STYLE_BTN_CONTROLS_PLUS_MINUS = "custom_controls.TButton"
    STYLE_LBL_FULL = "custom.Inverse.TLabel"
    STYLE_PROGRESSBAR_RED = "custom.Horizontal.TProgressbar"


def getCustomStyles():
    style = Style()
    style.configure(CustomStylesNames.STYLE_BTN_WARNING_OUTLINE.value,
                    font=(DEFAULT_FONT_NAME, DEFAULT_FONT_SIZE)
                    )
    style.configure(CustomStylesNames.STYLE_BTN_DARK.value,
                    background=Colors.BACKGROUND
                    )
    style.configure(CustomStylesNames.STYLE_LBL_FULL.value,
                    background=Colors.BACKGROUND
                    )
    style.configure(CustomStylesNames.STYLE_BTN_FOOTER_PLUS_MINUS.value,
                    background=Colors.BACKGROUND,
                    font=(DEFAULT_FONT_NAME, 30)
                    )
    style.configure(CustomStylesNames.STYLE_BTN_CONTROLS_PLUS_MINUS.value,
                    background=Colors.BACKGROUND,
                    font=(DEFAULT_FONT_NAME, 40)
                    )
    style.configure(CustomStylesNames.STYLE_PROGRESSBAR_RED.value,
                    background=Colors.PRIMARY,
                    bordercolor=Colors.BACKGROUND,
                    # foreground=Colors.BACKGROUND,
                    troughcolor=Colors.BACKGROUND
                    )


class CustomButton(tk.Button):
    def __init__(self, parent, text="",
                 image=None,
                 font=DEFAULT_FONT,
                 background=Colors.BTN_STANDARD_BACKGROUND,
                 foreground=Colors.TEXT_WHITE,
                 command=None,
                 borderwidth=1,
                 highlightbackground=Colors.WHITE,
                 highlightthickness=Colors.BTN_BORDER_THICKNESS,
                 highlightcolor=Colors.BTN_BORDER_COLOR,
                 relief=tk.RIDGE
                 ):
        super().__init__(parent, text=text,
                         image=image,
                         font=font,
                         background=background,
                         foreground=foreground,
                         command=command,
                         borderwidth=borderwidth,
                         highlightbackground=highlightbackground,
                         highlightthickness=highlightthickness,
                         highlightcolor=highlightcolor,
                         relief=relief
                         )


class CustomFooterButton(tk.Button):
    def __init__(self, parent, text="",
                 font=DEFAULT_FONT,
                 background=Colors.BTN_FOOTER_BACKGROUND,
                 foreground=Colors.TEXT_WHITE,
                 command=None,
                 style=None,
                 ):
        super().__init__(parent, text=text,
                         font=font,
                         background=background,
                         foreground=foreground,
                         command=command,
                         )


class CustomLabel(tk.Label):
    def __init__(self, parent: tk.Frame,
                 text=None,
                 font=DEFAULT_FONT,
                 justify=None,
                 background=Colors.BACKGROUND,
                 foreground=Colors.TEXT_WHITE,
                 padx=None,
                 pady=None,
                 width=None,
                 height=None,
                 ):
        super().__init__(parent,
                         text=text,
                         font=font,
                         justify=justify,
                         background=background,
                         foreground=foreground,
                         padx=padx,
                         pady=pady,
                         width=width,
                         height=height
                         )


class CustomScale(tk.Scale):
    def __init__(self, parent: tk.Frame,
                 background=Colors.ERROR,
                 foreground=Colors.TEXT_WHITE,
                 relief=tk.FLAT,
                 from_=0,
                 to=100,
                 orient=tk.HORIZONTAL,
                 width=None,
                 label=None,
                 showvalue=0,
                 troughcolor=Colors.SLIDER_BACKGROUND,
                 resolution=None,
                 ):
        super().__init__(parent,
                         highlightcolor="green",
                         highlightthickness=0,
                         foreground=foreground,
                         background=background,
                         relief=relief,
                         from_=from_,
                         to=to,
                         orient=orient,
                         width=width,
                         label=label,
                         showvalue=showvalue,
                         troughcolor=troughcolor,
                         borderwidth=0,
                         resolution=resolution
                         )
