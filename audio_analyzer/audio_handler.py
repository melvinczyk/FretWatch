import librosa
import numpy as np


def load_file(file) -> (np.ndarray, float):
    try:
        signal, sr = librosa.load(file)
        return signal, sr
    except Exception as e:
        print(f"Error occurred: {e}")
        return None

