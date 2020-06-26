import tkinter as tk

myfont="Courier"

# labels in each size
class MyLabel8(tk.Label):
  def __init__(self,*args, **kwargs):
      super(MyLabel8, self).__init__( *args, foreground="white", font=(myfont, 8), background="black", **kwargs)
class MyLabel10(tk.Label):
  def __init__(self,*args, **kwargs):
      super(MyLabel10, self).__init__( *args, foreground="white", font=(myfont, 10), background="black", **kwargs)

class MyLabel12(tk.Label):
  def __init__(self,*args, **kwargs):
      super(MyLabel12, self).__init__( *args, foreground="white", font=(myfont, 12), background="black", **kwargs)

class MyLabel18(tk.Label):
  def __init__(self,*args, **kwargs):
      super(MyLabel18, self).__init__( *args, foreground="white", font=(myfont, 18), background="black", **kwargs)

class MyLabel24(tk.Label):
  def __init__(self,*args, **kwargs):
      super(MyLabel24, self).__init__( *args, foreground="white", font=(myfont, 24), background="black", **kwargs)
class MyLabel30(tk.Label):
  def __init__(self,*args, **kwargs):
      super(MyLabel30, self).__init__( *args, foreground="white", font=(myfont, 30), background="black", **kwargs)

class MyLabel40(tk.Label):
  def __init__(self,*args, **kwargs):
      super(MyLabel40, self).__init__( *args, foreground="white", font=(myfont, 40), background="black", **kwargs)



# buttons 
class BtnBlack10(tk.Button):
  def __init__(self, *args, **kwargs):
    super(BtnBlack10, self).__init__( *args, font=(myfont, 10), **kwargs, background="black", foreground="white")
class BtnBlack12(tk.Button):
  def __init__(self, *args, **kwargs):
    super(BtnBlack12, self).__init__( *args, font=(myfont, 12), **kwargs, background="black", foreground="white")
class BtnBlack20(tk.Button):
  def __init__(self, *args, **kwargs):
    super(BtnBlack20, self).__init__( *args, font=(myfont, 20), **kwargs, background="black", foreground="white")


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

# -------------------MODE 0 ----------------------
class LblMode0(tk.Label):
    def __init__(self,*args, **kwargs):
        super(LblMode0, self).__init__(
                *args,
                foreground="white",
                font=("Courier", 28),
                background="black",
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
class LblMode3(tk.Label):
    def __init__(self,*args, **kwargs):
        super(LblMode3, self).__init__(
                *args,
                foreground="white",
                font=("Courier", 14),
                background="black",
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
