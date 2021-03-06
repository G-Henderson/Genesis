import random
from time import strftime
from time import sleep
import json

import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

from utils.recognition import myCommand

def normal_greeting(voice_instance):
    greetings = ["Hello! How are you?", "Hello! What's up?"]

    which_greeting = random.randint(0, len(greetings)-1)
    voice_instance.say(greetings[which_greeting])


# Called during user interactions
def sendData(voice_instance, address, payload, my_retain, iter=0):
    try:
        print(f"Publishing to MQTT server")
        publish.single(address, payload, retain=my_retain, hostname="homehub.home")

    except:
        if (iter < 5):
            print.say("Failed to publish data to the home hub. Trying again in 5 seconds...")
            sleep(5)
            sendData(voice_instance, address, payload, my_retain, iter+1)
        else:
            voice_instance.say("Data sending failed...")


def morning_routine(voice_instance):
    # Turn on the light
    sendData(voice_instance, "cmnd/bedroom1/Power", "on", False)

def night_routine(voice_instance, alarm_obj):
    # Set alarm for tomorrow
    voice_instance.say("What time would you like me to set the alarm for?")
    #voice_instance.say("I have set the alarm for six twenty tomorrow.")

    # Check if got valid alarm time
    valid_time = False
    need_time = True

    # Get user input for alarm time using voice input library
    while ((valid_time == False) and (need_time == True)):
        try:
            # Get voice input
            voice_q = myCommand()

            # Check for cancellations
            if ("cancel" in voice_q) or ("none" in voice_q) or ("don't" in voice_q):
                need_time = False

            # Get alarm time
            else:
                print(voice_q)
                valid_time = True

        except Exception as e:
            voice_instance.say("Sorry, what time?")

    # Check if we are setting an alarm
    if (need_time == True):
        # Add the alarm to the alarm array
        voice_instance.say("OK, I have set the alarm for eight o'clock tomorrow")
        new_alarm = {"label":"Good morning George!", "hour":"08", "minute":"00"}
        alarm_obj.append(new_alarm)

    # Don't set an alarm
    else:
        voice_instance.say("Sure, I haven't set an alarm. Enjoy your lie in!")

    # Turn off the light
    sendData(voice_instance, "cmnd/bedroom1/Power", "off", False)

    # return the alarm object
    return alarm_obj


def good_greeting(spec_time, voice_instance, extras=None):
    speech = ""
    hour_of_day = int(strftime('%H'))
    print(hour_of_day)
    my_result = None

    if spec_time == "morning":
        greetings = ["Top of the mornin' to ya!", "Morning!", "Good morning.", "Nice to see you!"]

        if (hour_of_day < 7):
            greetings.append("Good morning. You're up early!")

        which_greeting = random.randint(0, len(greetings)-1)
        speech = greetings[which_greeting]

        if (hour_of_day >= 12):
            speech += " Or should I say afternoon!"
        else:
            # Run morning routine
            morning_routine(voice_instance)

    elif spec_time == "day":
        greetings = ["Hey there! Let me know if I can help.", "Hi. How can I help?", "Hi. What can I do for you?", "Nice to see you!"]

        if (hour_of_day < 12):
            greetings.extend(["Top of the mornin' to ya!", "Morning!", "Good morning."])

        elif (hour_of_day >= 12) and (hour_of_day < 18):
            greetings.extend(["Afternoon!", "Good afternoon."])

        else:
            greetings.extend(["Evening!", "Good evening."])

        which_greeting = random.randint(0, len(greetings)-1)
        speech = greetings[which_greeting]

    elif spec_time == "afternoon":
        greetings = ["Hi. How can I help?", "Hi. What can I do for you?", "Nice to see you!"]

        if (hour_of_day >= 12):
            greetings.extend(["And a very good afternoon to you, as well. Let me known if there's anything I can help you with!", "Afternoon!", "Good afternoon."])

        which_greeting = random.randint(0, len(greetings)-1)
        speech = greetings[which_greeting]

    elif spec_time == "evening":
        greetings = ["Hi. How can I help?", "Hi. What can I do for you?", "Nice to see you!"]

        if (hour_of_day >= 17):
            greetings.extend(["And a very good evening to you, as well. Let me known if there's anything I can help you with!", "Evening!", "Good evening."])

        which_greeting = random.randint(0, len(greetings)-1)
        speech = greetings[which_greeting]

    elif spec_time == "night":
        greetings = ["Goodnight!", "Night night.", "Sleep well!"]

        which_greeting = random.randint(0, len(greetings)-1)
        speech = greetings[which_greeting]

        if (hour_of_day < 19):
            speech += " You are going to bed early!"
        else:
            # Run night routine
            my_result = night_routine(voice_instance, extras)

    voice_instance.say(speech)

    return my_result


def gratitude_reply(voice_instance):
    replies = ["It's a pleasure to serve", "Cheers mate", "You are extremely welcome", "You're most welcome"]

    which_reply = random.randint(0, len(replies)-1)
    voice_instance.say(replies[which_reply])


def talk_about_feelings(voice_instance):
    parts = ["I'm splendid! Thank you for asking", "I'm grand, thanks."]

    which_part = random.randint(0, len(parts)-1)
    speech = parts[which_part]

    voice_instance.say(speech)


def run_name(voice_instance):
    speech = "My name is \"Genesis\""
    parts = [". I like to think of it as a cool nickname.", ", because I like to keep it short and sweet.", ". It's great to meet you!"]

    which_part = random.randint(0, len(parts)-1)
    speech += parts[which_part]

    voice_instance.say(speech)


def run_bio(voice_instance):
    speech = "I'm Genesis, your personal assistant. "
    parts = ["I can set timers and add things to your shopping list.", "I like helping you and taking long walks on the beach, provided a long enough extension cord or a charger!", "I can control the lights and adjust the thermostat", "I can tell you the time and read you the news", "I can read you the weather forecast and set timers"]

    which_part = random.randint(0, len(parts)-1)
    speech += parts[which_part]

    voice_instance.say(speech)


def offensive(cmd, voice_instance):
    if (cmd == "bye"):
        parts = ["Goodbye, and stay well!", "Have a good day!", "I'll say goodbye in German. Auf wiedersehen!", "See you later alligator!", "See you later!"]

    elif (cmd == "ali"):
        parts = ["In a while croc-a-dile!"]

    elif (cmd == "go away"):
        parts = ["Got it, I'll stop.", "Ok, I'll leave you be", "Sure, I'll stop"]

    elif (cmd == "nothing"):
        parts = ["Oh, ok", "Sure, my bad", "Okay", "Ok"]

    elif (cmd == "shut"):
        parts = ["Oh", "That's rude!", "Ok"]


    which_part = random.randint(0, len(parts)-1)
    speech = parts[which_part]

    voice_instance.say(speech)


def run(extras, cmd, args, voice_instance):
    print(args)
    command = str(cmd)
    my_return = None

    # Normal greetings
    if command == "hello":
        normal_greeting(voice_instance)

    elif command == "hey":
        normal_greeting(voice_instance)

    elif command == "hi" and args[0] != "notng":
        normal_greeting(voice_instance)


    # Good day greetings
    elif "morning" in command:
        good_greeting("morning", voice_instance)

    elif "evening" in command:
        good_greeting("evening", voice_instance)

    elif "afternoon" in command:
        good_greeting("afternoon", voice_instance)

    elif "day" in command:
        good_greeting("day", voice_instance)

    elif "night" in command:
        my_return = good_greeting("night", voice_instance, extras)

    
    # Gratitude
    elif (command == "thanks") or (command == "thank you"):
        gratitude_reply(voice_instance)


    # Questions
    elif command == "how are you":
        talk_about_feelings(voice_instance)

    elif command == "who are you":
        run_bio(voice_instance)

    elif "your name" in command:
        run_name(voice_instance)


    # Offensive
    elif command == "nothing":
        offensive("nothing", voice_instance)

    elif command == "go away":
        offensive("go", voice_instance)

    elif "bye" in command:
        offensive("bye", voice_instance)

    elif command == "see you later":
        offensive("bye", voice_instance)

    elif "alligator" in command:
        offensive("ali", voice_instance)

    elif "shut up" == command:
        offensive("shut", voice_instance)

    return my_return
