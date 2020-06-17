import tkinter as tk
from games.utils.customElements import LblSettings
from games.utils.customElements import BtnSettings
from games.utils.customElements import BtnDefault


class Game:

    def __init__(self, parent):
        self.parent = parent

        # Audio volume
        self.parent.label1 = LblSettings(text="audioVolume")
        self.parent.label1.place(relx=.5, rely=.2, anchor=tk.N)
        w = tk.Scale( from_=0, to=200, orient=tk.HORIZONTAL)
        w.place(relx=.5, rely=.25, anchor=tk.N)

        # Interval Delay for ear training 
        self.parent.label2 = LblSettings(text="delay between notes (ms)")
        self.parent.label2.place(relx=.5, rely=.35, anchor=tk.N)
        w1 = tk.Scale( from_=0, to=1000, orient=tk.HORIZONTAL)
        w1.place(relx=.5, rely=.4, anchor=tk.N)

        # interval types for earTraining chords
        self.parent.label3 = LblSettings(text="include chords")
        self.parent.label3.place(relx=.5, rely=.6, anchor=tk.N)
        self.parent.btnChord1 = BtnDefault(text="9th chords") 
        self.parent.btnChord1.place(relx=.5,rely= .65, anchor=tk.N)

        # SaveConfig File
        self.parent.label4 = LblSettings(text="save conf as default")
        self.parent.label4.place(relx=.5, rely=.7, anchor=tk.N)
        self.parent.btnChord2 = BtnDefault(text="save") 
        self.parent.btnChord2.place(relx=.5,rely= .75, anchor=tk.N)



    def destroy(self):
        print("trying destroy")
        del self


    # TODO : put config file
    # TODO : save config file automaticcally
    # TODO : load config file automatically

        
