
import mido

class MidiIO:
    def __init__(self):
        # define input and ouput USB midi
        self.outport= mido.open_output('USB-MIDI:USB-MIDI MIDI 1 24:0')
        self.inport= mido.open_input('USB-MIDI:USB-MIDI MIDI 1 24:0')
        self.inport.callback = None
        self.inport.poll()

        self.isListening = True

        #try to clear pending notes
        print("TRY TO CLEAR ==========")
        self.inport._queue._queue.mutex.acquire()
        self.inport._queue._queue.queue.clear()
        self.inport._queue._queue.all_tasks_done.notify_all()
        self.inport._queue._queue.unfinished_tasks=0
        self.inport._queue._queue.mutex.release()
        print("END ==========")

        #for msg in self.inport.iter_pending():
        #    print("pending : ", msg)
        self.showIOPorts()
        self.outport.panic()
        self.outport.reset()

    def showIOPorts(self):
        print(80*"=")
        # ['Midi Through:Midi Through Port-0 14:0', 'USB-MIDI:USB-MIDI MIDI 1 24:0']
        print( "Availables inputs: ", mido.get_input_names())
        print( "Availables outputs: ", mido.get_output_names())
        print("<== Selected input is {}".format(self.inport))
        print("==> Selected output is {}".format(self.outport))
        print(80*"=")

    def getAllMidiInputs(self):
        return mido.get_input_names()

    def getAllMidiOutputs(self):
        return mido.get_output_names()

    def setMidiInput(self, _input):
        self.inport = mido.open_input(_input)

    def setMidiOutput(self,_output):
        self.outport= mido.open_output(_output)

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
        self.inport.callback = callback

    def sendOut(self, msgtype, note):
        print("[+] sending note : ", msgtype, note)
        msg = mido.Message(msgtype, note=note)
        self.outport.send(msg)

    def panic(self):
        self.outport.panic()

    def toggleListening(self):
        if self.isListening == True:
            self.isListening=False
        else:
            self.isListening=True
        print("isListening ? " , self.isListening)
