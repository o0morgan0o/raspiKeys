import tkinter as tk
from tkinter import messagebox
from src.game.utils.customElements.labels import *
from src.game.utils.customElements.buttons import *
from src.game.utils.utilFunctions import *
from src.game.autoload import Autoload
import json
from src.game import env


class Game:
    def __init__(self, parentLeft, parentRight, config):
        # get audio instance to be sure the audio is loaded
        self.audio = Autoload().getInstanceAudio()
        self.midiIO = Autoload().getInstance()
        self.window = None
        self.midiInstance = None
        self.labelCurrentIn = None
        self.labelCurrentOut = None

        self.config = config
        self.parentRight = parentRight
        self.parentRight.btnConfig.config(command=self.openMidiPanel)

        self.loadInitialSettings()
        self.parentRight.btnSaveDefault.config(command=self.saveConfig)

    def saveConfig(self):
        # we must get all the parameters used in the app
        default_mode = 0  # for this time, default mode is hardcoded
        question_delay = self.parentRight.slider1_1.get()
        difficulty = self.parentRight.slider1_2.get()
        times_each_transpose = self.parentRight.slider2_1.get()
        nb_of_transpose_before_change = self.parentRight.slider2_2.get()
        midi_in = self.midiIO.inport.name
        midi_out = self.midiIO.outport.name

        currentConfig = loadConfig()
        print("settings: ", question_delay, difficulty, midi_in)
        currentConfig["default_mode"] = default_mode
        currentConfig["question_delay"] = question_delay
        currentConfig["difficulty"] = difficulty
        currentConfig["times_each_transpose"] = times_each_transpose
        currentConfig["nb_of_transpose_before_change"] = nb_of_transpose_before_change,
        currentConfig["MIDI_interface_in"] = midi_in
        currentConfig["MIDI_interface_out"] = midi_out
        json_object = json.dumps(currentConfig, indent=4)
        print("trying to save...", json_object)
        savedFile = saveConfig(currentConfig)
        if savedFile:
            messagebox.showinfo(title="save as default", message="Config saved successfully")
        else:
            messagebox.showerror(title="save as default", message="Failed at save config")

    def openMidiPanel(self):
        print("opening settings")
        self.window = tk.Toplevel(self.parentRight, cursor="none")
        self.window.attributes("-topmost", True)
        self.window.config(background="yellow")
        self.window.geometry("%sx%s" % (env.FULL_SCREEN_W, env.FULL_SCREEN_H))
        yplacement = 10
        label = LblSettings(self.window, text="click on your midi IN device:")
        label.place(x=0, y=yplacement, width=200, height=30)

        self.labelCurrentIn = LblSettings(self.window)
        try:
            self.labelCurrentIn.config(text="actual In is : " + self.midiIO.inport.name)
        except:
            self.labelCurrentIn.config(text="Can \'t retrieve info")

        yplacement += 30
        self.labelCurrentIn.place(x=0, y=yplacement, width=320, height=30)

        # get all availables interface
        self.midiInstance = Autoload().getInstance()

        # midiInstance.showIOPorts() # just to shoe in the console
        midi_inputs = self.midiInstance.getAllMidiInputs()
        midi_outputs = self.midiInstance.getAllMidiOutputs()
        print(midi_inputs, midi_outputs)

        yplacement += 40

        for mInput in midi_inputs:
            if not "RtMidi" in mInput:
                btn = BtnBlack8(self.window, text=mInput)
                btn.config(command=lambda mInput=mInput: self.setIn(mInput), wraplength=300)
                btn.place(x=10, y=yplacement, width=300, height=30)
                yplacement += 30

        yplacement += 15

        label2 = LblSettings(self.window, text="click on your midi OUT device:")
        label2.place(x=0, y=yplacement, width=320, height=30)

        self.labelCurrentOut = LblSettings(self.window)
        try:
            self.labelCurrentOut.config(text="actual out is " + self.midiIO.outport.name)
        except:
            self.labelCurrentOut.config(text="Can\'t retrieve out !")

        yplacement += 30
        self.labelCurrentOut.place(x=0, y=yplacement, width=320, height=30)

        yplacement += 10

        for mOutput in midi_outputs:
            if not "RtMidi" in mOutput:
                btn = BtnBlack8(self.window, text=mOutput)
                btn.config(command=lambda mOutput=mOutput: self.setOut(mOutput), wraplength=300)
                yplacement += 30
                btn.place(x=0, y=yplacement, width=320, height=30)

        yplacement += 15
        btnClose = BtnBlack20(self.window, text="Close", command=self.quitConfig)
        btnClose.place(x=80, y=380, width=160, height=80)

    def setIn(self, mInput):
        print("input selected: ", mInput)
        # TODO : check if it works
        self.midiInstance.setMidiInput(mInput)
        self.config["MIDI_interface_in"] = mInput
        self.labelCurrentIn.config(text="actual In is : " + mInput)

    def setOut(self, mOutput):
        # TODO : check if it works
        print("output selected:", mOutput)
        self.midiInstance.setMidiOutput(mOutput)
        self.config["MIDI_interface_out"] = mOutput
        self.labelCurrentOut.config(text="actual Out is : " + mOutput)

    def quitConfig(self):
        self.window.destroy()

    def destroy(self):
        print("trying destroy")
        del self

    def loadInitialSettings(self):
        value = int(self.config["question_delay"])
        print(value)
        self.parentRight.slider1_1.set(value)
