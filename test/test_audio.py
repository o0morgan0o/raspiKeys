# import unittest
# from src.game.utils.audio import Audio
# import os
# from src.game import env
#
#
# class TestAudio(unittest.TestCase):
#     def setUp(self):
#         self.audio = Audio()
#
#     def test_loadBacktracksWavOfEmptyFolder(self):
#         self.audio.processed_waveDir = env.TEST_ROOT_DIR_PROCESSED_EMPTY_FOLDER
#         self.audio.loadBacktracksWav()
#         self.assertEquals(self.audio.tracksWav.house, [])
#         self.assertEquals(self.audio.tracksWav.latin, [])
#         self.assertEquals(self.audio.tracksWav.jazz, [])
#         self.assertEquals(self.audio.tracksWav.hiphop, [])
#
#     def test_loadBacktracksWav_With_One_House_File(self):
#         self.audio.processed_waveDir = env.TEST_ROOT_DIR_PROCESSED_WAV_FOLDER
#         self.audio.loadBacktracksWav()
#         self.assertEquals(len(self.audio.tracksWav.house), 1)
#         self.assertEquals(len(self.audio.tracksWav.latin), 0)
#         self.assertEquals(len(self.audio.tracksWav.jazz), 3)
#         self.assertEquals(len(self.audio.tracksWav.hiphop), 0)
#         self.assertEquals(self.audio.tracksWav.house[0], os.path.join(
#             self.audio.processed_waveDir, "house",  "metro1.wav"))
#
#     def test_pickRandomSample_Of_Non_Existing_Category(self):
#         self.audio.pickRandomSample("non-existing")
#         self.assertEquals(self.audio.activeSample, None)
#
#     def test_pickRandomSample_Of_ExistingCategory(self):
#         self.audio.processed_waveDir = env.TEST_ROOT_DIR_PROCESSED_WAV_FOLDER
#         self.audio.loadBacktracksWav()
#         self.audio.pickRandomSample("jazz")
#         self.assertNotEqual(self.audio.activeSample, None)
#         self.assertEqual(
#             self.audio.activeSample[0] in self.audio.tracksWav.jazz, True)
#         self.assertGreaterEqual(self.audio.activeSample[1], 0)
#         self.assertLessEqual(
#             self.audio.activeSample[1], len(self.audio.tracksWav.jazz))
#
#     def tearDown(self):
#         del self.audio
