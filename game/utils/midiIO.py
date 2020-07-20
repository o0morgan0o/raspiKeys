
import mido


class MidiIO:
    def __init__(self, midiIn, midiOut):
        self.midoInList = self.getAllMidiInputs()
        self.midoOutList = self.getAllMidiOutputs()
        print("list:", self.midoInList, self.midoOutList)
        # define input and ouput USB midi
        # we check if the default interface is present in the list
        if midiIn in self.midoInList:
            self.inport = mido.open_input(midiIn)
        else:
            print("default IN setting not found !, use mido[0] insted")
            self.inport = self.openInput(self.midoInList, 0)

        if midiOut in self.midoOutList:
            self.outport = mido.open_output(midiOut)
            # pass
        else:
            print("default OUT setting not found !, use mido[0] insted")
            self.outport = self.openOutput(self.midoOutList, 0)

        self.resetInAndOut()

    def openInput(self, inputsArr, index):
        if len(inputsArr) > 0:
            return mido.open_input(inputsArr[index])

    def openOutput(self, outputsArr, index):
        if len(outputsArr) > 0:
            return mido.open_output(outputsArr[index])

    def resetInAndOut(self):
        try:
            self.inport.callback = None
            self.inport.poll()
            self.isListening = True

            print("TRY TO CLEAR ==========")
            self.inport._queue._queue.mutex.acquire()
            self.inport._queue._queue.queue.clear()
            self.inport._queue._queue.all_tasks_done.notify_all()
            self.inport._queue._queue.unfinished_tasks = 0
            self.inport._queue._queue.mutex.release()
            print("END ==========")

            self.showIOPorts()
            self.outport.panic()
            self.outport.reset()
        except Exception as e:
            print("Error in function resetInAndOut()", e)

    def showIOPorts(self):
        print(80*"=")
        # ['Midi Through:Midi Through Port-0 14:0', 'USB-MIDI:USB-MIDI MIDI 1 24:0']
        print("Availables inputs: ", mido.get_input_names())
        print("Availables outputs: ", mido.get_output_names())
        print("<== Selected input is {}".format(self.inport))
        print("==> Selected output is {}".format(self.outport))
        print(80*"=")

    def getAllMidiInputs(self):
        try:
            return mido.get_input_names()
        except Exception as e :
            print("Impossible to run mido_get_output_names" , e)
            return []

    def getAllMidiOutputs(self):
        try:
            return mido.get_output_names()
        except Exception as e:
            print("Impossible to run mido_get_output_names" , e)
            return  []

    def setMidiInput(self, _input):
        try:
            self.inport.close()
        except Exception as e:
            print("can't close input port.", e)
        try:
            self.inport = mido.open_input(_input)
        except Exception as e:
            print("error setting input port", e)
        self.resetInAndOut()

    def setMidiOutput(self, _output):
        try:
            self.outport.close()
        except Exception as e:
            print("can't close output port", e)
        try:
            self.outport = mido.open_output(_output)
        except Exception as e:
            print("error setting output port", e)
        self.resetInAndOut()

    def destroy(self):
        self.inport.callback = None
        self.outport.panic()
        # close ports
        self.outport.close()
        self.inport.close()
        # print("is closed output? : ",self.outport.closed)
        # print("is closed input? : ",self.inport.closed)
        #del self.inport
        #del self.outport

    def setCallback(self, callback):
        try:
            self.inport.callback = callback
        except Exception as e:
            print("error in setCallback()", e)

    def sendOut(self, msgtype, note, velocity=100):
        # print("[+] sending note : ", msgtype, note, velocity)
        msg = mido.Message(msgtype, note=note, velocity=velocity)
        self.outport.send(msg)

    def panic(self):
        self.outport.panic()

    def toggleListening(self):
        if self.isListening == True:
            self.isListening = False
        else:
            self.isListening = True
        print("isListening ? ", self.isListening)
