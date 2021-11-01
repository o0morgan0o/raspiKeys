import tkinter as tk

myfont = "Courier"


# ================LABELS================================

class AllLabels(tk.Label):
    def __init__(self, *args, **kwargs):
        super(AllLabels, self).__init__(*args,
                                        # activebackground="black",
                                        **kwargs)


# labels in each size
class MyLabel8(AllLabels):
    def __init__(self, *args, **kwargs):
        super(MyLabel8, self).__init__(*args, foreground="white", font=(myfont, 8), background="black", **kwargs)


class MyLabel10(AllLabels):
    def __init__(self, *args, **kwargs):
        super(MyLabel10, self).__init__(*args, foreground="white", font=(myfont, 10), background="black", **kwargs)


class MyLabel12(AllLabels):
    def __init__(self, *args, **kwargs):
        super(MyLabel12, self).__init__(*args, foreground="white", font=(myfont, 12), background="black", **kwargs)


class MyLabel18(AllLabels):
    def __init__(self, *args, **kwargs):
        super(MyLabel18, self).__init__(*args, foreground="white", font=(myfont, 18), background="black", **kwargs)


class MyLabel24(AllLabels):
    def __init__(self, *args, **kwargs):
        super(MyLabel24, self).__init__(*args, foreground="white", font=(myfont, 24), background="black", **kwargs)


class MyLabel30(AllLabels):
    def __init__(self, *args, **kwargs):
        super(MyLabel30, self).__init__(*args, foreground="white", font=(myfont, 30), background="black", **kwargs)


class MyLabel40(AllLabels):
    def __init__(self, *args, **kwargs):
        super(MyLabel40, self).__init__(*args, foreground="white", font=(myfont, 40), background="black", **kwargs)


class LblDefault(AllLabels):
    def __init__(self, *args, **kwargs):
        super(LblDefault, self).__init__(
            *args,
            foreground="blue",
            #  font=("Courier", 8),
            **kwargs
        )


# -------------------MODE 0 ----------------------
class LblMode0(AllLabels):
    def __init__(self, *args, **kwargs):
        super(LblMode0, self).__init__(
            *args,
            foreground="white",
            font=("Courier", 28),
            background="black",
            **kwargs
        )


# ======================BUTTONS===============================
class LblCurrentPlaying(AllLabels):
    def __init__(self, *args, **kwargs):
        super(LblCurrentPlaying, self).__init__(
            *args,
            pady=0,
            bg="steelBlue",
            fg="white",
            font=("Courier", 8),
            **kwargs
        )


class LblMode3(AllLabels):
    def __init__(self, *args, **kwargs):
        super(LblMode3, self).__init__(
            *args,
            foreground="white",
            font=("Courier", 14),
            background="black",
            **kwargs
        )


class LblSettings(AllLabels):
    def __init__(self, *args, **kwargs):
        super(LblSettings, self).__init__(
            *args,
            bg="steelBlue",
            fg="white",
            font=("Courier", 8),
            **kwargs
        )
