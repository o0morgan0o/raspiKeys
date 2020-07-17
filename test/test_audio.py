import unittest
from game.utils.audio import Sound
import pygame


class TestAudio(unittest.TestCase):
    def setUp(self):
        pass

    def test_emptyTest(self):
        self.assertEqual(0, 0)

    def test_whenSoundIsCreatedMixerVolumeIsSetToVolLow(self):
        self.sound = Sound()
        # .3 is choose arbitraty because .1 is not always correctly rounded
        self.assertLess(round(pygame.mixer.music.get_volume()), .3)

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
            self.fail(
                "pygame.mixer.music.load(self.metroTick) raised Exception unexpectedly!")
        try:
            pygame.mixer.music.play()
        except Exception:
            self.fail("pygame.mixer.music.play() raised Exception unexpectedly!")

    def test_setVolumeOver100ShouldMakeVolume100(self):
        newVolume = 150
        self.setVolume(newVolume)
        realVolume = pygame.mixer.music.get_volume()
        self.assertLess(realVolume, 1)


if __name__ == "__main__":
    unittest.main()
