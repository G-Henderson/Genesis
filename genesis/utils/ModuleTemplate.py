from utils.voice import Voice


class Module:

    """
    Template for creating new modules
    """

    def __init__(self, command: str, args: list, voice_instance: Voice, extras) -> None:
        # Initialise variables from the arguments
        self.command = command
        self.args = args
        self.voice = voice_instance
        self.extras = extras

    def run(self) -> None:
        # Do stuff here...

        return None