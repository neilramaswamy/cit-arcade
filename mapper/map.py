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
    num_leds_per_panel = (panel_width * panel_height)
    num_leds = num_leds_per_panel * num_panels

    # Zero all the colors
    for i in range(num_leds-1):
        strip.setPixelColor(i, Color(0, 255, 255))
    strip.show()

    for i in range(num_panels):
        strip_root = i * num_leds_per_panel 

        # Determine the corner and direction
        if config.get('is_dev'):
            (panel_index, corner, direction) = (i, 0, "D")
        else:
            print(f"Going to illuminate pixel starting at {strip_root}")
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
    elif corner == 3 and direction == "H":
        for i in range(panel_height):
            for j in range(panel_width):
                # When i == 0, we're at the bottom, going right to left
                # When i % 2 == 1, we're going to left to right
                if i % 2 == 0:
                    # Going right to left
                    horiz_offset = ((panel_width - 1) - j)
                else:
                    horiz_offset = j
            
                rm_vert_offset = ((panel_height - 1)  - i) * (panel_width * panels_wide)
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

    # ================================
    # Bottom-right horizontal snaking
    # Two panels stacked vertically
    # ================================
    derive_rm_root(panel_index=0, panel_width=3, panel_height=4, panels_wide=1, panels_high=2)

    # {9: 12, 10: 13, 11: 14, 8: 15, 7: 16, 6: 17, 3: 18, 4: 19, 5: 20, 2: 21, 1: 22, 0: 23}
    br_h_first_panel = get_map_from_orientation(strip_root=12, rm_root=0, panel_width=3, panel_height=4,
                                            panels_wide=1, panels_high=2, corner=3, direction="H")
    # {21: 0, 22: 1, 23: 2, 20: 3, 19: 4, 18: 5, 15: 6, 16: 7, 17: 8, 14: 9, 13: 10, 12: 11}
    br_h_second_panel = get_map_from_orientation(strip_root=0, rm_root=12, panel_width=3, panel_height=4,
                                            panels_wide=1, panels_high=2, corner=3, direction="H")

    # ==================================
    # Bottom-right horizontal snaking
    # Two panels side-by-side: bottom 
    #
    # In this diagram, S means start, and E means end.
    # The numbers in the grid are how the panels are
    # wired together.
    #
    #  ______ ______
    # |    ->|->    |
    # |  1   |    2 |
    # |____<-|<-____|
    # |    ->|->    |
    # |  0   |    3 |
    # |____<-|<-____|
    #
    #
    # ==================================
    
    grid_0_rm_root = derive_rm_root(panel_index=2, panel_width=3, panel_height=4, panels_wide=2, panels_high=2)
    grid_1_rm_root = derive_rm_root(panel_index=0, panel_width=3, panel_height=4, panels_wide=2, panels_high=2)
    grid_2_rm_root = derive_rm_root(panel_index=1, panel_width=3, panel_height=4, panels_wide=2, panels_high=2)
    grid_3_rm_root = derive_rm_root(panel_index=3, panel_width=3, panel_height=4, panels_wide=2, panels_high=2)

    # {44: 0, 43: 1, 42: 2, 36: 3, 37: 4, 38: 5, 32: 6, 31: 7, 30: 8, 24: 9, 25: 10, 26: 11}
    grid_panel_0 = get_map_from_orientation(strip_root=0, rm_root=grid_0_rm_root, panel_width=3, panel_height=4, 
                                            panels_wide=2, panels_high=2, corner=3, direction="H")
    # {20: 12, 19: 13, 18: 14, 12: 15, 13: 16, 14: 17, 8: 18, 7: 19, 6: 20, 0: 21, 1: 22, 2: 23}
    grid_panel_1 = get_map_from_orientation(strip_root=12, rm_root=grid_1_rm_root, panel_width=3, panel_height=4,
                                            panels_wide=2, panels_high=2, corner=3, direction="H")
    # {3: 24, 4: 25, 5: 26, 11: 27, 10: 28, 9: 29, 15: 30, 16: 31, 17: 32, 23: 33, 22: 34, 21: 35}
    grid_panel_2 = get_map_from_orientation(strip_root=24, rm_root=grid_2_rm_root, panel_width=3, panel_height=4,
                                            panels_wide=2, panels_high=2, corner=0, direction="H")
    # {27: 36, 28: 37, 29: 38, 35: 39, 34: 40, 33: 41, 39: 42, 40: 43, 41: 44, 47: 45, 46: 46, 45: 47}
    grid_panel_3 = get_map_from_orientation(strip_root=36, rm_root=grid_3_rm_root, panel_width=3, panel_height=4,
                                            panels_wide=2, panels_high=2, corner=0, direction="H")

    command = input("Inspect map or create new? [I/C]: ")
    if command == "I":
        name = input("Name of calibration: ")
        loaded_map = load_panel_config(name)
    elif command == "C":
        ensure_panel_config()
    else:
        print("Invalid command")
