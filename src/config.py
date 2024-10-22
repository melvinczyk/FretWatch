import sounddevice as sd
from utils import load_config


class GlobalSettings:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(GlobalSettings, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, '_initialized'):
            loaded_config = load_config()
            recording_config = loaded_config['recording']

            super().__init__()
            self.devices = recording_config.get('input_device', sd.default.device[0]), \
                recording_config.get('output_device', sd.default.device[1])
            self.samplerate = recording_config.get('sample_rate', sd.default.samplerate)
            self.channels = recording_config.get('channels', sd.default.channels)
            self.duration = recording_config.get('duration', 5)

            sd.default.device = self.devices
            sd.default.samplerate = self.samplerate
            sd.default.channels = self.channels
            self._instance = True

    def reset(self):
        sd.default.reset()
        self.devices = sd.default.device
        self.samplerate = sd.default.samplerate
        self.channels = sd.default.channels
        self.duration = None

    def __repr__(self):
        return (f"GlobalSettings(device={self.devices}, "
                f"samplerate={self.samplerate}, "
                f"channels={self.channels}, "
                f"duration={self.duration}) ")


settings = GlobalSettings()

print(settings)
print(sd.default.samplerate)
