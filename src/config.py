import sounddevice as sd
from utils import load_config


class GlobalSettings(sd.default):

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
            self.devices = (recording_config['input_device'], recording_config['output_device'])
            self.samplerate = recording_config['samplerate']
            self.channels = recording_config['channels']
            self.duration = recording_config['duration']
            self._instance = True

    def reset(self):
        super().reset()
        self.duration = None

    def __repr__(self):
        parent_repr = super().__repr__()
        return f"{parent_repr}, duration={self.duration}"


settings = GlobalSettings()
