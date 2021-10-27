from src.game.autoload import Autoload
from src.game.utils.config import updateAudioVolume, updateMidiVolume, getAudioVolume, getMidiVolume


class FooterViewModel:

    def __init__(self, view):
        self.view = view
        self.midiIO = Autoload.get_instance().getMidiInstance()
        self.audioInstance = Autoload.get_instance().getAudioInstance()

        self.initializeAudioSlider()
        self.initializeMidiSlider()

    def initializeAudioSlider(self):
        volume = getAudioVolume()
        self.view.slAudioVolume.set(volume)
        self.audioInstance.setVolume(volume)

    def initializeMidiSlider(self):
        volume = getMidiVolume()
        self.view.slMidiVolume.set(volume)
        self.midiIO.setMidiVolume(volume)

    def updateAudioVolumeCallback(self, event):
        new_value = self.view.slAudioVolume.get()
        updateAudioVolume(new_value)
        self.audioInstance.setVolume(new_value)

    def updateMidiVolumeCallback(self, event):
        new_value = self.view.slMidiVolume.get()
        updateMidiVolume(new_value)
        self.midiIO.setMidiVolume(new_value)
