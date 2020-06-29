import tkinter as tk

class SettingsScale(tk.Scale):
    def __init__(self, *args, **kwargs):
      super(SettingsScale, self).__init__(
        *args,
        bd=0,
        # bg="black",
        # fg="white",
        font=("Courier", 12),
        width=30,
        sliderlength=40,
        **kwargs
      )