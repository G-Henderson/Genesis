import sounddevice as sd
from scipy.io.wavfile import write
import librosa
import numpy as np
from tensorflow.keras.models import load_model
from threading import Thread

FS = 44100
SECONDS = 2
FILENAME = "audio/prediction.wav"
CLASS_NAMES = ["NOT Detected", "Detected"]

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
            myrecording = sd.rec(int(SECONDS * FS), samplerate=FS, channels=2)
            sd.wait()
            write(FILENAME, FS, myrecording)

            audio, sample_rate = librosa.load(FILENAME)
            mfcc = librosa.feature.mfcc(y=audio, sr=sample_rate, n_mfcc=40)
            mfcc_processed = np.mean(mfcc.T, axis=0)

            prediction = self.model.predict(np.expand_dims(mfcc_processed, axis=0))
            if prediction[:, 1] > 0.99:
                print("Wake Word Detected")
                print("Confidence:", prediction[:, 1])
                pass

    def start_listening(self):
        pass

    def stop_listening(self):
        self.listening = False