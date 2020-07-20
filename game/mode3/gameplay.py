import datetime
import random
import pygame
from game.utils.bpm import Bpm
from threading import Timer
import threading
import random
import os
from game import env
import time
import tkinter as tk
from tkinter import messagebox
import json
from tkinter import ttk as ttk
import mido

from PIL import Image, ImageTk

from game.utils.midiIO import MidiIO
from game.autoload import Autoload
from game.utils.questionNote import CustomSignal
from game.utils.midiToNotenames import noteName
from game.utils.utilFunctions import getChordInterval
from game.utils.utilFunctions import formatOutputInterval

from game.utils.customElements.buttons import *
from game.utils.customElements.labels import *


class Game:
    def __init__(self, globalRoot, root, config, app):
        # images
        self.playImage = ImageTk.PhotoImage(Image.open(env.PLAY_IMAGE))
        self.pauseImage = ImageTk.PhotoImage(Image.open(env.PAUSE_IMAGE))
        self.shuffleImage = ImageTk.PhotoImage(Image.open(env.SHUFFLE_IMAGE))

        self.midiIO = Autoload().getInstance()
        self.midiIO.setCallback(self.handleMIDIInput)

        self.isPlaying = False
        self.config = config
        self.globalRoot = globalRoot
        self.root = root
        self.app = app

        # Default path
        self.midiRepository = env.MIDI_FOLDER

        # Callbacks for buttons
        # self.root.btnRecord.config(command=self.showWithOrWithoutBacktrackWindow)
        self.root.btnPractiseLick.config(image=self.playImage, command=self.playOneLick)
        self.root.btnRandomLick.config(image=self.shuffleImage, command=self.pickRandomLick)
        self.root.btnDeleteSelected.config(command=self.deleteLick)
        self.root.btnPrev.config(command=self.previousLick)
        self.root.btnNext.config(command=self.nextLick)

        self.midiFiles = []
        self.reloadMidiFiles()
        self.fileIndex = 0
        self.recordNotes = None

        self.midiIO = Autoload().getInstance()
        self.audioInstance = Autoload().getInstanceAudio()
        # self.midiIO.setCallback(self.handleMIDIInput)

        self.bassNote = 0
        self.chordQuality = "-"
        self.transpose = 0
        self.activeCustomSignals = []
        self.lickRepetitionCounter = 1
        self.lickMaxRepetition = self.config["times_each_transpose"]
        self.playOnlyChord = False

        self.currentLickIndex = 0
        self.currentLick = None

        self.practiseAllLicks = False
        self.lastTranspose = 0
        self.futureTranspose = 0

        self.playBacktrackThread = None
        self.audioThread = None

        self.bass = None
        self.mType = None
        self.notes = None
        self.backtrackVolume = None

        self.loadASample(len(self.midiFiles) - 1)

        # we need the number of licks in order to show the user

    def loadASample(self, index):
        nbOfSamples = len(self.midiFiles)
        if nbOfSamples == 0:
            self.root.lblNotes.config(text="No lick, record one first !")
        else:
            # we load last sample
            self.currentLickIndex = index
            self.loadSelectedItem(self.midiFiles[self.currentLickIndex])
            self.root.lblMessage.config(text="Lick {} / {} loaded.".format(index + 1, len(self.midiFiles)))
            self.showUserInfo(0)

    def reloadMidiFiles(self):
        counter = 0
        midiFiles = []
        for filename in os.listdir(self.midiRepository):
            # get only json files
            if os.path.splitext(filename)[1] == ".json":
                mFile = os.path.join(self.midiRepository, filename)
                midiFiles.append(mFile)
                counter += 1

        self.midiFiles = midiFiles
        self.midiFiles.sort()
        print("Reloading all MIDI files...", len(self.midiFiles))

    def loadSelectedItem(self, name):
        self.loadFile(os.path.join(self.midiRepository, name))

    def showUserInfo(self, transpose, counter=-1, nbBeforeTranspose=-1):
        self.userMessage = ""
        for note in self.notes:
            # print(note)
            if note["type"] == "note_on":
                if len(self.userMessage) > 30:
                    self.userMessage = self.userMessage[:28] + "..."
                else:
                    self.userMessage += noteName(note["note"] + transpose) + " "
        self.root.lblKey.config(foreground="white")
        self.root.lblKey.config(text="{} {}".format(noteName(self.bass + transpose), self.mType))
        self.root.lblNotes.config(foreground="white")
        self.root.lblNotes.config(text=self.userMessage)
        self.root.lblMessage.config(text="Lick {} / {} loaded.".format(self.currentLickIndex + 1, len(self.midiFiles)))
        if counter != -1:
            self.root.lblFollowing.config(
                text="{} / {} before transpose...".format(str(counter), str(nbBeforeTranspose)), foreground="white"
            )
        else:
            self.root.lblFollowing.config(text="")

    def showUserInfoNextTranspose(self, oldTranspose, newTranspose):
        beforeKey = noteName(self.bass + oldTranspose)
        afterKey = noteName(self.bass + newTranspose)
        self.root.lblKey.config(foreground="orange", text="{}=>{}".format(beforeKey, afterKey + self.mType))
        self.root.lblNotes.config(foreground="orange", text=formatOutputInterval(newTranspose - oldTranspose))
        self.root.lblFollowing.config(foreground="orange", text="Transpose next loop...")

    def loadFile(self, mFile):
        try:
            with open(mFile, "r") as f:
                datastore = json.load(f)
                self.currentLick = mFile
                self.bass = datastore["bass"]
                self.notes = datastore["notes"]
                self.mType = datastore["type"]
                self.backtrackVolume = datastore["volumeBacktrack"]
                self.showUserInfo(0)
        except Exception as e:
            print("problem loading file :", mFile, e)

    # def showWithOrWithoutBacktrackWindow(self):
    #     self.cancelThreads()
    #     try :
    #         del self.globalRoot.recordWindow
    #     except Exception as e:
    #         print(e)
    #     self.root.destroy()
    #     self.destroy()
    #     self.globalRoot.recordWindow= RecordWithBacktrack(self.globalRoot, self.app)

    def playChords(self, transpose):
        # notes_on_timing =[]
        # notes_on_notes=[]
        # notes_on_velocity=[]
        # notes_off_timing=[]
        # notes_off_notes=[]
        # for note in self.chord_notes:
        #     if note["type"] == "note_on":
        #         notes_on_timing.append(note["time"])
        #         notes_on_notes.append(note["note"]+transpose)
        #         notes_on_velocity.append(note["velocity"])
        #     elif note["type"]== "note_off":
        #         notes_off_timing.append(note["time"])
        #         notes_off_notes.append(note["note"]+transpose)
        # print(notes_on_timing)
        # print(notes_on_notes)

        # self.playingThread= TestThread(self,notes_on_timing, notes_on_notes, notes_on_velocity, notes_off_timing, notes_off_notes)
        self.playingThreadChord = TestThread(self, self.chord_notes, transpose)
        self.playingThreadChord.start()

        # for note in self.chord_notes:
        #     self.activeCustomSignals.append(CustomSignal(
        #         self,
        #         note["type"],
        #         note["note"] + transpose,
        #         note["velocity"],
        #         note["time"]
        #     ))

    def playMelody(self, transpose):
        # for note in self.melodyNotes:
        #     self.activeCustomSignals.append(CustomSignal(
        #         self,
        #         note["type"],
        #         note["note"] + transpose,
        #         note["velocity"],
        #         note["time"]
        #     ))
        self.playingThreadMelody = TestThread(self, self.melodyNotes, transpose)
        self.playingThreadMelody.start()

    def activateAudioThread(self, completeTraining):
        # self.cancelThreads()
        with open(self.currentLick, "r") as jsonfile:
            jsonLick = json.load(jsonfile)
        self.key = jsonLick["bass"]
        self.mType = jsonLick["type"]
        self.melodyNotes = jsonLick["notes"]
        self.chord_notes = jsonLick["chord_notes"]
        self.nbOfLoops = jsonLick["nbOfLoops"]
        self.backtrack = jsonLick["backtrack"]
        self.duration = jsonLick["backtrackDuration"] * self.nbOfLoops

        print("Current file has nb of notes :" + str(len(self.melodyNotes) + len(self.chord_notes)))

        self.audioThread = BackTrackThread(self, self.backtrack, self.nbOfLoops, completeTraining)
        self.audioThread.start()

    def previousLick(self):
        self.cancelThreads()
        pygame.mixer.music.stop()
        self.currentLickIndex += -1
        if self.currentLickIndex < 0:
            self.currentLickIndex = len(self.midiFiles) - 1
        self.loadFile(self.midiFiles[self.currentLickIndex])
        self.showUserInfo(0)

    def nextLick(self):
        self.cancelThreads()
        pygame.mixer.music.stop()
        self.currentLickIndex += 1
        if self.currentLickIndex >= len(self.midiFiles):
            self.currentLickIndex = 0
        self.loadFile(self.midiFiles[self.currentLickIndex])
        self.showUserInfo(0)

    def playOneLick(self, completeTraining=False):
        if self.isPlaying == False:
            self.root.btnPractiseLick.config(image=self.pauseImage)
            self.isPlaying = True
            self.activateAudioThread(completeTraining)
        else:
            self.root.btnPractiseLick.config(image=self.playImage)
            self.audioThread.isAlive = False
            # del self.audioThread
            self.isPlaying = False
            self.cancelThreads()
            return

    def pickRandomLick(self):
        # load a new random sample
        self.loadASample(random.randint(0, len(self.midiFiles) - 1))
        self.playOneLick(completeTraining=True)

    def deleteLick(self):
        self.cancelThreads()
        pygame.mixer.music.stop()
        if messagebox.askokcancel("delete ?", message="are you sure you want to delete the current Lick ?") == True:
            try:
                print("-->try to delete lick :", self.currentLick)
                os.remove(self.currentLick)
                self.reloadMidiFiles()
                self.currentLickIndex = 0
                if len(self.midiFiles) > 0:
                    self.currentLick = self.midiFiles[self.currentLickIndex]
                    self.loadSelectedItem(self.currentLick)
                else:
                    self.root.lblNotes.config(text="No lick, record one first !")
                    self.root.lblKey.config(text="")
                    self.root.lblFollowing.config(text="")
                    self.root.lblMessage.config(text="")
            except Exception as e:
                print("Error trying to delete lick", self.currentLick, e)
            self.reloadMidiFiles()

    def cancelThreads(self):
        try:
            self.root.btnPractiseLick.config(text="Practise Lick")
        except:
            print("can't update screen")
        self.isPlaying = False
        try:
            self.audioThread.isAlive = False
        except Exception as e:
            print("no threads to cancel", e)
        # we try to kill all notes no already played
        try:
            self.playingThreadChord.isAlive = False
        except Exception as e:
            print("no threads to cancel", e)
        try:
            self.playingThreadMelody.isAlive = False
        except Exception as e:
            print("no threads to cancel", e)
        for signal in self.activeCustomSignals:
            signal.timer.cancel()
        del self.activeCustomSignals
        self.activeCustomSignals = []
        self.midiIO.panic()

    def destroy(self):
        self.cancelThreads()
        pygame.mixer.music.stop()
        try:
            del self.activeCustomSignals
            del self.precountTimer
        except Exception as e:
            print("error in destroy :", e)
        del self

    def handleMIDIInput(self, msg):
        pass


class BackTrackThread(threading.Thread):
    def __init__(self, parent, backtrack, nbOfLoops, completeTraining):
        self.parent = parent
        threading.Thread.__init__(self)
        self.backtrack = backtrack
        self.isAlive = True
        self.nbOfLoops = nbOfLoops
        pygame.mixer.music.stop()
        pygame.event.clear()
        self.MUSIC_END = pygame.USEREVENT + 1
        pygame.mixer.music.set_endevent(self.MUSIC_END)
        pygame.mixer.music.load(self.backtrack)
        pygame.mixer.music.set_volume(self.parent.backtrackVolume * 100)
        pygame.mixer.music.play(loops=self.nbOfLoops)

        self.transpose = 0
        self.newTranspose = -99
        self.prepareChordArray()
        self.prepareMelodyArray()
        self.time0 = int(round(time.time() * 1000))

        self.counter = 0
        print("Initialisation AUDIO THREAD")
        self.nbBeforeTranspose = 4
        self.parent.showUserInfo(self.transpose, self.counter + 1, self.nbBeforeTranspose)

    def run(self):
        print("Running thread...")

        while self.isAlive == True:

            for event in pygame.event.get():
                print(event.type)
                if event.type == self.MUSIC_END:
                    if self.newTranspose != -99:
                        self.transpose = self.newTranspose
                        self.newTranspose = -99

                    self.ChordIndexNoteOn = 0
                    self.ChordIndexNoteOff = 0
                    self.MelodyIndexNoteOn = 0
                    self.MelodyIndexNoteOff = 0
                    self.time0 = int(round(time.time() * 1000))
                    # if pygame.mixer.music.get_busy() == False: # means it is not playing => reload a new loop
                    # self.parent.playingThreadChord.reset()
                    self.counter += 1
                    self.parent.showUserInfo(self.transpose, self.counter + 1, self.nbBeforeTranspose)
                    print("Relaunching backtrack loop ", self.counter, self.transpose)
                    pygame.mixer.music.play(self.nbOfLoops)
                    # self.parent.replayLick()
                    # self.parent.playChords(self.transpose)
                    # if self.counter % 2 == 0: # play melody one time on 2
                    # self.parent.playMelody(self.transpose)

                    if self.counter == self.nbBeforeTranspose - 1:
                        self.newTranspose = random.randint(-7, 6)
                        print("Transposing next loop ...", self.transpose)
                        self.parent.showUserInfoNextTranspose(self.transpose, self.newTranspose)
                        # self.transpose = newTranspose
                        self.counter = -1

            timeT = int(round(time.time() * 1000)) - self.time0
            if self.counter == 0:
                self.checkMelody(timeT, self.transpose)
            self.checkChords(timeT, self.transpose)

        # def playMelody(self):

        pygame.mixer.music.stop()

    def checkChords(self, timeT, transpose):
        if self.ChordIndexNoteOn <= len(self.ChordNoteOnTiming) - 1:
            if timeT >= self.ChordNoteOnTiming[self.ChordIndexNoteOn]:
                noteToPlay = self.ChordNoteOnNotes[self.ChordIndexNoteOn]
                velocity = self.ChordNoteOnVelocity[self.ChordIndexNoteOn]
                # print("note on", noteToPlay, velocity)
                # t1 = time.time()
                self.parent.midiIO.sendOut("note_on", noteToPlay + transpose, velocity)
                # t2 = time.time()
                # print("time loosed: ", t2 - t1)
                self.ChordIndexNoteOn += 1
        if self.ChordIndexNoteOff <= len(self.ChordNoteOffTiming) - 1:
            if timeT >= self.ChordNoteOffTiming[self.ChordIndexNoteOff]:
                noteToEnd = self.ChordNoteOffNotes[self.ChordIndexNoteOff]
                self.parent.midiIO.sendOut("note_off", noteToEnd + transpose)
                self.ChordIndexNoteOff += 1

    def checkMelody(self, timeT, transpose):
        if self.MelodyIndexNoteOn <= len(self.MelodyNoteOnTiming) - 1:
            if timeT >= self.MelodyNoteOnTiming[self.MelodyIndexNoteOn]:
                noteToPlay = self.MelodyNoteOnNotes[self.MelodyIndexNoteOn]
                velocity = self.MelodyNoteOnVelocity[self.MelodyIndexNoteOn]
                # print("note on", noteToPlay, velocity)
                # t1 = time.time()
                self.parent.midiIO.sendOut("note_on", noteToPlay + transpose, velocity)
                # t2 = time.time()
                # print("time loosed: ", t2 - t1)
                self.MelodyIndexNoteOn += 1
        if self.MelodyIndexNoteOff <= len(self.MelodyNoteOffTiming) - 1:
            if timeT >= self.MelodyNoteOffTiming[self.MelodyIndexNoteOff]:
                noteToEnd = self.MelodyNoteOffNotes[self.MelodyIndexNoteOff]
                self.parent.midiIO.sendOut("note_off", noteToEnd + transpose)
                self.MelodyIndexNoteOff += 1

    def prepareChordArray(self):
        self.ChordNotes = self.parent.chord_notes
        self.ChordNoteOnTiming = []
        self.ChordNoteOnNotes = []
        self.ChordNoteOnVelocity = []
        self.ChordNoteOffTiming = []
        self.ChordNoteOffNotes = []
        for note in self.ChordNotes:
            if note["type"] == "note_on":
                self.ChordNoteOnTiming.append(note["time"])
                self.ChordNoteOnNotes.append(note["note"])
                self.ChordNoteOnVelocity.append(note["velocity"])
            elif note["type"] == "note_off":
                self.ChordNoteOffTiming.append(note["time"])
                self.ChordNoteOffNotes.append(note["note"])
        print(self.ChordNoteOnTiming)
        print(self.ChordNoteOnNotes)
        self.ChordIndexNoteOn = 0
        self.ChordIndexNoteOff = 0

    def prepareMelodyArray(self):
        self.MelodyNotes = self.parent.melodyNotes
        self.MelodyNoteOnTiming = []
        self.MelodyNoteOnNotes = []
        self.MelodyNoteOnVelocity = []
        self.MelodyNoteOffTiming = []
        self.MelodyNoteOffNotes = []
        for note in self.MelodyNotes:
            if note["type"] == "note_on":
                self.MelodyNoteOnTiming.append(note["time"])
                self.MelodyNoteOnNotes.append(note["note"])
                self.MelodyNoteOnVelocity.append(note["velocity"])
            elif note["type"] == "note_off":
                self.MelodyNoteOffTiming.append(note["time"])
                self.MelodyNoteOffNotes.append(note["note"])
        print(self.MelodyNoteOnTiming)
        print(self.MelodyNoteOnNotes)
        self.MelodyIndexNoteOn = 0
        self.MelodyIndexNoteOff = 0

