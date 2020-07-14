import unittest
import tkinter as tk
from main import MainApplication


class TestMain(unittest.TestCase):

    def setUp(self):
        self.root =tk.Tk()
        self.app =MainApplication(self.root,"")


    def test_configIsNotEmpty(self):
        self.assertIsInstance(self.app.config, dict)




if __name__=="__main__":
    unittest.main()