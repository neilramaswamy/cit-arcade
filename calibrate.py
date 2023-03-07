from enum import Enum

# Panel axes
ORIENTATION = Enum("ORIENTATION", "ABOVE BELOW LEFT RIGHT")

# A proof-of-concept for panel calibration
class Display:
    panel_length: int = 0
    display_width_panels: int = 0
    display_height_panels: int = 0

    # Derived properties (sugar)
    pixels_per_panel: int = 0
    display_pixel_width: int = 0
    display_pixel_height: int = 0

    # Maps pixels between their strip index and the row major index, where row-major starts at the
    # top-left and goes left-to-right, top-to-bottom (i.e. how arrays are stored in memory).
    strip_rm_map: dict[int, int] = {}

    def __init__(self, panel_length: int, display_width_panels: int, display_height_panels: int):
        self.panel_length = panel_length 
        self.display_width_panels = display_width_panels
        self.display_height_panels = display_height_panels

        self.pixels_per_panel = self.panel_length * self.panel_length
        self.display_pixel_width = self.display_width_panels * self.panel_length
        self.display_pixel_height = self.display_height_panels * self.panel_length

    # Returns the row-major index of the pixel at the given strip index, by prompting the user.
    # For now, the prompt is via the console, but this will be replaced with a GUI.
    def get_user_input(self, strip_index: int) -> int:
        index = input("Illuminating pixel at strip-index %d. Enter the row-major index: " % strip_index)
        return int(index)

    # Returns whether end_rm_index is above, below, to the left, or to the right of start_rm_index.
    def orientation(self, start_rm_index: int, end_rm_index: int) -> ORIENTATION:
        """
        Suppose we have the configuration below, where S is our start pixel, and we have two
        options for our end pixel, either Up or Right.

        U • •
        • • •
        S • R

        If we have U, notice that |S - U| = 6. Observe that |S - R| = (3 - 1). So, just by
        calculating the difference, we know that if (diff % 3) == 0, then our end pixel must be U.
        Otherwise, if diff == (3 - 1) our end pixel must be R.
        """
        if start_rm_index == end_rm_index:
            raise Exception(f"Start and end indices must differ; got both {start_rm_index}")

        diff = start_rm_index - end_rm_index
        abs_diff = abs(diff)   

        # Y is major
        if abs_diff % self.panel_length == 0:
            if diff > 0:
                return ORIENTATION.ABOVE
            else:
                return ORIENTATION.BELOW
        elif abs_diff == self.panel_length - 1:
            if diff > 0:
                return ORIENTATION.LEFT
            else:
                return ORIENTATION.RIGHT
        else:
            raise Exception(f"Invalid start and end indices of start {start_rm_index} and end {end_rm_index}")
    
    def get_direction_from_orientation(self, orientation: ORIENTATION) -> tuple[int, int]:
        if orientation == ORIENTATION.ABOVE:
            return -self.display_pixel_width
        elif orientation == ORIENTATION.BELOW:
            return self.display_pixel_width
        elif orientation == ORIENTATION.LEFT:
            return -1
        elif orientation == ORIENTATION.RIGHT:
            return 1
        else:
            raise Exception(f"Unknown orientation: {orientation}")


    def calibrate_panel(self, panel_index: int):
        # From strip-light index to row-major index
        mapping = {}


        first_light_strip_index = panel_index * self.pixels_per_panel 
        first_light_rm_index = self.get_user_input(first_light_strip_index)

        major_axis_end_strip_index = first_light_strip_index + (self.panel_length - 1)
        major_axis_end_rm_index = self.get_user_input(major_axis_end_strip_index)

        # Infer the major orientation and minor orientation
        major_orientation = self.orientation(first_light_rm_index, major_axis_end_rm_index)

        # We can infer the minor axis by seeing which side of the panel we're on, and using the
        # major axis
        minor_orientation = None
        
        if first_light_rm_index % self.pixels_per_panel == 0:
            # We're on the top-left of panel
            if major_orientation == ORIENTATION.RIGHT:
                minor_orientation = ORIENTATION.BELOW
            elif major_orientation == ORIENTATION.BELOW:
                minor_orientation = ORIENTATION.RIGHT
            else:
                raise Exception(f"Could not determine minor axis from top-left point {first_light_rm_index} and major {major_orientation}")
        elif first_light_rm_index % self.pixels_per_panel == self.panel_length - 1:
            # We're on the top-right of panel
            if major_orientation == ORIENTATION.LEFT:
                minor_orientation = ORIENTATION.BELOW
            elif major_orientation == ORIENTATION.BELOW:
                minor_orientation = ORIENTATION.LEFT
            else:
                raise Exception(f"Could not determine minor axis from top-right point {first_light_rm_index} and major {major_orientation}")
        elif first_light_rm_index % self.pixels_per_panel == (self.pixels_per_panel - self.panel_length):
            # We're on the bottom-left of panel
            if major_orientation == ORIENTATION.RIGHT:
                minor_orientation = ORIENTATION.ABOVE
            elif major_orientation == ORIENTATION.ABOVE:
                minor_orientation = ORIENTATION.RIGHT
            else:
                raise Exception(f"Could not determine minor axis from bottom-left point {first_light_rm_index} and major {major_orientation}")
        elif first_light_rm_index % self.pixels_per_panel == self.pixels_per_panel - 1:
            # We're on the bottom-right of the panel
            if major_orientation == ORIENTATION.LEFT:
                minor_orientation = ORIENTATION.ABOVE
            elif major_orientation == ORIENTATION.ABOVE:
                minor_orientation = ORIENTATION.LEFT
            else: 
                raise Exception(f"Could not determine minor axis from bottom-right point {first_light_rm_index} and major {major_orientation}")
        else:
            raise Exception(f"Could not infer minor axis: invalid first light index: {first_light_rm_index}")


        # We use the major and minor orientations to determine how to layout the panel
        major_direction = self.get_direction_from_orientation(major_orientation)
        minor_direction = self.get_direction_from_orientation(minor_orientation)

        print(f"Major direction is {major_direction} and minor direction is {minor_direction}")

        for minor_idx in range(self.panel_length):
            for major_idx in range(self.panel_length):
                strip_offset = (minor_idx * self.panel_length) + major_idx

                # Even row, we go in the direction of major_direction
                if minor_idx % 2 == 0:
                    major_offset = major_idx * major_direction
                else:
                    # Compute from the other side of the panel
                    major_offset = (self.panel_length - major_idx - 1) * major_direction

                minor_offset = minor_idx * minor_direction

                mapping[strip_offset] = first_light_rm_index + major_offset + minor_offset

        return mapping    
    
    def do_calibrate(self):
        for i in range(self.display_width_panels * self.display_height_panels):
            print(self.calibrate_panel(i))

if __name__ == "__main__":
    d = Display(2, 2, 2)
    d.do_calibrate()