import unittest
from game.utils.midiChords import MidiChords


class TestMidiChords(unittest.TestCase):

    def setUp(self):
        pass

    def test_emptyTest(self):
        self.asssertEqual(0, 0)

    def test_chordsLengthIsGreaterThan0(self):
        self.midiChords = MidiChords()
        self.assertGreater(self.midiChords.chords, 0)
