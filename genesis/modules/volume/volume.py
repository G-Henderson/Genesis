import alsaaudio
from time import sleep
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
from random import randint

from utils.voice import Voice


class Module:

    """
    Module for adjusting the volume the device
    """

    def __init__(self, command: str, args: list, voice_instance: Voice, extras) -> None:
        # Initialise variables from the arguments
        self.command = command
        self.args = args
        self.voice = voice_instance
        self.extras = extras

        # Setup other variables
        self.VOLUME_TOPIC = "data/kitchen/genesis/volume"


    # Send data to the MQTT Server
    def sendData(self, voice_instance: Voice, address: str, payload: str, my_retain: bool, iter=0) -> None:
        try:
            print(f"Publishing to MQTT server")
            publish.single(address, payload, retain=my_retain, hostname="homehub.home")

        except:
            if (iter < 3):
                voice_instance.say("Failed to publish data to the home hub. Trying again in 5 seconds...")
                sleep(5)
                self.sendData(voice_instance, address, payload, my_retain, iter+1)
            else:
                voice_instance.say("Data sending failed...")

    # Change volume
    def changeVol(self, vol: str, voice_instance: Voice, m: alsaaudio.Mixer) -> None:
        try:
            m.setvolume(int(vol))

            responses = [f"Volume set to {vol} percent", f"I've set the volume to {vol} percent", f"Volume at {vol} percent"]
            speech = "Volume set to "+vol+" percent"
            voice_instance.say(speech)

            # Send to MQTT Server
            self.sendData(voice_instance, self.VOLUME_TOPIC, str(vol), True)

        except:
            voice_instance.say('Error setting volume!')

    # Remove any other characters from the string
    def stripString(self, begin: str) -> str:
        # Create new empty string for return
        end = ""
        # Setup 
        NUMBERS = "0123456789"
        for i in range(len(begin)):
            if (begin[i] in NUMBERS):
                end += begin[i]

        return end

    # Main procedure
    def run(self) -> None:
        # Setup the audio mixer object
        m = alsaaudio.Mixer()

        # Get the new audio level from the speech args
        str_volume = self.stripString(self.args[-1])
        # Set the new volume
        self.changeVol(str_volume, self.voice_instance, m)
