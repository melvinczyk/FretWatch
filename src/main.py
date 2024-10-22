import librosa

import audiovisual.recording as av
from scipy.io.wavfile import read
import audiovisual.signal_processing as sp
from config import settings
from matplotlib import pyplot as plt
import sounddevice as sd


if __name__ == "__main__":
    #sd.default.device[0] = 0
    path = av.record_file(duration=5)
    print(path)
    sr, signal = read(path)
    plt.plot(signal)
    plt.show()
