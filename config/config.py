import json
from typing import TypedDict

# Keep this in sync with config.json
Config = TypedDict('config', {'is_dev': bool})

config: Config = json.load(open('config.json'))