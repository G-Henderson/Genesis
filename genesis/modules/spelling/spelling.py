def spell(my_string, voice_instance):
    speech = my_string+" is spelt, "
    for i in range(len(my_string)):
        if (my_string[i] != " "):
            speech += my_string[i]

            if (i != len(my_string)-1):
                speech += ", "

    voice_instance.say(speech)

def run(extras, cmd, args, voice_instance):
    string_to_spell = " ".join(args)
    spell(string_to_spell, voice_instance)