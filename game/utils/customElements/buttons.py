import tkinter as tk

myfont = "Courier"


class AllButtons(tk.Button):
    def __init__(self, *args, **kwargs):
        super(AllButtons, self).__init__(*args, **kwargs)


# buttons
class BtnBlack8(AllButtons):
    def __init__(self, *args, **kwargs):
        super(BtnBlack8, self).__init__(*args, font=(myfont, 8), **kwargs, background="black", foreground="white")


class BtnBlack10(AllButtons):
    def __init__(self, *args, **kwargs):
        super(BtnBlack10, self).__init__(*args, font=(myfont, 10), **kwargs, background="black", foreground="white")


class BtnBlack12(AllButtons):
    def __init__(self, *args, **kwargs):
        super(BtnBlack12, self).__init__(*args, font=(myfont, 12), **kwargs, background="black", foreground="white")


class BtnBlack20(AllButtons):
    def __init__(self, *args, **kwargs):
        super(BtnBlack20, self).__init__(*args, font=(myfont, 20), **kwargs, background="black", foreground="white", activeforeground="yellow")


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
