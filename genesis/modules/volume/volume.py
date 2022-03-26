import alsaaudio
from time import sleep

import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish


# Send data to the MQTT Server
def sendData(voice_instance, address, payload, my_retain, iter=0):
    try:
        print(f"Publishing to MQTT server")
        publish.single(address, payload, retain=my_retain, hostname="homehub.home")

    except:
        if (iter < 3):
            voice_instance.say("Failed to publish data to the home hub. Trying again in 5 seconds...")
            sleep(5)
            sendData(voice_instance, address, payload, my_retain, iter+1)
        else:
            voice_instance.say("Data sending failed...")

# Change volume
def changeVol(vol, voice_instance, m):
    try:
        m.setvolume(int(vol))

        speech = "Volume set to "+vol+" percent"
        voice_instance.say(speech)

        # Send to MQTT Server
        sendData(voice_instance, "data/kitchen/genesis/volume", str(vol), True)

    except:
        voice_instance.say('Error setting volume!')

# Remove any other characters from the string
def stripString(begin):
    end = ""
    numbers = "0123456789"
    for i in range(len(begin)):
        if (begin[i] in numbers):
            end += begin[i]

    return end

# Main procedure
def run(extras, cmd, args, voice_instance):
    m = alsaaudio.Mixer()

    str_volume = stripString(args[-1])
    changeVol(str_volume, voice_instance, m)
