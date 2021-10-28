import unittest
from src.game.utils.config import *


class TestConfig(unittest.TestCase):

    def test_blankTest(self):
        self.assertEqual(True, True)

    def test_loadEmptyConfigFile(self):
        test_config = None
        config = loadConfigFromFile(test_config)
        self.assertIsNotNone(config)

    def test_loadConfigFromFile(self):
        test_config = {ConfigurationFields.DEFAULT_MODE.value: 0}
        config = loadConfigFromFile(test_config)
        self.assertIsNotNone(config)
        self.assertEqual(config[ConfigurationFields.EAR_TRAINING_NOTE_QUESTION_DELAY.value], 50)
