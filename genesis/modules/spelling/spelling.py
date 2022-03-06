from utils.voice import Voice
from random import randint

class Module:

    def __init__(self, command: str, args: list, voice_instance: Voice, extras) -> None:
        # Initialise variables from the arguments
        self.command = command
        self.args = args
        self.voice = voice_instance
        self.extras = extras

    def spell(self, my_string) -> None:
        speech = self.get_prefix(my_string)
        for i in range(len(my_string)):
            if (my_string[i] != " "):
                speech += my_string[i]

                if (i != len(my_string)-1):
                    speech += ", "

        self.voice.say(speech)

    def get_prefix(self, my_string) -> str:
        # Create list of possible response prefixes
        prefixes = [f"{my_string} is spelt, ", "It's spelt, ", "That's spelt, ", ""]
        
        # Generate a random number up to the length of the list
        my_index = randint(0, len(prefixes)-1)

        # Return the response prefix at that index
        return prefixes[my_index]

    def run(self) -> None:
        string_to_spell = " ".join(self.args)
        self.spell(string_to_spell, self.voice)

        return None