import os
import vlc
from subprocess import call
from gtts import gTTS
import pyttsx3
import time
from threading import Thread
from playsound import playsound

from utils.configuration import Configuration
import utils.Voices as Voices
from utils.LEDArray import LEDArray

class Voice:

    """
    Main class for TTS
    """

    def __init__(self, genesis_config: Configuration, led_ring: LEDArray) -> None:

        # Set the default voice (pico)
        self.my_voice = Voices.DEFAULT

        # Setup the pyttsx library
        self.engine = pyttsx3.init()

        self.genesis_config = genesis_config
        self.my_config = self.genesis_config.load_configuration()
        self.settings = self.my_config["settings"]
        self.location = self.settings["location"]
        self.platform = self.settings["platform"]

        # Create vlc instance
        self.vlc_instance = vlc.Instance("--no-video")
        self.player = self.vlc_instance.media_player_new()
        self.media_playlist = vlc.MediaListPlayer()

        # Set the language for gTTS
        self.ttsLanguage = self.settings["language"]

        # Setup the LED ring
        self.led_ring = led_ring

    def say(self, speech: str) -> None:
        print(speech)

        # Run speaking animation
        self.led_ring.speaking()

        if (self.my_voice == Voices.GOOGLE_TTS):
            self.speak_gtts(speech)

        elif (self.my_voice == Voices.PYTTSX):
            self.speak_pyttsx(speech)

        elif (self.my_voice == Voices.PICO):
            self.speak_pico(speech)
            
        elif (self.my_voice == Voices.MIMIC):
            self.speak_mimic(speech)

        elif (self.my_voice == Voices.MIMIC_2):
            self.speak_mimic_2(speech)

        # Stop speaking animation
        self.led_ring.reset()

    def speak_gtts(self, speech: str) -> None:
        try:
            # Create TTS object from 'speech' variable
            myObj = gTTS(text=str(speech), lang=self.ttsLanguage, slow=False)
            # Create audio file from TTS object
            myObj.save("response.mp3")
            # Play the audio file
            media = self.vlc_instance.media_new("response.mp3")

            self.player.set_media(media)
            self.player.play()

        except Exception as e:
            # Error with gTTS - print error
            print("Error whilst using gTTS:")
            print(e)

    def speak_pyttsx(self, speech: str) -> None:
        try:
            # use pyttsx library to speak
            self.engine.say(str(speech))
            # wait for engine to finish speaking
            self.engine.runAndWait()

        except Exception as e:
            # Catch errors with pyttsx - print error
            print("Error whilst using pyttsx:")
            print(e)

    def speak_pico(self, speech: str) -> None:
        try:
            # Create audio file with speech using PICO library
            call('pico2wave -w response.wav "' + speech + '"', shell=True)
            # Play audio file
            os.system("aplay response.wav")

        except Exception as e:
            # Error with Pico TTS - print error
            print("Error whilst using PICO:")
            print(e)

    def speak_mimic(self, speech: str) -> None:
        try:
            os.system("cd /home/pi/mimic")
        except Exception as e:
            print("Error whilst using Mimic TTS:")
            print(e)

    def speak_mimic_2(self, speech: str) -> None:
        pass

    def play_media(self, file_name: str) -> None:
        pass