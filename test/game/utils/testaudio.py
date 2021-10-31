import unittest
import os
from src.game.utils.audio import Audio

BASE_PROJECT_FOLDER = os.path.join("D:", os.sep, "code", "raspiKeys")


class TestFindALlBacktracksFolders(unittest.TestCase):
    def test_validFolders(self):
        input_folder = os.path.join(BASE_PROJECT_FOLDER, "test", "game", "utils", "backtracks_test_folder")
        result = Audio.findBacktracksFolders(input_folder)
        self.assertEqual(len(result), 3)

    def test_emptyInputFolder(self):
        input_folder = os.path.join(BASE_PROJECT_FOLDER, "test", "game", "utils", "backtracks_test_folder_empty")
        result = Audio.findBacktracksFolders(input_folder)
        self.assertEqual(len(result), 0)


class TestAllValidAudioFilesInFolder(unittest.TestCase):
    def test_emptyFolder(self):
        base_audio_folder = os.path.join(BASE_PROJECT_FOLDER, "test", "game", "utils", "backtracks_test_folder")
        folder_to_test = "empty_folder"
        folder, wav_paths = Audio.findAllValidAudioFilesInFolder(base_audio_folder, folder_to_test)
        self.assertEqual(folder, folder_to_test)
        self.assertEqual(len(wav_paths), 0)
        self.assertEqual(type(wav_paths), list)

    def test_folder1(self):
        base_audio_folder = os.path.join(BASE_PROJECT_FOLDER, "test", "game", "utils", "backtracks_test_folder")
        folder_to_test = "folder1"
        folder, wav_paths = Audio.findAllValidAudioFilesInFolder(base_audio_folder, folder_to_test)
        self.assertEqual(folder,folder_to_test)
        self.assertEqual(len(wav_paths), 5)
        self.assertEqual(type(wav_paths), list)
