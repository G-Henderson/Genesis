# Import libraries - random & time
import random
from time import sleep


# Gets a random joke from the joke file
def get_joke():
    # Create string variable to store joke
    my_joke = "Did you hear about the monkeys who shared an Amazon account? They were Prime mates."
    
    # Return joke string variable
    return my_joke


# Tells the joke using the TTS engine
def tell_joke(voice_instance):
    # Get the joke
    my_joke = get_joke()

    # Use TTS engine to say joke
    voice_instance.say(my_joke)


# Main subroutine run by the main program (entry point)
def run(extras, cmd, args, voice_instance):       
    if (cmd != "tell me a joke"):
        # Witty reply
        response = ""
        # List of replies
        responses = ["I'm not sure it'll be funny but I'll try", "I can't make any promises but here goes.", "One funny joke coming right up.", "Here goes.", "Here's a real side-splitter!"]
        
        # Choose reply at random
        random_reply = random.randint(0, len(responses))
        reponse = responses[random_reply]        
        
        # Say reply
        voice_instance.say(response)
        
        
    # Tell joke
    tell_joke(voice_instance)
