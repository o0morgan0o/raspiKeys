import unittest
from game.utils.audio import Audio
import os
from game import env


class TestAudio(unittest.TestCase):
    def setUp(self):
        self.audio = Audio()

    def test_loadBacktracksWavOfEmptyFolder(self):
        self.audio.processed_waveDir = env.TEST_ROOT_DIR_PROCESSED_EMPTY_FOLDER
        self.audio.loadBacktracksWav()
        self.assertEquals(self.audio.tracksWav.metro, [])
        self.assertEquals(self.audio.tracksWav.latin, [])
        self.assertEquals(self.audio.tracksWav.jazz, [])
        self.assertEquals(self.audio.tracksWav.hiphop, [])

    def test_loadBacktracksWav_With_One_Metro_File(self):
        self.audio.processed_waveDir = env.TEST_ROOT_DIR_PROCESSED_WAV_FOLDER
        self.audio.loadBacktracksWav()
        self.assertEquals(len(self.audio.tracksWav.metro), 1)
        self.assertEquals(len(self.audio.tracksWav.latin), 0)
        self.assertEquals(len(self.audio.tracksWav.jazz), 0)
        self.assertEquals(len(self.audio.tracksWav.hiphop), 0)
        self.assertEquals(self.audio.tracksWav.metro[0], os.path.join(
            self.audio.processed_waveDir, "metro1.wav"))

    def tearDown(self):
        del self.audio
