from utils.voice import Voice
from random import randint
import json

class Module:

    def __init__(self, command: str, args: list, voice_instance: Voice, extras) -> None:
        # Initialise variables from the arguments
        self.command = command
        self.args = args
        self.voice = voice_instance
        self.extras = extras

    def get_joke(self) -> str:
        # Read in the jokes array from the json file
        my_file = open('jokes.json')
        data = json.load(my_file)
        jokes_array = data["jokes"]

        # Generate a random number from the list of indexs
        my_index = randint(0,len(jokes_array)-1)

        # Get the joke at that index
        my_joke = jokes_array[my_index]

        # Return the question and punch line
        return my_joke["question"], my_joke["answer"]

    def run(self) -> None:
        # Get a random joke
        my_q, my_a = self.get_joke()

        # Ask the question
        self.voice.say(my_q)
        
        # Pause

        # Say the punch line
        self.voice.say(my_a)

        return None