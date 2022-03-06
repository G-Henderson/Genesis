from threading import Thread
import sounddevice as sd
from scipy.io.wavfile import write
import librosa
import numpy as np
from tensorflow.keras.models import load_model

fs = 44100
seconds = 2
filename = "prediction.wav"
class_names = ["Wake Word NOT Detected", "Wake Word Detected"]

class WakewordListener:

    """
    Class for listening for the wakeword
    E.g Genesis, Alexa, Hey Google
    """

    def __init__(self) -> None:
        self.listening = False
        self.model = load_model("wake_word_models/Genesis.h5")

    def run_wake_word_detection(self) -> None:
        while self.listening:
            print("Say Now: ")
            myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
            sd.wait()
            write(filename, fs, myrecording)

            audio, sample_rate = librosa.load(filename)
            mfcc = librosa.feature.mfcc(y=audio, sr=sample_rate, n_mfcc=40)
            mfcc_processed = np.mean(mfcc.T, axis=0)

            prediction = self.model.predict(np.expand_dims(mfcc_processed, axis=0))
            if prediction[:, 1] > 0.99:
                print(f"Wake Word Detected for ({i})")
                print("Confidence:", prediction[:, 1])
                i += 1
            
            else:
                print(f"Wake Word NOT Detected")
                print("Confidence:", prediction[:, 0])

    def start_listening(self):
        try:
            # Set listening to true
            self.listening = True

            # Create a new thread
            t = Thread(name="wake-word-thread", target=self.run_wake_word_detection)
        except:
            pass

    def stop_listening(self):
        self.listening = False