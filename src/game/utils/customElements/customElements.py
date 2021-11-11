import tkinter as tk
from enum import Enum

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
    STYLE_CUSTOM_PROGRESSBAR = "custom.Horizontal.TProgressbar"
    STYLE_CUSTOM_BOOTSTRAP_SCALE = "myCustom.Horizontal.TScale"


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
    style.configure(CustomStylesNames.STYLE_CUSTOM_PROGRESSBAR.value,
                    background=Colors.CUSTOM_PROGRESSBAR_COLOR,
                    bordercolor=Colors.BACKGROUND,
                    troughcolor=Colors.BACKGROUND,
                    thickness=5
                    )
    style.configure(style="myCustom.Horizontal.TScale",
                    background='red',
                    borderwidth=0,
                    darkcolor='#ff0000',
                    groovewidth=0,
                    lightcolor='#00ff00',
                    sliderwidth=100,
                    troughcolor='#ffff00',
                    relief='flat'
                    )


class CustomRadioButton(tk.Radiobutton):
    def __init__(self,
                 parent,
                 value,
                 font=DEFAULT_FONT,
                 background=Colors.BTN_STANDARD_BACKGROUND,
                 foreground=Colors.TEXT_WHITE,
                 activebackground=Colors.PRIMARY,
                 activeforeground=Colors.TEXT_WHITE,
                 # highlightbackground=Colors.PRIMARY,
                 # highlightcolor=Colors.PRIMARY,
                 variable=None,
                 text="",
                 indicatoron=0,
                 selectcolor=Colors.PRIMARY,
                 ):
        super().__init__(
            parent,
            font=font,
            background=background,
            activebackground=activebackground,
            activeforeground=activeforeground,
            # highlightbackground=highlightbackground,
            # highlightcolor=highlightcolor,
            foreground=foreground,
            value=value,
            variable=variable,
            text=text,
            indicatoron=indicatoron,
            selectcolor=selectcolor,
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
                 relief=tk.RIDGE,
                 height=None,
                 width=None,
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
                         relief=relief,
                         height=height,
                         width=width
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
                 background=Colors.CUSTOM_SLIDER_BACKGROUND_COLOR,
                 foreground=Colors.TEXT_WHITE,
                 relief=tk.FLAT,
                 from_=0,
                 to=100,
                 orient=tk.HORIZONTAL,
                 width=None,
                 label=None,
                 showvalue=0,
                 troughcolor=Colors.CUSTOM_SLIDER_TROUGHCOLOR,
                 activebackground=Colors.CUSTOM_SLIDER_ACTIVE_COLOR,
                 borderwidth=0,
                 resolution=None,
                 command=None,
                 sliderlength=60
                 ):
        super().__init__(parent,
                         sliderlength=sliderlength,
                         highlightcolor=None,
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
                         activebackground=activebackground,
                         borderwidth=borderwidth,
                         resolution=resolution,
                         command=command
                         )
