from utils.voice import Voice

class Module:

    """
    Parent class for modules
    """

    def __init__(self, command: str, args: list, voice: Voice, extras) -> None:
        self.command = command
        self.args = args
        self.voice = voice
        self.extras = extras

    def run(self):
        return None