import yaml
from pathlib import Path
import sounddevice as sd


def load_config(config_file='config.yaml'):
    project_dir = Path(__file__).parent.parent.resolve()
    config_path = project_dir / config_file

    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)

    return config


def set_devices():
    config = load_config()
    recording = config['recording']
    sd.default.device = (recording['default_input'], recording['default_output'])
    sd.default.samplerate = recording['sample_rate']
