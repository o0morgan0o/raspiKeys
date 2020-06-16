import os
import time
import threading
import random
from threading import Timer
import mido
import simpleaudio as sa
import tkinter as tk

from games.utils.sounds import Sound

class Game:

    def __init__(self, parent):
        self.parent = parent
        self.sound = Sound()
        self.tracksMp3 = self.sound.loadBacktracksMp3()
        self.parent.btnPlay.config(command=self.toggleBacktrack)
        self.parent.btnRandom.config(command=self.playRandom)
        self.isPlaying = False

        #for filename in self.tracksMp3:
        #    self.sound.convertToWav(filename)


        self.tracksWav = self.sound.loadBacktracksWav()
        self.activeSamples = self.pickRandomSamples()
        self.currentTrack = self.activeSamples[0]

        self.showRandomTracks()

        self.playBacktrack()


    def changeAllBg(self, newColor):
        self.parent.label1["bg"] = newColor
        self.parent.label2["bg"] = newColor
        self.parent.label3["bg"] = newColor
        self.parent.label1["fg"] = "white"
        self.parent.label2["fg"] = "white"
        self.parent.label3["fg"] = "white"

    def destroy(self):
        # TODO : make a destroy which destroy stored audio
        self.sound.unloadAudio()
        pass

    def showRandomTracks(self):
            name = os.path.basename(self.activeSamples[0])
            self.parent.randTrack0.config(text=name, command=lambda: self.changeTrack(0))
            name = os.path.basename(self.activeSamples[1])
            self.parent.randTrack1.config(text=name, command=lambda: self.changeTrack(1))
            name = os.path.basename(self.activeSamples[2])
            self.parent.randTrack2.config(text=name, command=lambda: self.changeTrack(2))
            name = os.path.basename(self.activeSamples[3])
            self.parent.randTrack3.config(text=name, command=lambda: self.changeTrack(3))

            name = os.path.basename(self.currentTrack)
            self.parent.labelCurrent.config(text="Currently Playing:\n"+ name)

    def changeTrack(self, index):
        try :
            self.stopBacktrack()
        except : 
            print( "cant stop track during changeTrack.")

        self.currentTrack = self.activeSamples[index]
        self.playBacktrack()
        self.isPlaying = True

    def pickRandomSamples(self):
        return  random.sample(self.tracksWav, 4)


    
    def playRandom(self):
        self.activeSamples = self.pickRandomSamples()
        self.showRandomTracks()
        if self.isPlaying == True:
            self.sound.stopPlay()
        self.currentTrack = self.activeSamples[0]
        self.isPlaying =False
        self.playBacktrack()

    def toggleBacktrack(self):
        if self.isPlaying == True:
            self.isPlaying= False
            self.stopBacktrack()
        else :
            self.isPlaying = True
            self.playBacktrack()

    def stopBacktrack(self):
        self.sound.stopPlay()
        self.parent.btnPlay.config(text="Play")

    def playBacktrack(self):
        self.sound.simplePlay(self.currentTrack)
        self.parent.btnPlay.config(text="Stop")
        

        
 
