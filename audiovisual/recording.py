import yaml
import numpy as np
import sounddevice as sd
from scipy.io.wavfile import write
from pathlib import Path
import sys
import time
import threading


def record_array(input_device: int, duration: float=10.0, sr: int=44100) -> np.ndarray:
    sd.default.device = (input_device, None)
    sd.default.samplerate = sr
    sd.default.channels = 1
    recording = sd.rec(int(duration * sr), samplerate=sr)

    display_thread = threading.Thread(target=show_progress, args=(duration,))
    display_thread.start()
    sd.wait()
    display_thread.join()
    return recording


def record_file(input_device: int=None, file_name: str='output.wav', duration: float=10.0, sr: int=44100) -> Path:
    if input_device is not None:
        sd.default.device = (input_device, None)
    else:
        pass
        sd.default.device = None
    sd.default.samplerate = sr
    sd.default.channels = 1

    project_dir = Path(__file__).parent.resolve()
    recordings_dir = project_dir / 'recordings'
    recordings_dir.mkdir(exist_ok=True)
    recordings_path = recordings_dir / file_name

    recording = sd.rec(int(duration * sr), samplerate=sr)

    display_thread = threading.Thread(target=show_progress, args=(duration,))
    display_thread.start()
    sd.wait()
    display_thread.join()
    write(str(recordings_path), sr, data=recording.astype(np.int16))
    print(f"Path saved to: {recordings_path}")
    return recordings_path


def play_audio(array: np.ndarray, output_device: int, sr: int=44100):
    sd.default.device = None, output_device
    sd.play(array, sr)


def show_progress(duration):
    start_time = time.time()
    while True:
        elapsed_time = time.time() - start_time
        progress = min(elapsed_time / duration * 100, 100)
        sys.stdout.write(f"\rRecording: {progress:.2f}%")
        sys.stdout.flush()

        if elapsed_time >= duration:
            break
        time.sleep(0.01)

