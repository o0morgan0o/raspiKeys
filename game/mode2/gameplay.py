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
        # self.midiIO=Autoload().getInstance()
        # self.midiIO.setCallback(self.handleMIDIInput)

        self.parent.btnRandom.config(command=self.playRandom)
#        self.isPlaying = False

        #for filename in self.tracksMp3:
        #    self.sound.convertToWav(filename)

        # TODO : handle errors if non valid files are loaded
        self.tracksWav = Autoload().getTracksWav()
        self.activeSample = Autoload().getActiveSample()
        self.activeSampleIndex = Autoload().getActiveSampleIndex()
        self.currentTrack = self.activeSample


        self.showRandomTracks()
        self.playBacktrack()

        # we want to show the number of tracks
        nbTracksStr = "Random beat:\n{} beats in the base.".format(str(len(self.tracksWav)))
        self.parent.lblStatic1.config(text=nbTracksStr)

    # def destroy(self):
    #     self.sound.unloadAudio()
    #     del self.sound
    #     del self

    def showRandomTracks(self):
            self.showCurrentPlayingInLabel()

    def showCurrentPlayingInLabel(self):
        name = os.path.basename(self.currentTrack)
        # self.parent.labelCurrent.config(text="Currently Playing:\n"+ name + "\n" + str(self.sound.getCurrentTrack()[0]) +" sec") 

    def changeTrack(self, index):
        try :
            self.stopBacktrack()
        except : 
            print( "cant stop track during changeTrack.")

        self.currentTrack = self.activeSample[index]
        self.playBacktrack()
        self.showCurrentPlayingInLabel()
        self.sound.isPlaying = True

    def pickRandomSample(self):
        index = random.randint(0, len(self.tracksWav)-1)
        self.activeSampleIndex = index
        return  (self.tracksWav[index], index)


    
    def playRandom(self):
        self.activeSample = self.pickRandomSample()
        self.showRandomTracks()
        if self.sound.isPlaying == True:
            self.sound.stopPlay()
        
        self.currentTrack = self.activeSample[0]
        self.showCurrentPlayingInLabel()
        self.sound.isPlaying =False
        self.playBacktrack()
        self.sound.isPlaying= True

    def toggleBacktrack(self):
        if pygame.mixer.music.get_busy() == True:
            self.stopBacktrack()
            self.sound.isPlaying= False
        else :
            self.playBacktrack()
            self.sound.isPlaying = True

    def stopBacktrack(self):
        self.sound.stopPlay()
        self.parent.btnPlay.config(text="Play")

    def playBacktrack(self):
        self.sound.simplePlay(self.currentTrack)
        self.sound.isPlaying=True
        self.parent.btnPlay.config(text="Stop")
        trackInfo = self.sound.getCurrentTrack()
        trackName = trackInfo[0].split("/")[-1]
        trackLength = "{0:.2f}".format(trackInfo[1])
        self.parent.labelCurrent.config(text="Currently Playing ({} / {}):\n{}\n({} sec length)".format(
            self.activeSampleIndex,
            str(len(self.tracksWav)),
            trackName, 
            str(trackLength)))
        # while pygame.mixer.music.get_busy():

        # print("launching thread")
        # self.canvasUpdateThread = MyThread(1, "ThreadCanvas", self.parent.canvas, self.sound)
        # self.canvasUpdateThread.start()

        

        