import tkinter

from src.game.autoload import Autoload
from src.game.utils.config import getMidiInterfaceIn, getMidiInterfaceOut, updateMidiOutConfig, \
    updateMidiInConfig
from src.game.utils.questionNote import playWinMelody


class OptionsViewModel:
    def __init__(self, view):
        self.view = view
        self.midiIO = Autoload.get_instance().getMidiInstance()
        self.midiIO.setCallback(self.handleMIDIInput)
        self.midiIO.setListening(True)
        self.midiInstance = None
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
        self.view.updateUiMidiInAndOut(midi_in, midi_out)
        return midi_in, midi_out

    def midiInChangeCallback(self, event):
        selection = event.widget.curselection()
        index = selection[0]
        item_selected = event.widget.get(index)
        self.view.updateUiMidiIn(item_selected)
        self.midiIO.setMidiInput(item_selected)
        self.midiIO.setCallback(self.handleMIDIInput)
        updateMidiInConfig(item_selected)

    def midiOutChangeCallback(self, event):
        selection = event.widget.curselection()
        index = selection[0]
        item_selected = event.widget.get(index)
        self.view.updateUiMidiOut(item_selected)
        self.midiIO.setMidiOutput(item_selected)
        self.midiIO.setCallback(self.handleMIDIInput)
        updateMidiOutConfig(item_selected)

    def playTestNotes(self):
        playWinMelody(self.midiIO, 100, callback_after_melody=self.view.didYouHearMelody)

    def handleMIDIInput(self, msg):
        # check if user has midi  listen
        if not self.midiIO.getListeningState():
            print("[--] ignoring queue message...", msg)
            return
        print("[-]receiving something", msg)
        self.view.updateUiMIDIMessageReceived(str(msg))

    def destroyViewModel(self):
        print("Deleting OptionsViewModel")
        self.midiIO.cancelCallback()
        self.midiIO.setListening(False)
