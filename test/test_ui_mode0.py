import unittest
import tkinter as tk
from main import MainApplication
from game.utils.questionNote import QuestionNote
import mido


class TestUIMode0(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.app = MainApplication(self.root, "")
        self.app.new_window(0)
        self.gui = self.app.app
        self.gameplay = self.gui.game

    def test_emptyTest(self):
        self.assertEqual(0, 0)

    def test_configIsAList(self):
        # print("AAAAAAAAAAAAAAA", type(self.gameplay.config))
        self.assertIsInstance(self.gameplay.config, dict)

    def test_startStateIsWaitingUserInput(self):
        self.assertEqual(self.gameplay.gameState, "waitingUserInput")

    def test_afterPlayNoteGameStateIsListenAndStartingNoteIsSet(self):
        self.assertEqual(self.gameplay.gameState, "waitingUserInput")
        mNote = mido.Message('note_on', note=60)
        self.gameplay.handleMIDIInput(mNote)
        self.assertEqual(self.gameplay.gameState, "listen")
        self.assertEqual(self.gameplay.startingNote, 60)
        self.assertIsInstance(self.gameplay.questionNote, QuestionNote)

    def tearDown(self):
        pass


if __name__ == "__main__":
    unittest.main()
