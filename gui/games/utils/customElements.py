import tkinter as tk

class BtnMenu(tk.Button):
    def __init__(self, *args, **kwargs):
        super(BtnMenu, self).__init__(
            *args,
            font=("Courier", 9),
            **kwargs)

class BtnDefault(tk.Button):
    def __init__(self, *args, **kwargs):
        super(BtnDefault, self).__init__(
            *args,
       #     font=("Courier", 12),
            **kwargs)


class LblDefault(tk.Label):
    def __init__(self, *args, **kwargs):
      super(LblDefault, self).__init__(
        *args,
        foreground="blue",
      #  font=("Courier", 8),
        **kwargs
      )




# -------------------MODE 3 -----------------------
class BtnWavList(tk.Button):
    def __init__(self, *args, **kwargs):
      super(BtnWavList, self).__init__(
        *args,
        pady=0,
        fg="black",
        font=("Courier", 8),
        **kwargs
      )

class LblCurrentPlaying(tk.Label):
    def __init__(self, *args, **kwargs):
      super(LblCurrentPlaying, self).__init__(
        *args,
        pady=0,
        bg="steelBlue",
        fg="white",
        font=("Courier", 8),
        **kwargs
      )

class BtnBigButton(tk.Button):
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
        #font=("Courier", 14),
        **kwargs
      )

# ------------------ MODE 4 ------------------------
# ------------------ MODE 5 ------------------------


class LblSettings(tk.Label):
    def __init__(self, *args, **kwargs):
      super(LblSettings, self).__init__(
        *args,
        bg="steelBlue",
        fg="white",
        font=("Courier", 8),
        **kwargs
      )

class BtnSettings(tk.Button):
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

