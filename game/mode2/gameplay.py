import os
import time
import threading
import random
from threading import Timer
import mido
import simpleaudio as sa
import tkinter as tk
import pygame
import game.env

from game.utils.midiIO import MidiIO
from game.utils.audio import Audio
from game.autoload import Autoload


from game.mode2.recordSetupGui import RecordSetupGui
from game.mode2.recordNotesGui import RecordNotesGui
from game.mode2.recordChordsGui import RecordChordsGui
from game.mode2.recordWithBacktrack import RecordWithBacktrack

from game.utils.canvasThread import MyThread
from game.utils.canvasThread import MyThreadForBacktrackScreen


class Game:
    def __init__(
        self, globalRoot, parent, config, app,
    ):
        self.midiIO = Autoload().getInstance()
        self.midiIO.setCallback(self.handleMIDIInput)
        self.globalRoot = globalRoot
        self.app = app
        self.config = config

        self.parent = parent
        self.sound = Autoload().getInstanceAudio()

        self.parent.btnPlay.config(command=self.toggleBacktrack)
        self.parent.btnRandom.config(command=self.playRandom)
        self.tracksWav = self.sound.tracksWav
        # self.activeSample = self.sound.activeSample[0]
        # self.activeSampleIndex = self.sound.activeSample[1]
        # self.tuple = self.sound.pickRandomSample(self.tracksWav)
        # self.activeSample = self.tuple[0]
        # self.activeSampleIndex=self.tuple[1]

        self.currentTrack = self.sound.activeSample[0]
        self.showRandomTracks()
        self.playBacktrack()

        nbTracksStr = "Random beat:\n{} beats in the base.".format(str(len(self.tracksWav)))
        self.parent.lblStatic1.config(text=nbTracksStr)
        self.parent.btnLick.config(command=self.showWithOrWithoutBacktrackWindow)

        # recording variables

        self.recordingBassLick = False
        self.recordingNotes = False

        self.recordingCustomChords = False
        self.recordedNotes = []
        self.recordedCustomChords = []

    # def destroy(self):
    #     self.sound.unloadAudio()
    #     del self.sound
    #     del self
    def showWithOrWithoutBacktrackWindow(self,):
        self.cancelThreads()
        try:
            del self.parent.recordWindow
        except Exception as e:
            print(e)
        self.parent.destroy()
        self.destroy()
        self.globalRoot.recordWindow = RecordWithBacktrack(self.globalRoot, self.app,)

    def showRandomTracks(self,):
        self.showCurrentPlayingInLabel()

    def showCurrentPlayingInLabel(self,):
        name = os.path.basename(self.currentTrack)
        # self.parent.labelCurrent.config(text="Currently Playing:\n"+ name + "\n" + str(self.sound.getCurrentTrack()[0]) +" sec")

    def changeTrack(self, index):
        try:
            self.stopBacktrack()
        except:
            print("cant stop track during changeTrack.")

        self.currentTrack = self.activeSample[index]
        self.playBacktrack()
        self.showCurrentPlayingInLabel()
        self.sound.isPlaying = True

    # def pickRandomSample(self,):
    #     index = random.randint(0, len(self.tracksWav) - 1,)
    #     self.activeSampleIndex = index
    #     return (
    #         self.tracksWav[index],
    #         index,
    #     )

    def playRandom(self):
        self.sound.pickRandomSample()
        # self.activeSample =
        self.showRandomTracks()
        if self.sound.isPlaying == True:
            self.sound.stopPlay()

        self.currentTrack = self.sound.activeSample[0]
        self.showCurrentPlayingInLabel()
        self.sound.isPlaying = False
        self.playBacktrack()
        self.sound.isPlaying = True

    def toggleBacktrack(self):
        if pygame.mixer.music.get_busy() == True:
            self.stopBacktrack()
            self.sound.isPlaying = False
        else:
            self.playBacktrack()
            self.sound.isPlaying = True

    def stopBacktrack(self):
        self.sound.stopPlay()
        self.parent.btnPlay.config(text="Play")

    def playBacktrack(self):
        self.sound.simplePlay(self.currentTrack)
        self.sound.isPlaying = True
        self.parent.btnPlay.config(text="Stop")
        trackInfo = self.sound.getCurrentTrack()
        trackName = trackInfo[0].split("/")[-1]
        trackLength = "{0:.2f}".format(trackInfo[1])
        self.parent.labelCurrent.config(text="Currently Playing ({} / {}):\n{}\n({} sec length)".format(self.sound.activeSample[1], str(len(self.sound.tracksWav)), trackName, str(trackLength),))
        # thread for canvas
        self.parent.canvas.delete("all")
        try:
            self.thread.isAlive = False  # kill previous thread
        except Exception as e:
            print(e)
        self.thread = MyThreadForBacktrackScreen("thread-canvas", self.parent.canvas, self.sound, self.sound.currentFileLength, self,)
        self.thread.start()

    def cancelThreads(self):
        try:
            self.thread.isAlive = False
        except Exception as e:
            print(e)
        try:
            del self.thread
        except Exception as e:
            print(e)
        pygame.mixer.music.stop()

    def destroy(self):
        print("trying cancel thread")
        self.cancelThreads()
        # pass
        # self.cancelThreads()
        # pygame.mixer.music.stop()
        # try:
        # del self.activeCustomSignals
        # del self.precountTimer
        # except Exception as e:
        #     print("error in destroy :", e)
        # del self

    def handleMIDIInput(self, msg):
        # No handle because we want to ignore the midi input messages
        pass
