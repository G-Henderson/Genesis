from utils.voice import Voice
from random import randint

class Module:

    def __init__(self, command: str, args: list, voice_instance: Voice, extras) -> None:
        # Initialise variables from the arguments
        self.command = command
        self.args = args
        self.voice = voice_instance
        self.extras = extras

    def get_joke(self) -> str:
        # Read in the jokes array from the json file

        # Generate a random number from the list of indexs

        # Get the jokes at that index

        # Return the question and punch line
        return "", ""

    def run(self) -> None:
        # Get a random joke
        my_q, my_a = self.get_joke()

        # Ask the question
        self.voice.say(my_q)
        
        # Pause

        # Say the punch line
        self.voice.say(my_a)

        return None