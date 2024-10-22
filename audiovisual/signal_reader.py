import numpy as np
import os
import tqdm
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from scipy.fftpack import fft
from scipy.io import wavfile
from pydub import AudioSegment

# Constants and Configuration
PATH = '/Users/nicholasburczyk/Documents/Coding/FretWatch/audiovisual'
AUDIO_FILE = "/Users/nicholasburczyk/Documents/Coding/FretWatch/audiovisual/recordings/Drop_C#.mp3"  # Path to the audio file
FPS = 30
FFT_WINDOW_SECONDS = 0.25
FREQ_MIN = 10
FREQ_MAX = 1000
TOP_NOTES = 3
NOTE_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
RESOLUTION = (1920, 1080)
SCALE = 2
FFT_WINDOW_SIZE = None
AUDIO_LENGTH = None


# Functions for Note and Frequency Conversion
def freq_to_number(f): return 69 + 12 * np.log2(f / 440.0)


def number_to_freq(n): return 440 * 2.0 ** ((n - 69) / 12.0)


def note_name(n): return NOTE_NAMES[n % 12] + str(int(n / 12 - 1))


# Hanning window function
def hanning_window(size):
    return 0.5 * (1 - np.cos(np.linspace(0, 2 * np.pi, size, False)))


# Plot FFT
def plot_fft(p, xf, fs, notes, dimensions=(960, 540)):
    layout = go.Layout(
        title="Frequency Spectrum",
        autosize=False,
        width=dimensions[0],
        height=dimensions[1],
        xaxis_title="Frequency (note)",
        yaxis_title="Magnitude",
        font={'size': 24}
    )

    fig = go.Figure(layout=layout,
                    layout_xaxis_range=[FREQ_MIN, FREQ_MAX],
                    layout_yaxis_range=[0, 1])

    fig.add_trace(go.Scatter(x=xf, y=p))

    for note in notes:
        fig.add_annotation(x=note[0] + 10, y=note[2],
                           text=note[1],
                           font={'size': 48},
                           showarrow=False)
    return fig


# Extract audio sample for FFT
def extract_sample(audio, frame_number, frame_offset, fft_window_size):
    end = frame_number * frame_offset
    begin = int(end - fft_window_size)

    if end == 0:
        return np.zeros((np.abs(begin)), dtype=float)
    elif begin < 0:
        return np.concatenate([np.zeros((np.abs(begin)), dtype=float), audio[0:end]])
    else:
        return audio[begin:end]


# Find top notes
def find_top_notes(fft, num, xf):
    if np.max(fft.real) < 0.001:
        return []

    lst = [x for x in enumerate(fft.real)]
    lst = sorted(lst, key=lambda x: x[1], reverse=True)

    idx = 0
    found = []
    found_note = set()
    while (idx < len(lst)) and (len(found) < num):
        f = xf[lst[idx][0]]
        y = lst[idx][1]
        n = freq_to_number(f)
        n0 = int(round(n))
        name = note_name(n0)

        if name not in found_note:
            found_note.add(name)
            s = [f, name, y]
            found.append(s)
        idx += 1

    return found


# Main Execution
def main():
    # Get the file extension
    file_extension = os.path.splitext(AUDIO_FILE)[1].lower()

    if file_extension == '.wav':
        # Handle WAV files
        fs, data = wavfile.read(AUDIO_FILE)
        audio = data.T[0]  # Extract one channel
    elif file_extension == '.mp3':
        # Handle MP3 files
        audio_segment = AudioSegment.from_mp3(AUDIO_FILE)
        fs = audio_segment.frame_rate  # Sample rate
        audio = audio_segment.get_array_of_samples()  # Convert to numpy array
    else:
        raise ValueError("Unsupported audio format. Please provide a WAV or MP3 file.")

    FFT_WINDOW_SIZE = int(fs * FFT_WINDOW_SECONDS)
    AUDIO_LENGTH = len(audio) / fs
    FRAME_COUNT = int(AUDIO_LENGTH * FPS)
    FRAME_OFFSET = int(len(audio) / FRAME_COUNT)
    xf = np.fft.rfftfreq(FFT_WINDOW_SIZE, 1 / fs)

    # Calculate Hanning window
    window = hanning_window(FFT_WINDOW_SIZE)

    # Pass 1: Find maximum amplitude for scaling
    mx = 0
    for frame_number in range(FRAME_COUNT):
        sample = extract_sample(audio, frame_number, FRAME_OFFSET, FFT_WINDOW_SIZE)
        fft = np.fft.rfft(sample * window)
        fft = np.abs(fft).real
        mx = max(np.max(fft), mx)

    print(f"Max amplitude: {mx}")

    # Pass 2: Generate images
    for frame_number in tqdm.tqdm(range(FRAME_COUNT)):
        sample = extract_sample(audio, frame_number, FRAME_OFFSET, FFT_WINDOW_SIZE)
        fft = np.fft.rfft(sample * window)
        fft = np.abs(fft) / mx  # Normalize

        top_notes = find_top_notes(fft, TOP_NOTES, xf)
        fig = plot_fft(fft.real, xf, fs, top_notes, RESOLUTION)
        fig.write_image(f"/Users/nicholasburczyk/Documents/Coding/FretWatch/audiovisual/content/frame{frame_number}.png", scale=SCALE)


if __name__ == "__main__":
    main()
