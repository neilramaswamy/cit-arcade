from enum import Enum
from schemas import Schema, SchemaDisplayConf, SchemaPanelConf
from inferer import Inferer
from config.config import CALIBRATION_SAVE_PATH
import os

# A proof-of-concept for panel calibration
# Someone (with the ability to render pixels), should interface with this function to write/read
# calibration details.
#                                |---> inferer
# someone else -----> calibrator |
#                                |---> disk writer
class Calibrator:
    def __init__(
            self,
            panel_length: int,
            display_width_panels: int,
            display_height_panels: int,
            save_path = CALIBRATION_SAVE_PATH):
        self.panel_length = panel_length
        self.display_width_panels = display_width_panels
        self.display_height_panels = display_height_panels

        self.save_path = os.path.expanduser(save_path)

        self.inferer = Inferer(panel_length, display_width_panels, display_height_panels)
    
    # From the given calibration, computes two mapping:
    #   1. Row-major index to strip-wise index
    #   2. Strip-wise index to row-major index
    # The maps are just inverses of each other.
    def compute_mappings(self, calibration: Schema) -> tuple[dict, dict]:
        # For each panel from the calibration, call the inferer
        strip_to_rm: dict[int, int] = {}

        for panel_conf in calibration.panel_conf:
            first_major_start_rm = panel_conf.first_major_start_rm
            first_major_end_rm =  panel_conf.first_major_end_rm

            panel_map = self.inferer.compute_panel_mapping(first_major_start_rm, first_major_end_rm)

            strip_offset = panel_conf.panel_index * (self.panel_length ** 2)

            for panel_strip_idx, rm_idx in panel_map.items():
                strip_to_rm[strip_offset + panel_strip_idx] = rm_idx

        rm_to_strip = {v: k for k, v in strip_to_rm.items()}
        return (strip_to_rm, rm_to_strip)

    def list_calibrations(self) -> list[Schema]:
        files = os.listdir(self.save_path)
        schemas = []

        for filename in files:
            with open(filename, "r") as file:
                schemas.append(Schema.from_json_data(file.read()))

        return schemas

    def add_calibration(self, name: str) -> Schema:
        pass

    # Should be able to edit a calibration
    def edit_calibration(self, name: str):
        pass

    def remove_calibration(self, name: str):
        filepath = os.path.join(self.save_path, name)

        if os.path.exists(filepath):
            os.unlink(filepath)


    # Returns the row-major index of the pixel at the given strip index, by prompting the user.
    # For now, the prompt is via the console, but this will be replaced with a GUI.
    def get_user_input(self, strip_index: int) -> int:
        index = input("Illuminating pixel at strip-index %d. Enter the row-major index: " % strip_index)
        return int(index)
