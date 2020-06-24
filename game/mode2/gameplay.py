import os
import time
import threading
import random
from threading import Timer
import mido
import simpleaudio as sa
import tkinter as tk
import pygame
import env

from utils.midiIO import MidiIO

from utils.audio import Sound
from autoload import Autoload


class Game:

    def __init__(self, parent,config):
        self.config = config
        self.parent = parent
        self.sound = Autoload().getInstanceAudio()
        self.parent.btnPlay.config(command=self.toggleBacktrack)
        # midi io
        self.midiIO=MidiIO()
        self.midiIO.setCallback(self.handleMIDIInput)

        self.parent.btnRandom.config(command=self.playRandom)
#        self.isPlaying = False

        #for filename in self.tracksMp3:
        #    self.sound.convertToWav(filename)

        # TODO : handle errors if non valid files are loaded
        self.tracksWav = Autoload().getTracksWav()
        self.activeSamples = Autoload().getActiveSamples()
        self.currentTrack = self.activeSamples[0]

        self.showRandomTracks()
        if self.sound.isPlaying == False:
            self.playBacktrack()


    # def destroy(self):
    #     self.sound.unloadAudio()
    #     del self.sound
    #     del self

    def showRandomTracks(self):
            name = os.path.basename(self.activeSamples[0])
            self.parent.randTrack0.config(text=name, command=lambda: self.changeTrack(0), fg=env.COL_SEC)
            name = os.path.basename(self.activeSamples[1])
            self.parent.randTrack1.config(text=name, command=lambda: self.changeTrack(1), fg=env.COL_GREY)
            name = os.path.basename(self.activeSamples[2])
            self.parent.randTrack2.config(text=name, command=lambda: self.changeTrack(2), fg=env.COL_GREY)
            name = os.path.basename(self.activeSamples[3])
            self.parent.randTrack3.config(text=name, command=lambda: self.changeTrack(3), fg=env.COL_GREY)

            self.showCurrentPlayingInLabel()

    def showCurrentPlayingInLabel(self):
        name = os.path.basename(self.currentTrack)
        self.parent.labelCurrent.config(text="Currently Playing:\n"+ name)

    def changeTrack(self, index):
        try :
            self.stopBacktrack()
        except : 
            print( "cant stop track during changeTrack.")

        self.currentTrack = self.activeSamples[index]
        self.playBacktrack()
        self.showCurrentPlayingInLabel()
        self.sound.isPlaying = True
        counter = 0

        self.parent.randTrack0.config(fg=env.COL_GREY)
        self.parent.randTrack1.config(fg=env.COL_GREY)
        self.parent.randTrack2.config(fg=env.COL_GREY)
        self.parent.randTrack3.config(fg=env.COL_GREY)
        if index == 0:
            self.parent.randTrack0.config(fg=env.COL_SEC)
        elif index == 1:
            self.parent.randTrack1.config(fg=env.COL_SEC)
        elif index == 2:
            self.parent.randTrack2.config(fg=env.COL_SEC)
        elif index == 3:
            self.parent.randTrack3.config(fg=env.COL_SEC)

        # for track in self.activeSamples:
            


    def pickRandomSamples(self):
        return  random.sample(self.tracksWav, 4)


    
    def playRandom(self):
        self.activeSamples = self.pickRandomSamples()
        self.showRandomTracks()
        if self.sound.isPlaying == True:
            self.sound.stopPlay()
        
        self.currentTrack = self.activeSamples[0]
        self.parent.randTrack0.config(fg=env.COL_SEC)
        self.showCurrentPlayingInLabel()
        self.sound.isPlaying =False
        self.playBacktrack()
        self.sound.isPlaying= True

    def toggleBacktrack(self):
        if self.sound.isPlaying == True:
            self.sound.isPlaying= False
            self.stopBacktrack()
        else :
            self.sound.isPlaying = True
            self.playBacktrack()

    def stopBacktrack(self):
        self.sound.stopPlay()
        self.parent.btnPlay.config(text="Play")

    def playBacktrack(self):
        self.sound.isPlaying=True
        self.sound.simplePlay(self.currentTrack)
        self.parent.btnPlay.config(text="Stop")
        

        
    def handleMIDIInput(self,msg):
        print("receiving : ", msg.note)
        if msg.type =="note_on" :
            #TODO : make this custimizable
            if msg.note == 21:
                self.playRandom()
        pass


 
