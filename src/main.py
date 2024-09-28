from pathlib import Path
import audiovisual.recording as av
import audiovisual.signal_processing as sp
import utils
from matplotlib import pyplot as plt


if __name__ == "__main__":
    config = utils.load_config()
    config_recording = config['recording']
    recording = av.record_array(input_device=config_recording['default_input'], duration=5.0)
    sine_wave = sp.create_sin(5.0, 65)
    another_wave = sp.create_sin(5.0, 98)
    combined = sine_wave + another_wave
    print(sp.extract_frequency(recording, 44100))
    fig, axis = plt.subplots(2, 1)
    axis[0].plot(recording)
    axis[1].plot(combined)
    plt.show()
    #av.play_audio(recording, output_device=config_recording['default_output'])
