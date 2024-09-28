from pathlib import Path
import audiovisual.recording as av
import utils
import sounddevice as sd


if __name__ == "__main__":
    config = utils.load_config()
    config_recording = config['recording']
    recording = av.record_array(input_device=config_recording['default_input'], duration=5.0)
    av.play_audio(recording, output_device=config_recording['default_output'])
