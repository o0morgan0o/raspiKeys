import os
import time
import threading
import random
from threading import Timer
import mido
import simpleaudio as sa
import tkinter as tk
import pygame
from game import env
import numpy as np

from PIL import Image, ImageTk
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
        self.currentTrack = None
        self.tracksWav = None

        # images
        self.playImage = ImageTk.PhotoImage(Image.open(env.PLAY_IMAGE))
        self.pauseImage = ImageTk.PhotoImage(Image.open(env.PAUSE_IMAGE))
        self.shuffleImage = ImageTk.PhotoImage(Image.open(env.SHUFFLE_IMAGE))
        self.page=0

        self.midiIO = Autoload().getInstance()
        self.midiIO.setCallback(self.handleMIDIInput)
        self.globalRoot = globalRoot
        self.app = app
        self.config = config
        metroBpmFile = open(env.CONFIG_METRO_BPM, 'r')
        self.metroBpm=int(metroBpmFile.read())
        self.isPlayingMetro=False

        self.parent = parent
        self.sound = Autoload().getInstanceAudio()

        # CLICK LISTENERS
        self.parent.btnPlay.config(command=self.toggleBacktrack)
        self.parent.btnMetro.config(command=self.playMetro)
        self.parent.btnBpmMinus.config(command=self.decreaseMetroTempo)
        self.parent.btnBpmPlus.config(command=self.increaseMetroTempo)
        self.parent.btnRandom.config(command=self.playRandom)
        self.parent.btnSwitchPage.config(command=self.switchPage)


        self.parent.btnHouse.config(
            command=lambda: self.pickRandomSampleInCategory("house"))
        self.parent.btnJazz.config(
            command=lambda: self.pickRandomSampleInCategory("jazz"))
        self.parent.btnLatin.config(
            command=lambda: self.pickRandomSampleInCategory("latin"))
        self.parent.btnHipHop.config(
            command=lambda: self.pickRandomSampleInCategory("hiphop")
            )

        # this is a list which regroups all 4 folders (house , jazz ,latin, hiphop)
        self.tracksWav = self.sound.tracksWav

        self.parent.btnLick.config(
            command=self.showWithOrWithoutBacktrackWindow)
        self.parent.btnRandom.config(text="", image=self.shuffleImage)

        # recording variables

        self.recordingBassLick = False
        self.recordingNotes = False

        self.recordingCustomChords = False
        self.recordedNotes = []
        self.recordedCustomChords = []

        self.damper = []
        self.damperActive = False

    # def destroy(self):
    #     self.sound.unloadAudio()
    #     del self.sound
    #     del self

    def switchPage(self,):
        self.page += 1
        if self.page >= 2:
            self.page=0
        
        if self.page ==0:
            self.parent.btnMetro.place(x=10, y=20)
            self.parent.btnBpmMinus.place(x=130, y=20)
            self.parent.btnBpmPlus.place(x=220, y=20)
            self.parent.btnHouse.place(x=10, y=120)
            self.parent.btnLatin.place(x=170, y=120)
            self.parent.btnJazz.place(x=10, y=220)

            self.parent.btnPlay.place(x=-200)
            self.parent.btnLick.place(x=-200)
            self.parent.btnHipHop.place(x=-200)
        
        elif self.page ==1:
            self.parent.btnPlay.place(x=10,y=20)
            self.parent.btnLick.place(x=170,y=20)
            self.parent.btnHipHop.place(x=10, y=120)

            self.parent.btnMetro.place(x=-200)
            self.parent.btnBpmMinus.place(x=-200)
            self.parent.btnBpmPlus.place(x=-200)
            self.parent.btnHouse.place(x=-200)
            self.parent.btnLatin.place(x=-200)
            self.parent.btnJazz.place(x=-200)

    

    def playMetro(self,):
        if self.isPlayingMetro==True:
            self.sound.stopPlay()
            self.parent.btnMetro.config(text="Metro")
            self.isPlayingMetro =False
        else :
            self.sound.playRealMetro(self.metroBpm)
            self.parent.btnMetro.config(text="("+str(self.metroBpm)+")")
            self.isPlayingMetro=True

        # we would like to generate 2 bars of  audio file to certain bpm
    def decreaseMetroTempo(self,):
        minBpm=10
        self.metroBpm -= 10
        if self.metroBpm <=minBpm: # 10 is the minimum tempo
            self.metroBpm =minBpm
        self.saveMetroBpm(self.metroBpm)
        self.isPlayingMetro=False
        self.playMetro()

    def increaseMetroTempo(self,):
        maxBpm=190
        self.metroBpm +=10
        if self.metroBpm >= maxBpm: # max tempo
            self.metroBpm =maxBpm
        self.saveMetroBpm(self.metroBpm)
        self.isPlayingMetro=False
        self.playMetro()
    
    def saveMetroBpm(self,bpm):
        metroBpmFile = open(env.CONFIG_METRO_BPM, 'w')
        metroBpmFile.write(str(bpm))
        metroBpmFile.close()

    def showWithOrWithoutBacktrackWindow(self,):
        self.cancelThreads()
        try:
            del self.parent.recordWindow
        except Exception as e:
            print(e)
        self.parent.destroy()
        self.destroy()
        self.globalRoot.recordWindow = RecordWithBacktrack(
            self.globalRoot, self.app,)

    def showRandomTracks(self,):
        self.showCurrentPlayingInLabel()

    def showCurrentPlayingInLabel(self,):
        name = os.path.basename(self.currentTrack)
        # self.parent.labelCurrent.config(text="Currently Playing:\n"+ name + "\n" + str(self.sound.getCurrentTrack()[0]) +" sec")

    def changeTrack(self, index):
        try:
            self.stopBacktrack()
        except Exception:
            print("cant stop track during changeTrack.")
        self.currentTrack = self.activeSample[index]
        self.playBacktrack()
        self.showCurrentPlayingInLabel()
        self.sound.isPlaying = True

    def pickRandomSampleInCategory(self, category):
        print(category)
        self.sound.pickRandomSample(category)
        self.playBacktrack()

    def playRandom(self):
        self.sound.pickRandomSample()
        # TODO should display somewhere the number of files in the category and the index
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
        self.parent.btnPlay.config(image=self.playImage)

    def playBacktrack(self):
        self.sound.simplePlay()
        self.sound.isPlaying = True
        self.parent.btnPlay.config(image=self.pauseImage)
        trackInfo = self.sound.getCurrentTrack()
        trackName = trackInfo[0].split("/")[-1]
        trackLength = "{0:.2f}".format(trackInfo[1])
        # self.parent.labelCurrent.config(
        #     text="Currently Playing ({} / {}):\n{}\n({} sec length)".format(
        #         self.sound.activeSample[1], str(
        #             len(self.sound.tracksWav)), trackName, str(trackLength),
        #     )
        # )
        # thread for canvas
        self.parent.canvas.delete("all")
        try:
            self.thread.isAlive = False  # kill previous thread
        except Exception as e:
            print(e)
        self.thread = MyThreadForBacktrackScreen(
            "thread-canvas", self.parent.canvas, self.sound, self.sound.currentFileLength, self,)
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

    def handleMIDIInput(self, msg):
        print(msg)
        # if msg.type == "control_change":
        #     print("pedal ... : ", msg.control, msg.value)
        #     if msg.control == 64 and msg.value > 64:
        #         self.damperActive = True
        #     if msg.control == 64 and msg.value <= 64:
        #         self.damperActive = False
        #         print(self.damper)
        #         self.damper = []

        # if self.damperActive == True and msg.type == "note_off":
        #     self.damper.append(msg.note)

        # # No handle because we want to ignore the midi input messages
        pass
