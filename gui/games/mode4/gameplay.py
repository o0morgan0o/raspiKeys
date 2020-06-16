import tkinter as tk
from games.utils.customElements import BtnDefault
from games.utils.customElements import LblDefault



class Game:

    def __init__(self, parent):
        self.parent=parent

        self.parent.lblMessage = LblDefault(text="there are x licks in the base")
        self.parent.lblMessage.place(relx=.5, rely=.3, anchor=tk.N)

        self.parent.btnRecord = BtnDefault(text="record")
        self.parent.btnRecord.place(relx=.5, rely=.2, anchor=tk.N)

        # TODO: voir si on peut loader une treeview

        self.parent.btnStart = BtnDefault(text="startPractice")
        self.parent.btnStart.place(relx=.5, rely=.4, anchor=tk.N)

        # TODO : il faut que le programme demande une basse
        # ensuite on joue le lick
        # en play: le programme joue la basse et donne en indice le premier interval


    def destroy(self):
        print("trying destroy")
        del self
