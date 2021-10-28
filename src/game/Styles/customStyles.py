import tkinter
from tkinter import ttk


class CustomButtonStyle:

    def __init__(self):
        self.style = ttk.Style()
        # self.style.theme_use('equilux')
        # self.style.configure('TButton',
        #                      foreground="yellow",
        #                      background="black",
        #                      bordercolor='red',
        #                      # borderwidth=8,
        #                      relief="flat",
        #                      font="helvetica 24",
        #                      # highlightthickness=60,
        #                      padding=10
        #                      )
        # self.style.configure('TButton.button.focus.padding.label', background='blue')
        # self.style.configure('Label', background='red')
        # self.style.configure('.TButton',
        #                      background="blue",
        #                      foreground='red',
        #                      font='helvetica 24'
        #                      )
        # self.style.map('TButton',
        #                background=[
        #                    ('active', 'white'),
        #                    ('disabled', 'red'),
        #                    ('selected', 'red')
        #
        #                ])
        print(self.style.layout('TButton'))
        # print(self.style.layout('Button.button'))
        print(self.style.element_options('Button.button'))
        print(self.style.lookup('Button.button', 'background'))
        dir(self.style)
        a = 4

    def getStyle(self):
        return self.style
