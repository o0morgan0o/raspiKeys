from threading import Timer
import pygame
from game.autoload import Autoload

class Bpm:
    def __init__(self, bpm, backtrack, backtrackDuration, nbOfLoops,callback):
        self.sound = Autoload().getInstanceAudio()
        self.sound.loadTick()
        self.backtrack = backtrack
        self.backtrackDuration=backtrackDuration
        self.nbOfLoops= nbOfLoops
        # self.saved_volume = pygame.mixer.music.get_volume()
        # print(self.saved_volume)
        # pygame.mixer.music.set_volume(1)

        self.bpm=bpm
        self.count=4
        self.delayBetweenBeats=60/float(self.bpm)
        print("delay between notes", self.delayBetweenBeats)
        self.callback = callback

        self.t1 = Timer(self.delayBetweenBeats, lambda: self.playFirstTick())
        self.t2= Timer(2* self.delayBetweenBeats, lambda: self.playTick())
        self.t3 = Timer(3*self.delayBetweenBeats, lambda: self.playTick())
        self.t4 = Timer(4*self.delayBetweenBeats, lambda: self.playLastTick())

        self.t1.start()
        self.t2.start()
        self.t3.start()
        self.t4.start()

    def playFirstTick(self):
        print("First TICK")
        self.sound.playTick()

    def playTick(self):
        print("TICK")
        self.sound.playTick()


    def playLastTick(self):
        print("TACK - recording...")
        # self.sound.playTick()
        self.sound.prepareBacktrackForRecord(self.backtrack)
        self.sound.playBacktrackForRecord(self.nbOfLoops)
        self.callback()
        # pygame.mixer.music.set_volume(self.saved_volume)
    
    def cancel(self):
        try:
            self.t4.cancel()
        except Exception as e:
            print(e)
        try:
            self.t3.cancel()
        except Exception as e:
            print(e)
        try:
            self.t2.cancel()
        except Exception as e:
            print(e)
        try:
            self.t1.cancel()
        except Exception as e:
            print(e)