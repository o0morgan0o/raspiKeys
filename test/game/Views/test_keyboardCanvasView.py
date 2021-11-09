import unittest

from src.game.Views.keyboardCanvasView import KeyboardCanvasView


class TestCalculateNumberOfOctavesNeeded(unittest.TestCase):
    def test_calculateOctaveRange0To8(self):
        minNote = 0
        maxNote = 8
        (minOctave, numberOfOctaves) = KeyboardCanvasView.calculateNumberOfOctaveNeeded(minNote, maxNote)
        self.assertEqual(minOctave, 0)
        self.assertEqual(numberOfOctaves, 1)

    def test_calculateOctaveRange2To2(self):
        minNote = 2
        maxNote = 2
        (minOctave, numberOfOctaves) = KeyboardCanvasView.calculateNumberOfOctaveNeeded(minNote, maxNote)
        self.assertEqual(minOctave, 0)
        self.assertEqual(numberOfOctaves, 1)

    def test_calculateOctaveRange2To8(self):
        minNote = 2
        maxNote = 8
        (minOctave, numberOfOctaves) = KeyboardCanvasView.calculateNumberOfOctaveNeeded(minNote, maxNote)
        self.assertEqual(minOctave, 0)
        self.assertEqual(numberOfOctaves, 1)

    def test_calculateOctaveRange2To11(self):
        minNote = 2
        maxNote = 11
        (minOctave, numberOfOctaves) = KeyboardCanvasView.calculateNumberOfOctaveNeeded(minNote, maxNote)
        self.assertEqual(minOctave, 0)
        self.assertEqual(numberOfOctaves, 1)

    def test_calculateOctaveRange2To12(self):
        minNote = 2
        maxNote = 12
        (minOctave, numberOfOctaves) = KeyboardCanvasView.calculateNumberOfOctaveNeeded(minNote, maxNote)
        self.assertEqual(minOctave, 0)
        self.assertEqual(numberOfOctaves, 2)

    def test_calculateOctaveRange12To18(self):
        minNote = 12
        maxNote = 18
        (minOctave, numberOfOctaves) = KeyboardCanvasView.calculateNumberOfOctaveNeeded(minNote, maxNote)
        self.assertEqual(minOctave, 1)
        self.assertEqual(numberOfOctaves, 1)

    def test_calculateOctaveRange2To25(self):
        minNote = 2
        maxNote = 25
        (minOctave, numberOfOctaves) = KeyboardCanvasView.calculateNumberOfOctaveNeeded(minNote, maxNote)
        self.assertEqual(minOctave, 0)
        self.assertEqual(numberOfOctaves, 3)

    def test_calculateOctaveRange43To43(self):
        minNote = 43
        maxNote = 43
        (minOctave, numberOfOctaves) = KeyboardCanvasView.calculateNumberOfOctaveNeeded(minNote, maxNote)
        self.assertEqual(minOctave, 3)
        self.assertEqual(numberOfOctaves, 1)

    def test_calculateOctaveRange0To43(self):
        minNote = 0
        maxNote = 43
        (minOctave, numberOfOctaves) = KeyboardCanvasView.calculateNumberOfOctaveNeeded(minNote, maxNote)
        self.assertEqual(minOctave, 0)
        self.assertEqual(numberOfOctaves, 4)
