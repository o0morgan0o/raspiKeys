#!/usr/bin/python3
import tkinter as tk
from random import choice

# import gamemodes
from games.demo0 import Demo0
from games.demo1 import Demo1

class MainApplication(tk.Frame):
    # definition de la fenetre globale
    def __init__(self, master):
        self.colors=['red', 'green', 'yellow']
        self.gameMode=0
        self.master=master
        # Main Frame
        self.master.title("RaspyKeys")
        self.master.geometry("500x500")
        self.frame=tk.Frame(self.master)

        # toolbar
        self.master.toolbar = tk.Frame(self.master, bg="blue")
        self.master.toolbar.pack(anchor=tk.CENTER, fill=tk.X)

        # toolbar buttons
        self.master.button1 = tk.Button(self.master.toolbar, text="EarTr", command=lambda: self.toggleMode(0))
        self.master.button1.pack(side=tk.LEFT)
        self.master.button2 =tk.Button(self.master.toolbar, text="Metro", command=lambda: self.toggleMode(1))
        self.master.button2.pack(side=tk.LEFT)
        self.master.button3=tk.Button(self.master.toolbar , text= "BackTrack", command=lambda: self.toggleMode(2))
        self.master.button3.pack(side=tk.LEFT)
        self.master.button4 = tk.Button(self.master.toolbar, text="Keyboard", command= lambda: self.toggleMode(3))
        self.master.button4.pack(side=tk.LEFT)
        self.master.button5 = tk.Button(self.master.toolbar, text="OFF", )
        self.master.button5.pack(side=tk.RIGHT)


        # Populate the GUI
        #self.button1= tk.Button(self.frame, text="hello", command=self.new_window)
        #self.button1.pack()

        self.frame.pack()

        # storage of the current Game Classe
        self.currentGameClass = None

        # initialization
        self.toggleMode(0)


    def toggleMode(self, intMode):
        #destroy the existing gameFrame
        try:
            self.gameFrame.pack_forget()
            self.gameFrame.destroy()
        except :
            print("no element")
 

        # recreation of the frame containing the game Mode
        self.gameFrame = tk.Frame(self.frame, bg= "red", width=200, height=200)
        # we instatiate the correct gameMode
        # TODO : handle the destruction of created threads
        try:
            del self.currentGameClass
        except:
            print("cant delete self.currentGameClass ")
        if(intMode == 0):
            self.currentGameClass = Demo0(self.gameFrame)
        elif(intMode == 1):
            self.currentGameClass = Demo1(self.gameFrame)

        #print(self.currentGameClass)
        # packing the ensemble
        self.gameFrame.pack()







if __name__ == "__main__":
    print("creating root")
    root=tk.Tk()
    MainApplication(root)
    root.mainloop()


















##TODO: make a class for every button so that it is easy to change appearance

#label1= Label(root,text="hello")
#label1.pack()

#button1 = Button(root, text = "Change color", anchor = W, command=lambda: root.configure(bg=choice(colors))) 
#button1.pack()


#root.mainloop()
#a=0

#while True:
#    label1["text"] = a
#    a+=1
#    root.update()



