import librosa
import numpy as np
import sounddevice as sd


def load_file(file) -> (np.ndarray, float):
    try:
        signal, sr = librosa.load(file)
        return signal, sr
    except Exception as e:
        print(f"Error occurred: {e}")
        return None


def create_sin(frequency: float, duration: float, sr: int=44100) -> np.ndarray:
    print(f"default: {sd.default.samplerate}")
    t = np.linspace(0, duration, int(sr * duration), endpoint=False)
    amplitude = 0.5
    sine_wave = amplitude * np.sin(2 * np.pi * frequency * t)
    return sine_wave


def create_harmonic_sin(base_freq: float, harmonics: int, duration: int=5.0) -> np.ndarray:
    combined = create_sin(base_freq, duration)
    exponent = 2
    for i in range(0, harmonics):
        octave = create_sin(frequency=base_freq * exponent, duration=duration)
        combined += octave
        exponent *= 2
    return combined


def extract_frequency(signal: np.ndarray, sr: int):
    n = len(signal)
    signal = signal.flatten()
    frequencies = np.fft.fftfreq(n, 1/sr)
    fft_values = np.fft.fft(signal)

    magnitude = np.abs(fft_values)

    positive_freq = frequencies[:n // 2]
    positive_magnitude = magnitude[:n // 2]

    prominent_frequencies_indices = np.argsort(positive_magnitude)[-2:]  # Find indices of the 2 highest peaks
    prominent_freq = positive_freq[prominent_frequencies_indices]

    dominant_freq = positive_freq[np.argmax(positive_magnitude)]

    return prominent_freq
