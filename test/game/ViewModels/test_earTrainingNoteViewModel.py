import tkinter as tk
import unittest
from src.game.ViewModels.earTrainingNoteViewModel import *


class TestEarTrainingViewModel(unittest.TestCase):
    pass


class TestPickNewNote(unittest.TestCase):

    def test_minorThirdInterval(self):
        starting_note = 34
        interval = 4
        result = EarTrainingNoteViewModel.getNewQuestionNote(starting_note, interval)
        self.assertNotEqual(result, starting_note)
        self.assertTrue(starting_note - interval <= result <= starting_note + interval)
        self.assertEqual(type(result), int)

    def test_maxIntervalIsZero(self):
        starting_note = 34
        interval = 0
        result = EarTrainingNoteViewModel.getNewQuestionNote(starting_note, interval)
        self.assertEqual(result, starting_note)
        self.assertEqual(type(result), int)

    def test_startingNoteIsZero(self):
        starting_note = 0
        interval = 10
        result = EarTrainingNoteViewModel.getNewQuestionNote(starting_note, interval)
        self.assertGreaterEqual(result, 0)

    def test_startingNoteIsHundredTwentySeven(self):
        starting_note = 127
        interval = 10
        result = EarTrainingNoteViewModel.getNewQuestionNote(starting_note, interval)
        self.assertLessEqual(result, 127)
