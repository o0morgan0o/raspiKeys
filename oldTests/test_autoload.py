
import unittest
from game.autoload import Autoload
from game.utils.audio import Audio

class TestAutoload(unittest.TestCase):

    def setUp(self):
        self.autoload = None

    def test_emptyTest(self):
        self.assertEqual(0,0)


    def test_creationOfMidiInstanceIsNotNone(self):
        self.assertIsNone(self.autoload)
        self.autoload = Autoload().getInstance()
        self.assertIsNotNone(self.autoload)


    def test_creationOfAudioInstanceIsNotNote(self):
        self.assertIsNone(self.autoload)
        self.autoload = Autoload().getInstanceAudio()
        self.assertIsNotNone(self.autoload)

    def test_getAudioInstanceReturnASound(self):
        self.instance=Autoload().getInstanceAudio()
        self.assertIsInstance(self.instance, Audio)

    def test_getActiveSampleIsNotAnEmptyString(self):
        self.activeSample = Autoload().getActiveSample()
        self.assertIsInstance(self.activeSample, str)
        self.assertNotEqual(self.activeSample, "")

    def test_getActiveSampleIndexIsAnInt(self):
        self.activeSampleIndex = Autoload().getActiveSampleIndex()
        self.assertIsInstance(self.activeSampleIndex, int)

    def test_getTracksWavIsAList(self):
        self.tracks = Autoload().getTracksWav()
        self.assertIsInstance(self.tracks, list)

    


if __name__ == "__main__":
    unittest.main()