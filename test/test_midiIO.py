import unittest
from game.utils.midiIO import MidiIO


class TestMidiIO(unittest.TestCase):

    def setUp(self):
        self.midiIO = MidiIO("", "")

    def test_emptyTest(self):
        self.assertEqual(0, 0)

    def test_shouldNotRaiseExceptionIfConfigInOrConfigOutIsNotCorrect(self):
        try:
            self.midiIO = MidiIO("", "")
        except Exception:
            self.fail("MidiIO('', '') raised an unexpectedException")

    def test_shouldNotRaiseExceptionIfInputsAreEmptyArray(self):
        self.midiIO.midoInList = []
        try:
            self.midiIO.openInput(self.midiIO.midoInList, 0)
        except Exception:
            self.fail("openInput([]) raised an Exception unexpectedly")

    def test_shouldNotRaiseExceptionIfOutputsAreEmptyArray(self):
        self.midiIO.midoOutList = []
        try:
            self.midiIO.openOutput(self.midiIO.midoOutList, 0)
        except Exception:
            self.fail("openOutput([]) raised an exception unexpectedly")

    def test_behaviorOfToggleListening(self):
        self.midiIO.isListening = False
        self.midiIO.toggleListening()
        self.assertEqual(self.midiIO.isListening, True)
        self.midiIO.toggleListening()
        self.assertEqual(self.midiIO.isListening, False)
