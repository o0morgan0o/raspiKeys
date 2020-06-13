import simpleaudio as sa

class Sound:
    def __init__(self):
        pass

    def loadEffectSounds(self):
        # success sound
        success_sound = "/home/pi/raspiKeys/gui/games/res/wav/success.wav"
        self.success_sound = sa.WaveObject.from_wave_file(success_sound)
        # error sound
        error_sound = "/home/pi/raspiKeys/gui/games/res/wav/error.wav"
        self.error_sound= sa.WaveObject.from_wave_file(error_sound)

    # TODO: make a try excerpt because may be the sound could not be loaded
    def play_sound_success(self):
        sound_object = self.success_sound.play()
        sound_object.wait_done()

    def play_sound_error(self):
        sound_object = self.error_sound.play()
        sound_object.wait_done()



