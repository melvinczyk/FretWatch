import librosa
import numpy as np
import sounddevice as sd
from scipy.io.wavfile import write
from pathlib import Path


def record_array(input_device: int, duration: float=10.0, sr: int=44100) -> np.ndarray:
    sd.default.device = (input_device, None)
    sd.default.samplerate = sr
    sd.default.channels = 1
    recording = sd.rec(int(duration * sr), samplerate=sr)
    print("Recording.....................")
    sd.wait()
    return recording


def record_file(input_device: int, file_name: str, duration: float=10.0, sr: int=44100) -> Path:
    sd.default.device = (input_device, None)
    sd.default.samplerate = sr
    sd.default.channels = 1,
    recording = sd.rec(int(duration * sr), samplerate=sr)
    print("Recording.....................")
    sd.wait()
    write(file_name, sr, data=recording.astype(np.int16))
    return output_path

def play_audio(array: np.ndarray, output_device: int, sr: int=44100):
    sd.default.device = None, output_device
    sd.play(array, sr)


