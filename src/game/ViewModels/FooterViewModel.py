from src.game.autoload import Autoload
from src.game.utils.config import updateAudioVolume, updateMidiVolume, getAudioVolume, getMidiVolume


class FooterViewModel:

    def __init__(self, view):
        self.view = view
        self.midiIO = Autoload.get_instance().getMidiInstance()
        self.audioInstance = Autoload.get_instance().getAudioInstance()

        self.initializeView()

        self.audioIncrement: int = 7
        self.midiIncrement: int = 10

    def initializeView(self):
        audioVolume = getAudioVolume()
        self.audioInstance.setVolume(audioVolume)
        midiVolume = getMidiVolume()
        self.midiIO.setMidiVolume(midiVolume)
        self.view.setUiInitialization(audioVolume, midiVolume)

    def updateAudioVolumeCallback(self, event):
        new_value = self.view.slAudioVolume.get()
        updateAudioVolume(new_value)
        self.audioInstance.setVolume(new_value)

    def updateMidiVolumeCallback(self, event):
        new_value = self.view.slMidiVolume.get()
        updateMidiVolume(new_value)
        self.midiIO.setMidiVolume(new_value)

    def audioPlusClicked(self):
        self.changeAudioVolume(self.audioIncrement)

    def audioMinusClicked(self):
        self.changeAudioVolume(-self.audioIncrement)

    def midiPlusClicked(self):
        self.changeMidiVolume(self.midiIncrement)

    def midiMinusClicked(self):
        self.changeMidiVolume(-self.midiIncrement)

    def changeAudioVolume(self, volume_change: int):
        current_volume = getAudioVolume()
        new_volume = current_volume + volume_change
        if new_volume <= 0:
            new_volume = 0
        elif new_volume >= 99:
            new_volume = 99
        if current_volume != new_volume:
            self.audioInstance.setVolume(new_volume)
            # write to config file the new volume
            updateAudioVolume(new_volume)
            self.view.updateLblAudioVolume(new_volume)

    def changeMidiVolume(self, volume_change: int):
        current_volume = getMidiVolume()
        new_volume = current_volume + volume_change
        if new_volume <= 0:
            new_volume = 0
        elif new_volume >= 127:
            new_volume = 127
        if current_volume != new_volume:
            self.midiIO.setMidiVolume(new_volume)
            # write to config file the new volume
            updateMidiVolume(new_volume)
            self.view.updateLblMidiVolume(new_volume)
