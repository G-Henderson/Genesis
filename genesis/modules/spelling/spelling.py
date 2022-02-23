from ast import Mod
from utils.Module import Module

class Spelling(Module):

    def spell(self, my_string):
        speech = my_string+" is spelt, "
        for i in range(len(my_string)):
            if (my_string[i] != " "):
                speech += my_string[i]

                if (i != len(my_string)-1):
                    speech += ", "

        self.voice.say(speech)

    def run(self):
        string_to_spell = " ".join(self.args)
        self.spell(string_to_spell, self.voice)