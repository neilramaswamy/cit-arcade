from typing import Tuple
import os
import pickle
from leds.mux import Color, get_strip
from config.config import config
from mapper.panel_config import PanelConfig

# Top-level directory
STORE_PATH = os.path.expanduser("~/.citarcade")

# Interactive CLI tool to create a mapping from row-major index to strip index
def create_map(panel_width, panel_height, panels_wide, panels_high) -> dict:
    mapping = {}
    strip = get_strip(panel_width, panel_height, panels_wide, panels_high)

    num_panels = panels_wide * panels_high
    num_leds = panel_width * panel_height

    for i in range(num_panels):
        strip_root = i * num_leds

        # Determine the corner and direction
        if config.get('is_dev'):
            (panel_index, corner, direction) = (i, 0, "D")
        else:
            # Illuminate the first 3 pixels of this panel
            for j in range(3):
                strip.setPixelColor(strip_root + j, Color(255, 0, 0))
            strip.show()

            (panel_index, corner, direction) = ask_for_orientation(num_panels)

        rm_root = derive_rm_root(panel_index, panel_width, panel_height, panels_wide, panels_high)

        panel_map = get_map_from_orientation(strip_root, rm_root, panel_width, panel_height, panels_wide, panels_high, corner, direction)
        for k, v in panel_map.items():
            mapping[k] = v

    return mapping

def derive_rm_root(panel_index, panel_width, panel_height, panels_wide, panels_high) -> int:
    # Which row/col (in the entire display) does panel_index reside on
    display_row = panel_index // panels_wide
    display_col = panel_index % panels_wide

    num_pixels_per_panel = panel_width * panel_height

    return (display_row * (panels_wide * num_pixels_per_panel)) + (display_col * panel_width)

# A panel's mapping is determined by two factors: its positioning within the entire grid, and its
# snaking pattern. The strip_root gives the first pixels in this panel's strip index, and the
# rm_root gives the row-major index of that pixel.
def get_map_from_orientation(strip_root, rm_root, panel_width, panel_height, panels_wide, panels_high, corner, direction) -> dict:
    assert(corner >= 0 and corner <= 3)
    # Horizontal, Vertical, Development
    assert(direction == "H" or direction == "V" or direction == "D")

    # from row-major to strip index
    mapping = {}

    if corner == 0 and direction == "H":
        for i in range(panel_height):
            for j in range(panel_width):
                # Because of the snaking pattern, how far we are from the left (i.e. horiz_offset)
                # is not simply j. It's j on even rows, and j from the right on odd rows.
                if i % 2 == 0:
                    horiz_offset = j
                else:
                    horiz_offset = ((panel_width - 1) - j)

                # The row-major vertical offset is a function of how wide the *entire* display is
                rm_vert_offset = (i * (panel_width * panels_wide))
                rm_index = rm_root + rm_vert_offset + horiz_offset

                strip_offset = (i * panel_width) + j
                mapping[rm_index] = strip_root + strip_offset 
    elif corner == 0 and direction == "D":
        for i in range(panel_height):
            for j in range(panel_width):
                # The row-major vertical offset is a function of how wide the *entire* display is
                rm_horiz_offset = j
                rm_vert_offset = (i * (panel_width * panels_wide))
                rm_index = rm_root + rm_vert_offset + rm_horiz_offset

                strip_offset = (i * panel_width) + j
                mapping[rm_index] = strip_root + strip_offset 
    else:
        raise RuntimeError("Not yet implemented")

    return mapping

# Orientation gets the positioning of the first 3 LEDs of a panel. Reports back the corner and
# direction of the first few LEDs.
# 
# The corner is (0, 1, 2, 3) for (top left, top right, bottom left, bottom right). The orientation
# is either horizontal or vertical.
def ask_for_orientation(num_panels) -> Tuple[int, int, str]:
    valid_corners = [str(i) for i in range(4)]
    valid_directions = ["H", "V"]

    panel_index = -1
    while panel_index < 0:
        panel_str = input("Panel row-major index: ")
        if int(panel_str) >= num_panels:
            print(f"Input must be in range [0, {num_panels})")
        else:
            panel_index = int(panel_str)

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
            print("Direction must be H, V, or D")
        else:
            direction = direction_str

    return (panel_index, corner, direction)

def save_panel_config(name: str, panel_config: PanelConfig):
    path = os.path.join(STORE_PATH, name)

    if not os.path.exists(STORE_PATH):
        os.mkdir(STORE_PATH)

    with open(path, 'w+b') as f:
        pickle.dump(panel_config, f)
    
    print(f"Successfully saved map to {path}")
    return

def load_panel_config(name: str) -> PanelConfig:
    path = os.path.join(STORE_PATH, name)

    if os.path.exists(path):
        print(f"Found existing panel config at {path}")

        with open(path, 'rb') as f:
            loaded_panel_config = pickle.load(f)        
            return loaded_panel_config 
    
    print(f"Did not find existing map at {path}") 
    return None

def ensure_panel_config() -> PanelConfig:
    name = input("Name for calibration: ")
    loaded_panel_config = load_panel_config(name)

    if loaded_panel_config is None:
        horz_side_length = int(input("Panel width (number of LEDs): "))
        vert_side_length = int(input("Panel height (number of LEDs): "))
        horz_panels = int(input("Number of panels across: "))
        vert_panels = int(input("Number of panels high: "))

        mapping = create_map(horz_side_length, vert_side_length, horz_panels, vert_panels)

        loaded_panel_config = PanelConfig(horz_side_length, vert_side_length, horz_panels, vert_panels, mapping)
        save_panel_config(name, loaded_panel_config)

    return loaded_panel_config 

if __name__ == "__main__":
    # Basic test for get_map_from_orientation

    # First test: 1x2 panel display, each panel is 3x3. Both have oreintation (0, H).
    first_panel = get_map_from_orientation(strip_root=0, rm_root=0, panel_width=3, panel_height=3,
                                           panels_wide=2, panels_high=1, corner=0, direction="H")
    # Expected: { 0: 0, 1: 1, 2: 2, 8: 3, 7: 4, 6: 5, 12: 6, 13: 7, 14: 8}
    derive_rm_root(panel_index=0, panel_width=3, panel_height=3, panels_wide=2, panels_high=1)
    # Expected: 0

    second_panel = get_map_from_orientation(strip_root=9, rm_root=3, panel_width=3, panel_height=3,
                                           panels_wide=2, panels_high=1, corner=0, direction="H")
    # Expected: { 3: 9, 4: 10, 5: 11, 11: 12, 10: 13, 9: 14, 15: 15, 16: 16, 17: 17}
    derive_rm_root(panel_index=1, panel_width=3, panel_height=3, panels_wide=2, panels_high=1)
    # Expected: 3


    # Second test: stack the panels vertically (2 x 1)
    first_panel_2 = get_map_from_orientation(strip_root=0, rm_root=0, panel_width=3, panel_height=3,
                                           panels_wide=1, panels_high=2, corner=0, direction="H")
    # Expected: { 0: 0, 1: 1, 2: 2, 5: 3, 4: 4, 3: 5, 6: 6, 7: 7, 8: 8}
    derive_rm_root(panel_index=0, panel_width=3, panel_height=3, panels_wide=1, panels_high=2)
    # Expected: 0
    second_panel_2 = get_map_from_orientation(strip_root=9, rm_root=9, panel_width=3, panel_height=3,
                                           panels_wide=1, panels_high=2, corner=0, direction="H")
    # Expected: { 9: 9, 10: 10, 11: 11, 14: 12, 13: 13, 12: 14, 15: 15, 16: 16, 17: 17}
    derive_rm_root(panel_index=1, panel_width=3, panel_height=3, panels_wide=1, panels_high=2)
    # Expected: 9

    command = input("Inspect map or create new? [I/C]: ")
    if command == "I":
        name = input("Name of calibration: ")
        loaded_map = load_panel_config(name)
    elif command == "C":
        ensure_panel_config()
    else:
        print("Invalid command")