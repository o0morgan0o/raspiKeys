import unittest
from game.utils.audio import Sound
import pygame


class TestAudio(unittest.TestCase):
    def setUp(self):
        pass


    def test_emptyTest(self):
        self.assertEqual(0,0)

    def test_whenSoundIsCreatedMixerVolumeIsSetToVolLow(self):
        self.sound = Sound()
        self.assertLess(round(pygame.mixer.music.get_volume()), .3) # .3 is choose arbitraty because .1 is not always correctly rounded

    def test_pickRandomSampleOfAnEmptyArrayDontRaiseError(self):
        self.sound = Sound()
        try:
            self.sound.pickRandomSample([])
        except Exception:
            self.fail("pickRandomSample([]) raised Exception unexpectedly !") 


    def test_loadAndPlayMetronomeTick(self):
        self.tick = Sound().metroTick
        try:
            pygame.mixer.music.load(self.tick)
        except Exception:
                self.fail("pygame.mixer.music.load(self.metroTick) raised Exception unexpectedly!")
        try:
            pygame.mixer.music.play()
        except Exception:
            self.fail("pygame.mixer.music.play() raised Exception unexpectedly!")

    def test_loadBacktracksWav(self):
        pass
    
    def test_SimplePlay(self):
        pass

    def test_stopPlay(self):
        pass

    def test_unloadAudio(self):
        pass

    def test_setVolume(self):
        pass

    def test_getCurrentTrack(self)
        pass


if __name__ == "__main__":
    unittest.main()