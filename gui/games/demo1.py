import tkinter as tk

class Demo1:
    def __init__(self,master):
        print( "launching program 1")
        self.master=master
        self.frame= tk.Frame(self.master)
        self.quitButton=tk.Button(self.frame, text= "Quit")
        self.quitButton.pack()
        self.frame.pack()
        self.game =None

    def destroy(self):
        pass

