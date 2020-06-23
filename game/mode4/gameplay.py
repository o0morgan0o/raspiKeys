import tkinter as tk
from utils.customElements import LblSettings
from utils.customElements import BtnSettings
from autoload import Autoload


class Game:

    def __init__(self, parent):
        self.parent = parent

        self.parent.btnConfig.config(command= self.openMidiPanel)


    def openMidiPanel(self):
        print("opening settings" )
        self.window = tk.Toplevel(self.parent)
        label = LblSettings(self.window, text="click on your midi IN device:")
        # label.grid(row=0, column=0)
        label.pack()

        # get all availables interface 
        self.midiInstance = Autoload().getInstance()

        #midiInstance.showIOPorts() # just to shoe in the console
        midi_inputs = self.midiInstance.getAllMidiInputs()
        midi_outputs= self.midiInstance.getAllMidiOutputs()
        print(midi_inputs, midi_outputs)

        counter = 0
        
        for mInput in midi_inputs:
            btn = tk.Button(self.window, text=mInput)
            btn.config(command= lambda mInput=mInput: self.setIn(mInput))
            btn.pack()
            counter+=1

        label2 = LblSettings(self.window, text="click on your midi OUT device:")
        # label2.grid(row=counter+1, column=0)
        label2.pack()

        for mOutput in midi_outputs:
            btn = tk.Button(self.window, text=mOutput)
            btn.config(command= lambda mOutput=mOutput: self.setOut(mOutput))
            btn.pack()
            counter+=1
        
        btnClose = BtnSettings(self.window, text="Close", command=self.quitConfig)
        btnClose.pack()

    def setIn(self, mInput):
        print("input selected: " , mInput)
        # TODO : check if it works
        self.midiInstance.setMidiInput(mInput)

    def setOut(self,mOutput):
        # TODO : check if it works
        print("output selected:" , mOutput)
        self.midiInstance.setMidiInput(mOutput)

    def quitConfig(self):
        self.window.destroy()




    def destroy(self):
        print("trying destroy")
        del self


    # TODO : put config file
    # TODO : save config file automaticcally
    # TODO : load config file automatically

        
