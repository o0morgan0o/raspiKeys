import unittest

from src.game.utils.config import *

class TestLoadConfig(unittest.TestCase):

    def test_loadConfig(self):
        config = loadConfig()
        self.assertIsNotNone(config)
        loadConfig().load
