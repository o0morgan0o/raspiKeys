import time
import threading
import random
from threading import Timer
import mido
import simpleaudio as sa

from games.utils.waitingNote import WaitingNote
from games.utils.questionNote import QuestionNote
from games.utils.midiIO import MidiIO
from games.utils.utilFunctions import formatOutputInterval
from games.utils.sounds import Sound

from games.utils.questionNote import CustomNote
from games.utils.questionNote import Melody

""" the mode 0 is for eartraining on a SINGLE INTERVAL
"""
class Game:

    def __init__(self, parent):
        self.parent = parent


    def changeAllBg(self, newColor):
        self.parent.label1["bg"] = newColor
        self.parent.label2["bg"] = newColor
        self.parent.label3["bg"] = newColor
        self.parent.label1["fg"] = "white"
        self.parent.label2["fg"] = "white"
        self.parent.label3["fg"] = "white"
        

        
 
