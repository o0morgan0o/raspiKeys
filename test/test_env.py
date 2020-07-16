import unittest
from os import path
from game import env 


class TestEnv(unittest.TestCase):

    def setUp(self):
        self.root_dir = env.ROOT_DIR
        self.program_folder = env.PROGRAM_FOLDER 
        self.user_wav_folder = env.USER_WAV_FOLDER 
        self.user_mp3_folder = env.USER_MP3_FOLDER 
        self.processed_wav_folder = env.PROCESSED_WAV_FOLDER 
        self.metro_tick_file = env.METRO_TICK_FILE
        self.midi_folder = env.MIDI_FOLDER
        self.config_file = env.CONFIG_FILE


    def test_EmptyTest(self):
        self.assertEqual(0,0)

    def test_envPathsExists(self):
        self.assertEqual(path.exists(self.root_dir), True)
        self.assertEqual(path.exists(self.program_folder), True)
        self.assertEqual(path.exists(self.user_wav_folder), True)
        # self.assertEqual(path.exists(self.user_mp3_folder), True)
        self.assertEqual(path.exists(self.processed_wav_folder), True)
        self.assertEqual(path.exists(self.midi_folder), True)
        
    def test_fileExists(self):
        # self.assertEqual(path.exists(self.metro_tick_file), True)
        self.assertEqual(path.exists(self.config_file), True)
        



if __name__=="__main__":
    unittest.main()
