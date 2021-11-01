from src.game.autoload import Autoload


class NavbarViewModel:
    def __init__(self, view):
        self.view = view
        self.audioInstance = Autoload.get_instance().getAudioInstance()
        self.app = None
