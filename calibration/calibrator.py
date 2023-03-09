from enum import Enum
from schemas import Schema, SchemaDisplayConf, SchemaPanelConf
from inferer import Inferer

# A proof-of-concept for panel calibration
# Someone (with the ability to render pixels), should interface with this function to write/read
# calibration details.
#                                |---> inferer
# someone else -----> calibrator |
#                                |---> disk writer
class Calibrator:
    def __init__(self, panel_length: int, display_width_panels: int, display_height_panels: int):
        self.panel_length = panel_length
        self.display_width_panels = display_width_panels
        self.display_height_panels = display_height_panels

        self.inferer = Inferer(panel_length, display_width_panels, display_height_panels)
    
    # From the given calibration, computes two mapping:
    #   1. Row-major index to strip-wise index
    #   2. Strip-wise index to row-major index
    # The maps are just inverses of each other.
    def compute_mappings(self, calibration: Schema) -> tuple[dict, dict]:
        # For each panel from the calibration, call the inferer
        pass

    # TODO(neil): List calibrations, get calibrations, get details for one calibration

    # Returns the row-major index of the pixel at the given strip index, by prompting the user.
    # For now, the prompt is via the console, but this will be replaced with a GUI.
    def get_user_input(self, strip_index: int) -> int:
        index = input("Illuminating pixel at strip-index %d. Enter the row-major index: " % strip_index)
        return int(index)
