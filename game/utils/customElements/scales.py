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


class VolumeSliderScale(tk.Scale):
    def __init__(self, *args, **kwargs):
        super(VolumeSliderScale, self).__init__(
            *args,
            troughcolor="black",
            highlightthickness=0,
            bd=1,
            font=("Courier", 12),
            width=45,
            sliderlength=55,
            sliderrelief=tk.SUNKEN,
            highlightcolor="black",
            from_=0,
            to=100,
            showvalue=0,
            orient=tk.HORIZONTAL,
            **kwargs
        )

