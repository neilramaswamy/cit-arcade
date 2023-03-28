import json
from typing import TypedDict

# Keep this in sync with config.json
Config = TypedDict('config', { 'is_dev': bool,
    'horz_side_length': int, 
    'vert_side_length': int,
    'horz_panels': int,
    'vert_panels': int })

config: Config = json.load(open('config.json'))