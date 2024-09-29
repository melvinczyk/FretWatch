from pathlib import Path
import audiovisual.recording as av
import audiovisual.signal_processing as sp
from config import settings
from matplotlib import pyplot as plt


if __name__ == "__main__":
    print(settings.devices)
    #recording = av.record_array(input_device=config_recording['default_input'], duration=3.0)
    base = 16.35
    octave_0 = sp.create_sin(5.0, base)
    octave_1 = sp.create_sin(5.0, base * 2)
    octave_2 = sp.create_sin(5.0, base * 4)
    octave_3 = sp.create_sin(5.0, base * 8)
    octave_4 = sp.create_sin(5.0, base * 16)
    combined = octave_1 + octave_0 + octave_2 + octave_3 + octave_4

    plt.plot(combined)
    plt.show()
    fig, axis = plt.subplots(2, 1)
    av.play_audio(combined)
