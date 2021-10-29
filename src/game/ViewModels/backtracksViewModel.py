import os
import tkinter

import pygame
from PIL import Image, ImageTk

from src.game import env
from src.game.autoload import Autoload


# from src.game.mode2.recordWithBacktrack import RecordWithBacktrack
# from src.game.utils.canvasThread import MyThreadForBacktrackScreen


class BacktracksViewModel:
    def __init__(self, view: tkinter.Frame):
        self.view = view

        self.midiIO = Autoload.get_instance().getMidiInstance()
        self.midiIO.setCallback(self.handleMIDIInput)
        self.audioInstance = Autoload.get_instance().getAudioInstance()

        self.currentTrack = None
        self.tracksWav = None

        # self.metroBpm=int(self.config["metroBpm"])
        # self.isPlayingMetro=False

        # # CLICK LISTENERS
        # self.parent.btnPlay.config(command=self.toggleBacktrack)
        # self.parent.btnMetro.config(command=self.playMetro)
        # self.parent.btnBpmMinus.config(command=self.decreaseMetroTempo)
        # self.parent.btnBpmPlus.config(command=self.increaseMetroTempo)
        # self.parent.btnRandom.config(command=self.playRandom)
        # self.parent.btnSwitchPage.config(command=self.switchPage)

        # for i in range(0,len(self.parent.wav_buttons)):
        #     button=self.parent.wav_buttons[i]
        #     # we must extract the part with number of tracks to only keep the category
        #     button_text=button['text'].split('\n')[0]
        #     button.config(command=lambda button_text=button_text:self.pickRandomSampleInCategory(button_text))

        # this is a list which regroups all 4 folders (house , jazz ,latin, hiphop)
        # self.tracksWav = self.audioInstance.tracksWav
        #
        # self.parent.btnLick.config(
        #     command=self.showWithOrWithoutBacktrackWindow)
        # self.parent.btnRandom.config(text="", image=self.shuffleImage)

        # recording variables

        # self.recordingBassLick = False
        # self.recordingNotes = False

        # self.recordingCustomChords = False
        # self.recordedNotes = []
        # self.recordedCustomChords = []
        #
        # self.damper = []
        # self.damperActive = False

    # def destroy(self):
    #     self.sound.unloadAudio()
    #     del self.sound
    #     del self

    def onBtnCategoryClick(self, id):
        print(id)

    def playMetro(self, ):
        if self.isPlayingMetro == True:
            self.audioInstance.stopPlay()
            self.parent.btnMetro.config(text="Metro")
            self.isPlayingMetro = False
        else:
            self.audioInstance.playRealMetro(self.metroBpm)
            self.parent.btnMetro.config(text="(" + str(self.metroBpm) + ")")
            self.isPlayingMetro = True

        # we would like to generate 2 bars of  audio file to certain bpm

    def decreaseMetroTempo(self, ):
        minBpm = 10
        self.metroBpm -= 10
        if self.metroBpm <= minBpm:  # 10 is the minimum tempo
            self.metroBpm = minBpm
        self.saveMetroBpm(self.metroBpm)
        self.isPlayingMetro = False
        self.playMetro()

    def increaseMetroTempo(self, ):
        maxBpm = 190
        self.metroBpm += 10
        if self.metroBpm >= maxBpm:  # max tempo
            self.metroBpm = maxBpm
        self.saveMetroBpm(self.metroBpm)
        self.isPlayingMetro = False
        self.playMetro()

    def saveMetroBpm(self, bpm):
        metroBpmFile = open(env.CONFIG_METRO_BPM, 'w')
        metroBpmFile.write(str(bpm))
        metroBpmFile.close()

    def showWithOrWithoutBacktrackWindow(self, ):
        self.cancelThreads()
        try:
            del self.parent.recordWindow
        except Exception as e:
            print(e)
        self.parent.destroy()
        self.destroy()
        self.globalRoot.recordWindow = RecordWithBacktrack(
            self.globalRoot, self.app, )

    def showRandomTracks(self, ):
        self.showCurrentPlayingInLabel()

    def showCurrentPlayingInLabel(self, ):
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
        self.audioInstance.isPlaying = True

    def pickRandomSampleInCategory(self, category):
        print(category)
        self.audioInstance.pickRandomSample(category)
        self.playBacktrack()

    def playRandom(self):
        self.audioInstance.pickRandomSample()
        # TODO should display somewhere the number of files in the category and the index
        self.showRandomTracks()
        if self.audioInstance.isPlaying == True:
            self.audioInstance.stopPlay()

        self.currentTrack = self.audioInstance.activeSample[0]
        self.showCurrentPlayingInLabel()
        self.audioInstance.isPlaying = False
        self.playBacktrack()
        self.audioInstance.isPlaying = True

    def toggleBacktrack(self):
        if pygame.mixer.music.get_busy() == True:
            self.stopBacktrack()
            self.audioInstance.isPlaying = False
        else:
            self.playBacktrack()
            self.audioInstance.isPlaying = True

    def stopBacktrack(self):
        self.audioInstance.stopPlay()
        self.parent.btnPlay.config(image=self.playImage)

    def playBacktrack(self):
        self.audioInstance.simplePlay()
        self.audioInstance.isPlaying = True
        self.parent.btnPlay.config(image=self.pauseImage)
        trackInfo = self.audioInstance.getCurrentTrack()
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
            "thread-canvas", self.parent.canvas, self.audioInstance, self.audioInstance.currentFileLength, self, )
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
