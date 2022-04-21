import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

from utils.setup import load_config
from utils.settings import get_addon_settings

import json
from time import sleep
import random


USER_SETTINGS = get_addon_settings("homecontrol")
HOST_NAME = USER_SETTINGS["hostname"]
ROOM_POSITION = USER_SETTINGS["roomname"]


# Called during user interactions
def sendData(voice_instance, address, payload, my_retain, iter=0):
    try:
        print(f"Publishing to MQTT server")
        if (isinstance(address, list)):
            for i in range(len(address)):
                publish.single(address[i], payload, retain=my_retain, hostname=HOST_NAME)

        else:
            publish.single(address, payload, retain=my_retain, hostname=HOST_NAME)

        respond(voice_instance)

    except:
        if (iter < 5):
            voice_instance.say("Failed to publish data to the home hub. Trying again in 5 seconds...")
            sleep(5)
            sendData(voice_instance, address, payload, my_retain, iter+1)
        else:
            voice_instance.say("Data sending failed...")


def respond(voice_instance):
    responses = ["Okay", "Sure", "OK"]

    my_index = random.randint(0,len(responses)-1)
    response = responses[my_index]

    voice_instance.say(response)


def parse_query(main, command, args):
    if (main == "turn") or (main == "put"):
        action = ""
        device = ""

        # Check if 'one' is a substring
        if "one" in command:
            # replace with number 1
            command = command.replace("one", "1")
            if ("one" in args):
                my_index = args.index("one")
                args[my_index] = "1"      

        if "on" in command:
            action = "on"
            if "light" in command:
                if "hall" in command:
                    device = "hall light"

                elif "bedroom" in command:
                    if "1" in command:
                        device = "george's bedroom light 1"

                    elif "two" in command:
                        device = "george's bedroom light 2"

                    else:
                        device = "george's bedroom light group"

                else:
                    device = ROOM_POSITION+" light group"

            elif "heating" or "boiler" in command:
                device = "heating"

                # Check for boost
                if ("for" in command):
                    # Check if 'an' is a substring and replace it with one
                    if "an" in command:
                        # replace with number 1
                        command = command.replace("an", "1")
                        if ("an" in args):
                            my_index = args.index("an")
                            args[my_index] = "1"

                    if ("minute" in args):
                        my_index = args.index("minute")
                        my_time = args[my_index-1]
                        try:
                            my_time = int(my_time) * 60
                        except:
                            return "unknown time"

                    elif ("hour" in args):
                        my_index = args.index("hour")
                        my_time = args[my_index-1]
                        try:
                            my_time = int(my_time) * 60
                        except:
                            return "unknown time"

                    elif ("minutes" in args):
                        my_index = args.index("minutes")
                        my_time = args[my_index-1]
                        try:
                            my_time = int(my_time)
                        except:
                            return "unknown time"

                    elif ("hours" in args):
                        my_index = args.index("hours")
                        my_time = args[my_index-1]
                        try:
                            my_time = int(my_time) * 60
                        except:
                            return "unknown time"

                    try:
                        return my_time
                    except:
                        return "unknown time"


        elif "off" in command:
            action = "off"
            if "light" in command:
                if "hall" in command:
                    device = "hall light"

                elif "bedroom" in command:
                    if "1" in command:
                        device = "george's bedroom light 1"

                    elif "two" in command:
                        device = "george's bedroom light 2"

                    else:
                        device = "george's bedroom light group"

                else:
                    device = ROOM_POSITION+" light group"

            elif "heating" or "boiler" in command:
                device = "heating"


        query = json.loads('{"action":"'+action+'", "device":"'+device+'"}')
        return query

    elif (main == "temperature") and ("color" not in command):
        if "outside" in command:
            location = "outside"

        elif "extension" in command:
            location = "extension"

        else:
            location = "inside"

        return location

    elif (main == "light"):
        # Get the brightness from the speech arguments
        bright_string = args[-1]
        print(bright_string)
        # Create an empty variale to contain the brightness as an integer
        filtered_bright_string = ""
        # Create list of integers
        num_string = "1234567890"
        # Iterate through raw string, checking if character is an int
        for i in range(len(bright_string)):
            if (bright_string[i] in num_string):
                filtered_bright_string += bright_string[i]

        return filtered_bright_string

    elif (main == "dimmer"):
        # Get the brightness from the speech arguments
        bright_string = args[-1]
        print(bright_string)
        # Create an empty variale to contain the brightness as an integer
        filtered_bright_string = ""
        # Create list of integers
        num_string = "1234567890"
        # Iterate through raw string, checking if character is an int
        for i in range(len(bright_string)):
            if (bright_string[i] in num_string):
                filtered_bright_string += bright_string[i]

        return filtered_bright_string

    elif (main == "colour temperature"):
        if ("warm" in command):
            colour = "00000000FF"

        else:
            colour = "000000FF00"

        return colour

    elif (main == "colour") and ("temperature" not in command):
        if ("green" in command):
            colour = "08FF000000"

        elif ("red" in command):
            colour = "FF04000000"

        elif ("blue" in command):
            colour = "002AFF0000"

        elif ("cyan" in command):
            colour = "00FFB20000"

        elif ("pink" in command):
            colour = "FF00730000"

        elif ("purple" in command):
            colour = "FF00FB0000"

        elif ("orange" in command):
            colour = "FF66000000"

        elif ("yellow" in command):
            colour = "FFBF000000"

        else:
            colour = "unknown"

        return colour

"""
def toggleLights():
    action = "toggle"
    device = ROOM_POSITION+" light"

    query = json.loads('{"action":"'+action+'", "device":"'+device+'"}')
    return query
"""

def execute_action(query, voice_instance):
    actions = {
        "heating": "house/boiler/command/mode",
        "hall light": "cmnd/sonoff/POWER",
        "george's bedroom light 1": "cmnd/bedroom1/Power",
        "george's bedroom light 2": "cmnd/bedroom2/Power",
        "george's bedroom light group": ["cmnd/bedroom1/Power","cmnd/bedroom2/Power"],
    }
    """
        "outside lights": "",
        "path lights": "",
        "patio light": "",
    }
    """

    print(actions[query["device"]])
    print(query["action"])

    sendData(voice_instance, actions[query["device"]], query["action"], False)


def boost_heating(query, voice_instance):
    if (str(query).isdigit()):
        responses = ["I have put the heating on for ", "Ok, turning the heating on for "]
        rand_index = random.randint(0,len(responses)-1)
        speech = responses[rand_index] + str(query) + "minutes."
        voice_instance.say(speech)

        # Send data to MQTT server
        data = str(query)
        topic = "house/boiler/boost"
        sendData(voice_instance, topic, data, True)

    else:
        responses = ["I have set the heating mode to on.", "I have turned the heating on.", "The heating is now on."]
        rand_index = random.randint(0,len(responses)-1)
        speech = responses[rand_index]
        voice_instance.say(speech)


def answer_action(mqttObj, query, voice_instance):
    speech = ""

    if (query == "inside"):
        speech = "The inside temperature is "+mqttObj.getInsideTemp()+" degrees"
        
    elif (query == "outside"):
        speech = "The outside temperature is "+mqttObj.getOutsideTemp()+" degrees"

    elif (query == "extension"):
        speech = "It is "+mqttObj.getExtensionTemp()+" degrees in the extension"

    elif (query == "floor"):
        speech = "The floor temperature is set to "+mqttObj.getFloorTemp()+" degrees"

    else:
        speech = "Sorry, it looks like that temperature sensor hasn't been set up yet!"

    voice_instance.say(speech)

# Checks the status of the boiler/heating
def checkHeatingStatus(mqttObj, q, voice_instance):
    if (q == "on") and (mqttObj.getBoilerStatus() == "1"):
        speech = "Yes, it is."

    elif (q == "off") and (mqttObj.getBoilerStatus() == "1"):
        speech = "No, the heating is on."

    elif (q == "off") and (mqttObj.getBoilerStatus() == "0"):
        speech = "Yes, it is."

    elif (q == "on") and (mqttObj.getBoilerStatus() == "0"):
        speech = "No, the heating is off"

    else:
        speech = "Hmmm. I'm not sure... There may be an mqtt problem."

    voice_instance.say(speech)

def run(mqttObj, command, args, voice_instance):
    print(args)

    if (len(args) > 1):
        query = parse_query(command, " ".join(args), args)
    else:
        query = args[0]

    if (("turn" in command) or ("put" in command)) and ("for" not in args):
        execute_action(query, voice_instance)

    elif (("turn" in command) or ("put" in command)) and ("for" in args):
        boost_heating(query, voice_instance)

    elif "light" in command:
        if query == "s":
            #query = toggleLights()
            print("Toggling lights")
            sendData(voice_instance, ["cmnd/bedroom1/Power","cmnd/bedroom2/Power"], "toggle", False)

        elif "set" in args:
            # Change light properties, e.g brightness, color
            if "colour" in args:
                # Set the color the lamp
                colour = args[-1]

            # Set the brightness of the lamp
            elif "brightness" in args:
                # Send the brightness to the server
                print(query)
                sendData(voice_instance, ["cmnd/bedroom1/Dimmer","cmnd/bedroom2/Dimmer"], query, False)

            elif "temperature" in query:
                # Set the colour temperature of the lamp
                colour_temp = args[-1]

    elif command == "dimmer":
        # Send the brightness to the server
        print(query)
        sendData(voice_instance, ["cmnd/bedroom1/Dimmer","cmnd/bedroom2/Dimmer"], query, False)

    elif command == "colour temperature":
        sendData(voice_instance, ["cmnd/bedroom1/Color","cmnd/bedroom2/Color"], query, False)

    elif (command == "colour") and ("temperature" not in args):
        if (query != "unknown"):
            sendData(voice_instance, ["cmnd/bedroom1/Color","cmnd/bedroom2/Color"], query, False)
        else:
            # Feedback about unknown colour
            # Create list of responses
            responses = ["I don't know that one", "I don't know that colour", "I don't recognise that colour"]
            # Generate random number in range of the length of responses
            chosen = random.randint(0,len(responses)-1)
            # Create variable and assign the random response
            response = responses[chosen]
            # Respond
            voice_instance.say(response)

    elif (command == "temperature") and ("colour" not in args):
        answer_action(mqttObj, query, voice_instance)

    elif command == "is the boiler":
        checkHeatingStatus(mqttObj, query, voice_instance)

    elif command == "is the heating":
        checkHeatingStatus(mqttObj, query, voice_instance)

    return None
