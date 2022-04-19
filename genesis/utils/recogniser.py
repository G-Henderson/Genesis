import speech_recognition as sr
from threading import Thread

from utils.LEDArray import LEDArray
from utils.configuration import Configuration
from utils.voice import Voice

class Recogniser:

    def __init__(self, config: Configuration, led_array: LEDArray, voice_instance: Voice) -> None:
        # Setup TTS
        self.voice_instance = voice_instance

        # Setup the configuration
        self.my_config = config.load_configuration()
        self.settings = self.my_config["settings"]
        self.language = self.settings["language"]
        self.platform = self.settings["platform"]

        # Setup the speech recogniser
        self.recogniser = sr.Recognizer()

        # Setup the microphone
        self.microphone = sr.Microphone()

        # Setup the LED array
        self.led_array = led_array

        # Create the error messages
        self.error_msg = "__error__"
        self.unknown_msg = "__unknown__"

    def play_listening_noise(self, voice_instance: Voice) -> None:
        """
        Plays the listening noise

        voice_instance: the instance of the voice class to play the sound
        """

        # Create a new thread for playing the noise asynchronously
        t = Thread(name="listening_noise", target=voice_instance.play_media("audio/Wah.mp3"))
        # Start the thread
        t.start()

    def recognise(self) -> str:
        """
        Run speech to text recognition,
        return the speech as a string
        """

        # Adjust for background noise
        with self.microphone as source:
            self.recogniser.adjust_for_ambient_noise(source)

        # Play the listening noise
        self.play_listening_noise(voice_instance)

        # Play the listening animation
        self.led_array.listening()

        # Start listening
        with self.microphone as source:
            audio = self.recogniser.listen(source)

        # Disable the listening light
        self.led_array.reset()

        # Enable the processing light
        self.led_array.loading()

        try:
            # Recognise the audio using Google Speech Recognition
            voice_input = str(
                self.recogniser.recognize_google(
                    audio, language=self.language
                )
            ).lower()

            # Disable the processing light
            self.led_array.reset()

            # Return the text
            return voice_input

        except sr.UnknownValueError:
            # Disable processing light
            self.led_array.reset()

            # Voice feedback
            self.voice_instance.say("Sorry, I didn't catch that...")

            # Return error
            return self.unknown_msg

        except sr.RequestError as e:
            # Disable processing light
            self.led_array.reset()

            print(
                "Uh oh! Couldn't request results from Google Speech Recognition service; {0}".format(
                    e
                )
            )

            # Voice feedback
            self.voice_instance.say("There was a speech recognition error. Check your network connection and try again...")

            # Return error
            return self.error_msg