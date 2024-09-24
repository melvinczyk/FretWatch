import librosa
import numpy as np
import sounddevice as sd
from scipy.io.wavfile import write


def record(input_device: int, output_device: int, duration: float, fs: int=44100) -> np.ndarray:
    sd.default.device = (input_device, output_device)
    sd.default.samplerate = fs
    sd.default.channels = 1
    recording = sd.rec(int(duration * fs), samplerate=fs)
    print("Recording.....................")
    sd.wait()
    return recording


def play_audio(array: np.ndarray, sr: int=44100):
    sd.play(array, sr)


