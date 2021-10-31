import mido
import logging

from src.game.utils.midiIO import MidiIO
from src.game.utils.audio import Audio
from src.game.utils.config import getMidiInterfaceIn, getMidiInterfaceOut


class Autoload:
    """Class used for singleton pattern, for storing global midiIO config"""

    __instance = None

    def __init__(self):
        if Autoload.__instance is not None:
            raise Exception("ERROR !!: Don't instantiate Autoload class, use get_instance method.")

        print("initialization...")
        self.configIn = getMidiInterfaceIn()
        self.configOut = getMidiInterfaceOut()
        # we try to handle midi config if config values are null for any reason
        if self.configIn == "":
            try:
                self.configIn = mido.get_input_names()[0]
            except Exception as e:
                print("ERROR: No midi input listed in mido !!")
                logging.exception(e)
        if self.configOut == "":
            try:
                self.configOut = mido.get_output_names()[0]
            except Exception as e:
                print("ERROR: No midi output listed in mido !!")
                logging.exception(e)
        print("default interface :", self.configIn, self.configOut)
        self.midiIO = MidiIO(self.configIn, self.configOut)
        self.sound = Audio()
        self.sound.initialize()

    @staticmethod
    def get_instance():
        if Autoload.__instance is None:
            print("Creation of instance")
            Autoload.__instance = Autoload()
        return Autoload.__instance

    def getMidiInstance(self):
        return self.midiIO

    def getAudioInstance(self):
        return self.sound
