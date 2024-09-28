import yaml
from pathlib import Path


def load_config(config_file='config.yaml'):
    project_dir = Path(__file__).parent.parent.resolve()
    config_path = project_dir / config_file

    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)

    return config

