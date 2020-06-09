from tkinter import * 
from random import choice


def toggleMode(intMode):
    pass

def  exitAll():
    pass


colors = ['red', 'green', 'yellow']
mode = 0

root=Tk() 
#root.geometry("500x500")
root.attributes('-fullscreen', True)
root.title("RaspyKeys") 


toolbar= Frame(root, bg="blue")
toolbar.pack()
button1 = Button(toolbar, text="EarTr", command=lambda: toggleMode(0))
button1.grid(row=0, column=0)
button2 = Button(toolbar, text="Metro", command=lambda: toggleMode(1))
button2.grid(row=0, column=1)
button3=Button(toolbar , text= "BackTrack", command=lambda: toggleMode(2))
button3.grid(row=0, column=2)
button4 = Button(toolbar, text="Keyboard", command= lambda: toggleMode(3))
button4.grid(row=0, column=3)
button5 = Button(toolbar, text="OFF", command=exitAll)
button5.grid(row=0,column=4)



label1= Label(root,text="hello")
label1.pack()

button1 = Button(root, text = "Change color", anchor = W, command=lambda: root.configure(bg=choice(colors))) 
button1.pack()


#root.mainloop()
a=0

while True:
    label1["text"] = a
    a+=1
    root.update()



