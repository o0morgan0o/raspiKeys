import logging

import mido


class MidiIO:

    def __init__(self, midi_in: str, midi_out: str):
        self.isListening = True
        self.midoInList = self.getAllMidiInputs()
        self.midoOutList = self.getAllMidiOutputs()
        self.midiVolume = 1

        print("mido MIDI I/O initial list:", self.midoInList, self.midoOutList)
        # we check if the default interface is present in the list
        if midi_in in self.midoInList:
            self.in_port = mido.open_input(midi_in)
        else:
            print("default midi_in_interface config not found !, use mido_in[0] instead")
            self.in_port = self.openInput(self.midoInList, 0)

        if midi_out in self.midoOutList:
            self.out_port = mido.open_output(midi_out)
        else:
            print("default midi_out_interface config not found !, use mido_out[0] instead")
            self.out_port = self.openOutput(self.midoOutList, 0)

        self.resetInAndOut()

    def setMidiVolume(self, midi_volume: int):
        self.midiVolume = midi_volume

    def getMidiVolume(self) -> int:
        return self.midiVolume

    # noinspection PyProtectedMember
    def resetInAndOut(self):
        try:
            self.in_port.callback = None
            self.in_port.poll()

            print("===== MIDO RESET =====")
            self.in_port._queue._queue.mutex.acquire()
            self.in_port._queue._queue.queue.clear()
            self.in_port._queue._queue.all_tasks_done.notify_all()
            self.in_port._queue._queue.unfinished_tasks = 0
            self.in_port._queue._queue.mutex.release()
            print("END ==========")

            self.showIOPorts()
            self.out_port.panic()
            self.out_port.reset()
        except Exception as e:
            print("Error in function resetInAndOut()")
            logging.exception(e)

    def showIOPorts(self):
        print(80 * "=")
        print("Available inputs: ", mido.get_input_names())
        print("Available outputs: ", mido.get_output_names())
        print("<== Selected input is {}".format(self.in_port))
        print("==> Selected output is {}".format(self.out_port))
        print(80 * "=")

    def setMidiInput(self, _input):
        self.resetInAndOut()
        try:
            self.in_port.close()
        except BaseException as e:
            print("can't close input port.", e)
        try:
            self.in_port = mido.open_input(_input)
        except BaseException as e:
            print("error setting input port", e)
        print("LISTENING ?????? ", self.isListening)

    def setMidiOutput(self, _output):
        self.resetInAndOut()
        try:
            self.out_port.close()
        except BaseException as e:
            print("can't close output port", e)
        try:
            self.out_port = mido.open_output(_output)
        except BaseException as e:
            print("error setting output port", e)

    def destroy(self):
        self.in_port.callback = None
        self.out_port.panic()
        # close ports
        self.out_port.close()
        self.in_port.close()

    def setCallback(self, callback):
        try:
            self.in_port.callback = callback
        except Exception as e:
            print("error in setCallback()", e)

    def sendOut(self, msg_type, note: int, velocity: int = 100):
        # we map the velocity with the global midi volume (global midi_volume is mapped from 0 to 1)
        out_velocity = int(velocity * self.midiVolume)
        print("[+] sending note : ", msg_type, note, out_velocity)
        msg = mido.Message(msg_type, note=note, velocity=out_velocity)
        self.out_port.send(msg)

    def panic(self):
        self.out_port.panic()


    def getListeningState(self) -> bool:
        return self.isListening

    def setListening(self, is_listening: bool):
        self.isListening = is_listening
        print("isListening ? ", self.isListening)
        # if self.isListening:
        #     self.isListening = False
        # else:
        #     self.isListening = True

    @staticmethod
    def getAllMidiInputs():
        try:
            return mido.get_input_names()
        except BaseException as e:
            print("Impossible to run mido_get_input_names", e)
            return []

    @staticmethod
    def getAllMidiOutputs():
        try:
            return mido.get_output_names()
        except BaseException as e:
            print("Impossible to run mido_get_output_names", e)
            return []

    @staticmethod
    def openInput(inputs_arr: dict, index: int):
        if len(inputs_arr) > 0:
            return mido.open_input(inputs_arr[index])

    @staticmethod
    def openOutput(outputs_arr, index):
        if len(outputs_arr) > 0:
            return mido.open_output(outputs_arr[index])
