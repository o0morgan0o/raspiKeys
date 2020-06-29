from threading import Timer
import pygame
from autoload import Autoload
import pygame
class Bpm:
    def __init__(self, bpm,callback):
        self.sound = Autoload().getInstanceAudio()
        self.sound.loadTick()
        self.saved_volume = pygame.mixer.music.get_volume()
        print(self.saved_volume)
        pygame.mixer.music.set_volume(1)

        self.bpm=bpm
        self.count=4
        self.delayBetweenBeats=60/float(self.bpm)
        print("delay between notes", self.delayBetweenBeats)
        self.callback = callback

        self.t1 = Timer(self.delayBetweenBeats, lambda: self.playTick())
        self.t2= Timer(2* self.delayBetweenBeats, lambda: self.playTick())
        self.t3 = Timer(3*self.delayBetweenBeats, lambda: self.playTick())
        self.t4 = Timer(4*self.delayBetweenBeats, lambda: self.playLastTick())

        self.t1.start()
        self.t2.start()
        self.t3.start()
        self.t4.start()



    def playTick(self):
        print("TICK")
        self.sound.playTick()


    def playLastTick(self):
        print("TACK - recording...")
        self.sound.playTick()
        self.callback()
        pygame.mixer.music.set_volume(self.saved_volume)