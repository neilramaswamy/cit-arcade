from typing import Tuple
import os
import pickle
from leds.strip import get_strip 

# Top-level directory
STORE_PATH = os.path.expanduser("~/.citarcade")

# Interactive CLI tool to create a mapping from row-major index to strip index
def create_map(panel_width, panel_height, panels_wide, panels_high) -> dict:
    mapping = {}

    strip = get_strip()
    strip.begin()

    num_panels = panels_wide * panels_high
    num_leds = panel_width * panel_height

    for i in range(num_panels):
        root_led = i * num_leds

        # Illuminate the first 3 pixels of this panel
        for j in range(3):
            strip.setPixelColorRGB(root_led + j, 1, 0, 0)
        strip.show()
        
        # Determine the corner and direction
        (corner, direction) = ask_for_orientation()

        panel_map = get_map_from_orientation(root_led, panel_width, panel_height, corner, direction)
        for k, v in panel_map.items():
            mapping[k] = v

    return mapping


def get_map_from_orientation(root_led, panel_width, panel_height, corner, direction) -> dict:
    assert(corner >= 0 and corner <= 3)
    assert(direction == "H" or direction == "V")

    # from row-major to strip index
    mapping = {}

    if corner == 0 and direction == "H":
        for i in range(panel_height):
            for j in range(panel_width):
                rm_index = root_led + ((i * panel_width) + j)

                if i % 2 == 0:
                    strip_index = (i * panel_width) + j
                else:
                    strip_index = (i * panel_width) + ((panel_width - 1) - j)
                    
                mapping[rm_index] = strip_index
    else:
        raise RuntimeError("Not yet implemented")

    return mapping

# Orientation gets the positioning of the first 3 LEDs of a panel. Reports back the corner and
# direction of the first few LEDs.
# 
# The corner is (0, 1, 2, 3) for (top left, top right, bottom left, bottom right). The orientation
# is either horizontal or vertical.
def ask_for_orientation() -> Tuple[int, str]:
    valid_corners = [str(i) for i in range(4)]
    valid_directions = ["H", "V"]

    corner = -1
    while corner < 0:
        corner_str = input("Corner for panel: ")

        if corner_str not in valid_corners:
            print("Input must be in range [0, 3]")
        else:
            corner = int(corner_str)
    
    direction = ""
    while direction == "":
        direction_str = input("Direction of LEDs: ")

        if direction_str not in valid_directions:
            print("Direction must be H or V")
        else:
            direction = direction_str

    return (corner, direction)

def save_map(name: str, mapping: dict):
    path = os.path.join(STORE_PATH, name)

    if not os.path.exists(STORE_PATH):
        os.mkdir(STORE_PATH)

    with open(path, 'w+b') as f:
        pickle.dump(mapping, f)
    
    print(f"Successfully saved map to {path}")
    return

def load_map(name: str) -> dict:
    path = os.path.join(STORE_PATH, name)

    if os.path.exists(path):
        print(f"Found existing map at {path}")

        with open(path, 'rb') as f:
            loaded_dict = pickle.load(f)        
            return loaded_dict
    
    print(f"Did not find existing map at {path}") 
    return None

def ensure_map() -> dict:
    name = input("Name for calibration: ")
    loaded_map = load_map(name)

    if loaded_map is None:
        panel_width = int(input("Panel width (number of LEDs): "))
        panel_height = int(input("Panel height (number of LEDs): "))
        panels_wide = int(input("Number of panels across: "))
        panels_high = int(input("NUmber of panels high: "))

        loaded_map = create_map(panel_width, panel_height, panels_wide, panels_high)
        save_map(name, loaded_map)

    print(f"Mapping is {str(loaded_map)}")
    return loaded_map

if __name__ == "__main__":
    command = input("Inspect map or create new? [I/C]: ")
    if command == "I":
        name = input("Name of calibration: ")
        loaded_map = load_map(name)
        print(f"Mapping is {str(loaded_map)}")
    elif command == "C":
        ensure_map()
    else:
        print("Invalid command")