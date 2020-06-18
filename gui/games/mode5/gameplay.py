import tkinter as tk


class Game:

    def __init__(self, parent):
        self.parent = parent

        self.parent.rowconfigure((0,1,2,3,4,5,6,7,8,9), weight = 1)

        self.parent.columnconfigure(0, weight=2)
        self.parent.columnconfigure(1, weight=1)
        self.parent.columnconfigure(2, weight=2)

        # SECTION 1 - Ear Training Note
        self.parent.section1.grid(row=0, column=0, columnspan=3, sticky="EW")
        self.parent.label1_1.grid(row=1,column=0, columnspan=1, sticky= "EWNS")
        self.parent.slider1_1.grid(row=1,column=2, columnspan=2, sticky= "EW")
        self.parent.label1_2.grid(row=2,column=0, columnspan=1, sticky= "EWNS")
        self.parent.slider1_2.grid(row=2,column=2, columnspan=2, sticky= "EW")

        # SECTION 2 - Practise licks
        self.parent.section2.grid(row=3, column=0,columnspan=3, sticky="EW")
        self.parent.label2_1.grid(row=4,column=0, columnspan=1, sticky= "EWNS")
        self.parent.slider2_1.grid(row=4,column=2, columnspan=2, sticky= "EWNS")
        self.parent.label2_2.grid(row=5,column=0, columnspan=1, sticky= "EWNS")
        self.parent.slider2_2.grid(row=5,column=2, columnspan=2, sticky= "EWNS")

        # SECTION 3 - bouttons
        self.parent.btnSaveDefault.grid(row=8, column=0, columnspan=1, sticky="S")
        self.parent.btnCancel.grid(row=8, column=2, columnspan=1, sticky="S")


#        # Audio volume
#        self.parent.label1.pack()
#        self.parent.w.pack()
#        # Interval Delay for ear training 
#        self.parent.label2.pack()
#        self.parent.w1.pack()
#        self.parent.label1.pack()
#        # interval types for earTraining chords
#        self.parent.label3.pack()
#        self.parent.btnChord1.pack()
#        self.parent.label1.pack()
#        # SaveConfig File
#        self.parent.label4.pack()
#        self.parent.btnChord2.pack()
#        self.parent.label1.pack()
#


    def destroy(self):
        print("trying destroy")
        del self


    # TODO : put config file
    # TODO : save config file automaticcally
    # TODO : load config file automatically

        
