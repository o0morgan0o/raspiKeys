import unittest
from game.utils.midiIO import MidiIO


# class TestMidiIO(unittest.TestCase):

#     def setUp(self):
#         # self.midiIO =MidiIO("Midi Through:Midi Through Port-0 24:0", "Midi Through:Midi Through Port-0 24:0")
#         pass


#     def test_emptyTest(self):
#         self.assertEqual(0, 0)

#     def test_shouldNotRaiseExceptionIfConfigInOrConfigOutIsNotCorrect(self):
#         pass
#         # try:
#         #     self.midiIO = MidiIO("", "")
#         # except Exception as e:
#         #     self.fail("MidiIO('', '') raised an unexpectedException")

#     def test_shouldNotRaiseExceptionIfInputsAreEmptyArray(self):
#         pass
#         # self.midiIO = MidiIO("", "")
#         # self.midiIO.midoInList = []
#         # try:
#         #     self.midiIO.openInput(self.midiIO.midoInList, 0)
#         # except Exception:
#         #     self.fail("openInput([]) raised an Exception unexpectedly")

#     def test_shouldNotRaiseExceptionIfOutputsAreEmptyArray(self):
#         pass
#         # self.midiIO = MidiIO("", "")
#         # self.midiIO.midoOutList = []
#         # try:
#         #     self.midiIO.openOutput(self.midiIO.midoOutList, 0)
#         # except Exception:
#         #     self.fail("openOutput([]) raised an exception unexpectedly")

#     def test_behaviorOfToggleListening(self):
#         self.midiIO = MidiIO("", "")
#         self.midiIO.isListening = False
#         self.midiIO.toggleListening()
#         self.assertEqual(self.midiIO.isListening, True)
#         self.midiIO.toggleListening()
#         self.assertEqual(self.midiIO.isListening, False)
