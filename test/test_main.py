import unittest
import tkinter as tk
from main import MainApplication


class TestMain(unittest.TestCase):

    def setUp(self):
        self.root =tk.Tk()
        self.app =MainApplication(self.root,"")


    def test_configIsADictionnary(self):
        self.assertIsInstance(self.app.config, dict)

    def test_configVolumeIsANumberBetween0and100(self):
        self.assertGreaterEqual(self.app.config["volume"], 0)
        self.assertLessEqual(self.app.config["volume"], 100)
    
    def test_configVolumeIsLoadedInSlider(self):
        self.assertEqual(self.app.volumeSlider.get(), self.app.config["volume"])

    def test_configDefaultModeIsANumberBetween0and4(self):
        self.assertGreaterEqual(self.app.config["default_mode"],0)
        self.assertLessEqual(self.app.config["default_mode"],4)

    def test_configDefaultModeIsLoadedInGameFrame(self):
        self.assertEqual(self.app.gameMode, self.app.config["default_mode"])

    def test_highLightMode0ifModeIs0(self):
        self.app.highLightActiveMode(0)
        self.assertEqual(self.app.button1["bg"], "black")
        self.assertEqual(self.app.button1["fg"], "white")
        self.assertEqual(self.app.button2["fg"], "black")
        self.assertEqual(self.app.button3["fg"], "black")
        self.assertEqual(self.app.button4["fg"], "black")



if __name__=="__main__":
    unittest.main()