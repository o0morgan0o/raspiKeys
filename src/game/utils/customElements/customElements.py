import tkinter as tk
from src.game.utils.colors import Colors
import os

my_font = "Courier"
DEFAULT_FONT_NAME = "Helvetica"
DEFAULT_FONT_SIZE = 12
DEFAULT_FONT = (DEFAULT_FONT_NAME, DEFAULT_FONT_SIZE)
DEFAULT_PADDING_X = 20
DEFAULT_PADDING_Y = 5


class CustomButton(tk.Button):
    def __init__(self, parent: tk.Frame, text="",
                 filename: str = None,
                 relief='flat',
                 font=DEFAULT_FONT,
                 background=Colors.BACKGROUND,
                 foreground=Colors.TEXT,
                 takefocus=0,
                 command=None,
                 wraplength=0,
                 padx=0,
                 pady=0,
                 width=None,
                 height=None
                 ):

        if filename is not None:
            img_file_path = os.path.join(os.getcwd(), 'game', 'utils', 'customElements', 'src_images', filename)
            self.img_file = tk.PhotoImage(file=img_file_path)
        else:
            self.img_file = None

        super().__init__(parent, text=text,
                         relief=relief,
                         overrelief=relief,
                         padx=padx,
                         pady=pady,
                         font=font,
                         background=background,
                         activebackground=background,
                         foreground=foreground,
                         activeforeground=foreground,
                         takefocus=takefocus,
                         command=command,
                         highlightthickness=0,
                         wraplength=wraplength,
                         image=self.img_file,
                         compound="center",
                         width=width,
                         height=height
                         )


class CustomLabel(tk.Label):
    def __init__(self, parent: tk.Frame,
                 text=None,
                 font=DEFAULT_FONT,
                 justify=None,
                 background=Colors.BACKGROUND,
                 foreground=Colors.TEXT,
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
                 background=Colors.BACKGROUND,
                 relief=tk.FLAT,
                 from_=0,
                 to=100,
                 orient=tk.HORIZONTAL,
                 width=None,
                 label=None,
                 showvalue=0,
                 troughcolor=Colors.TEXT,
                 ):
        super().__init__(parent,
                         highlightcolor="green",
                         highlightthickness=0,
                         background=background,
                         relief='flat',
                         from_=from_,
                         to=to,
                         orient=orient,
                         width=width,
                         # label=label,
                         showvalue=showvalue,
                         troughcolor=troughcolor,
                         borderwidth=0,
                         )


class AllButtons(tk.Button):
    def __init__(self, *args, **kwargs):
        super(AllButtons, self).__init__(*args, **kwargs)


# buttons
class BtnBlack8(AllButtons):
    def __init__(self, *args, **kwargs):
        super(BtnBlack8, self).__init__(*args, font=(my_font, 8), **kwargs, background="black", foreground="white")


class BtnBlack10(AllButtons):
    def __init__(self, *args, **kwargs):
        super(BtnBlack10, self).__init__(*args, font=(my_font, 10), **kwargs, background="black", foreground="white")


class BtnBlack12(AllButtons):
    def __init__(self, *args, **kwargs):
        super(BtnBlack12, self).__init__(*args, font=(my_font, 12), **kwargs, background="black", foreground="white")


class BtnBlack20(AllButtons):
    def __init__(self, *args, **kwargs):
        super(BtnBlack20, self).__init__(*args, font=(my_font, 20), **kwargs, background="black", foreground="white", )


class BtnMenu(AllButtons):
    def __init__(self, *args, **kwargs):
        super(BtnMenu, self).__init__(*args, font=("Courier", 9), bd=0, highlightthickness=0, **kwargs)


class BtnDefault(AllButtons):
    def __init__(self, *args, **kwargs):
        super(BtnDefault, self).__init__(
            *args,
            #     font=("Courier", 12),
            **kwargs
        )


# -------------------MODE 3 -----------------------
class BtnWavList(AllButtons):
    def __init__(self, *args, **kwargs):
        super(BtnWavList, self).__init__(*args, pady=0, fg="black", font=("Courier", 8), **kwargs)


class BtnBigButton(AllButtons):
    def __init__(self, *args, **kwargs):
        super(BtnBigButton, self).__init__(
            *args,
            bg="steelBlue",
            fg="white",
            #        width=8,
            #        height=3,
            #        wraplength=100,
            #        bd=3,
            #        relief=tk.GROOVE,
            foreground="black",
            # font=("Courier", 14),
            **kwargs
        )


# ------------------ MODE 4 ------------------------
# ------------------ MODE 5 ------------------------


class BtnSettings(AllButtons):
    def __init__(self, *args, **kwargs):
        super(BtnSettings, self).__init__(
            *args,
            bg="steelBlue",
            fg="white",
            width=8,
            height=3,
            wraplength=100,
            bd=3,
            relief=tk.GROOVE,
            foreground="black",
            font=("Courier", 14),
            **kwargs
        )
