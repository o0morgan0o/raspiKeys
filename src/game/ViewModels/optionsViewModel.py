import json
import tkinter
from tkinter import messagebox

from src.game import env
from src.game.autoload import Autoload
from src.game.utils.config import loadConfig, getMidiInterfaceIn, getMidiInterfaceOut, updateMidiOutConfig, \
    updateMidiInConfig
from src.game.utils.customElements.buttons import *
from src.game.utils.customElements.labels import *
from enum import Enum


class ViewStrings(Enum):
    NO_MIDI_IN_INTERFACE_SELECTED = "No Midi-in interface selected !!"
    NO_MIDI_OUT_INTERFACE_SELECTED = "No Midi-out interface selected !!"
    CURRENT_MIDI_IN = "MIDI in: "
    CURRENT_MIDI_OUT = "MIDI out: "
    LABEL_HEADER_OPTIONS = "OPTIONS:"


class OptionsViewModel:
    def __init__(self, view, config: dict):
        self.config = config
        self.view = view
        self.midiIO = Autoload.get_instance().getMidiInstance()
        self.midiInstance = None
        self.window = None
        self.labelCurrentIn = None
        self.labelCurrentOut = None

        (current_in, current_out) = self.loadCurrentMidiInputsAndOutputs()
        self.loadPossibleMidiInputsAndOutputsInList(current_in, current_out)

    @staticmethod
    def highlightItemInListbox(listbox: tkinter.Listbox, item_string: str):
        all_fields = listbox.get(0, listbox.size())
        if len(all_fields) == 0:
            print("Empty listbox ! {}".format(listbox.__str__()))
            return
        counter = 0
        for field in all_fields:
            if item_string == field:
                listbox.selection_set(counter)
                break
            counter += 1

    def loadPossibleMidiInputsAndOutputsInList(self, current_midi_in: str, current_midi_out: str):
        midi_inputs = self.midiIO.getAllMidiInputs()
        midi_outputs = self.midiIO.getAllMidiOutputs()
        for midi_input in midi_inputs:
            self.view.midiInListbox.insert('end', midi_input)
        for midi_output in midi_outputs:
            self.view.midiOutListbox.insert('end', midi_output)

        # We highlight the default selected MIDI interfaces just after we fill the listbox with possibles interfaces
        self.highlightItemInListbox(self.view.midiInListbox, current_midi_in)
        self.highlightItemInListbox(self.view.midiOutListbox, current_midi_out)

    def loadCurrentMidiInputsAndOutputs(self):
        midi_in = getMidiInterfaceIn()
        midi_out = getMidiInterfaceOut()
        # ternary operator
        self.view.currentMidiIn.config(text=(midi_in, ViewStrings.NO_MIDI_IN_INTERFACE_SELECTED.value)[midi_in == ""])
        self.view.currentMidiOut.config(text=(midi_out, ViewStrings.NO_MIDI_OUT_INTERFACE_SELECTED.value)[midi_out == ""])
        return midi_in, midi_out

    def midiInChangeCallback(self, event):
        selection = event.widget.curselection()
        index = selection[0]
        item_selected = event.widget.get(index)
        self.view.currentMidiIn.config(text=ViewStrings.CURRENT_MIDI_IN.value + item_selected)
        self.midiIO.setMidiInput(item_selected)
        updateMidiInConfig(item_selected)

    def midiOutChangeCallback(self, event):
        selection = event.widget.curselection()
        index = selection[0]
        item_selected = event.widget.get(index)
        self.view.currentMidiOut.config(text=ViewStrings.CURRENT_MIDI_OUT.value + item_selected)
        self.midiIO.setMidiOutput(item_selected)
        updateMidiOutConfig(item_selected)

    # def saveConfig(self):
    #     # we must get all the parameters used in the app
    #     default_mode = 0  # for this time, default mode is hardcoded
    #     question_delay = self.parentRight.slider1_1.get()
    #     difficulty = self.parentRight.slider1_2.get()
    #     times_each_transpose = self.parentRight.slider2_1.get()
    #     nb_of_transpose_before_change = self.parentRight.slider2_2.get()
    #     midi_in = self.midiIO.in_port.name
    #     midi_out = self.midiIO.out_port.name
    #
    #     currentConfig = loadConfig()
    #     print("settings: ", question_delay, difficulty, midi_in)
    #     currentConfig["default_mode"] = default_mode
    #     currentConfig["question_delay"] = question_delay
    #     currentConfig["difficulty"] = difficulty
    #     currentConfig["times_each_transpose"] = times_each_transpose
    #     currentConfig["nb_of_transpose_before_change"] = nb_of_transpose_before_change,
    #     currentConfig["MIDI_interface_in"] = midi_in
    #     currentConfig["MIDI_interface_out"] = midi_out
    #     json_object = json.dumps(currentConfig, indent=4)
    #     print("trying to save...", json_object)
    #     savedFile = saveConfig(currentConfig)
    #     if savedFile:
    #         messagebox.showinfo(title="save as default", message="Config saved successfully")
    #     else:
    #         messagebox.showerror(title="save as default", message="Failed at save config")

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
            self.labelCurrentIn.config(text="actual In is : " + self.midiIO.in_port.name)
        except:
            self.labelCurrentIn.config(text="Can \'t retrieve info")

        yplacement += 30
        self.labelCurrentIn.place(x=0, y=yplacement, width=320, height=30)

        # get all availables interface
        self.midiInstance = Autoload.get_instance().getMidiInstance()

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
            self.labelCurrentOut.config(text="actual out is " + self.midiIO.out_port.name)
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
