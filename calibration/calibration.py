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
    

    # Reads the configuration file from disk and synchronously writes the configuration data to
    # disk.
    def record_panel_configuration(self, config_name: str, panel_i: int, first_major_start_rm: int, first_major_end_rm: int):
        pass

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
    
    
    # Given an orientation on the current display, figures out the row-major "stride" that we need
    # to take to move in that direction.
    def get_stride_from_orientation(self, orientation: ORIENTATION) -> int:
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

    # Infers the minor axis of a panel given the row-major index of the first (strip-wise) light of
    # the panel. Uses the major axis to know to go the "other" way.
    def infer_minor_axis(self, first_light_rm_index: int, major_orientation: ORIENTATION) -> ORIENTATION:
        is_left_columnn = first_light_rm_index % self.panel_length == 0
        is_first_row = (first_light_rm_index % (self.pixels_per_panel * self.display_width_panels)) < self.display_pixel_width

        is_top_left = is_first_row and is_left_columnn
        is_top_right = is_first_row and not is_left_columnn
        is_bottom_left = not is_first_row and is_left_columnn
        is_bottom_right = not is_first_row and not is_left_columnn

        if is_top_left:
            if major_orientation == ORIENTATION.RIGHT:
                return ORIENTATION.BELOW
            elif major_orientation == ORIENTATION.BELOW:
                return ORIENTATION.RIGHT
            else:
                raise Exception(f"Could not determine minor axis from top-left point {first_light_rm_index} and major {major_orientation}")
        elif is_top_right:
            if major_orientation == ORIENTATION.LEFT:
                return ORIENTATION.BELOW
            elif major_orientation == ORIENTATION.BELOW:
                return ORIENTATION.LEFT
            else:
                raise Exception(f"Could not determine minor axis from top-right point {first_light_rm_index} and major {major_orientation}")
        elif is_bottom_left:
            if major_orientation == ORIENTATION.RIGHT:
                return ORIENTATION.ABOVE
            elif major_orientation == ORIENTATION.ABOVE:
                return ORIENTATION.RIGHT
            else:
                raise Exception(f"Couldn't infer minor axis from bottom-left point {first_light_rm_index} and major {major_orientation}")
        elif is_bottom_right:
            if major_orientation == ORIENTATION.LEFT:
                return ORIENTATION.ABOVE
            elif major_orientation == ORIENTATION.ABOVE:
                return ORIENTATION.LEFT
            else: 
                raise Exception(f"Could not determine minor axis from bottom-right point {first_light_rm_index} and major {major_orientation}")
        else:
            raise Exception(f"Could not infer minor axis: invalid first light index: {first_light_rm_index}")

    def calibrate_panel(self, first_major_start_rm: int, first_major_end_rm: int):
        # From strip-light index to row-major index
        mapping = {}

        # Figure out the major orientation and minor orientation
        major_orientation = self.orientation(first_major_start_rm, first_major_end_rm)
        minor_orientation = self.infer_minor_axis(first_major_start_rm, major_orientation)

        major_stride = self.get_stride_from_orientation(major_orientation)
        minor_stride = self.get_stride_from_orientation(minor_orientation)

        for minor_idx in range(self.panel_length):
            for major_idx in range(self.panel_length):
                # For an even row, we go in the direction of major_stride
                if minor_idx % 2 == 0:
                    major_offset = major_idx * major_stride
                else:
                    # For an odd row, we compute from the other side of the panel
                    major_offset = (self.panel_length - major_idx - 1) * major_stride

                minor_offset = minor_idx * minor_stride

                strip_offset = (minor_idx * self.panel_length) + major_idx
                mapping[strip_offset] = first_major_start_rm + major_offset + minor_offset

        return mapping    


    # Main sequence of events:
    #
    # while (get next panel to calibrate):
    #   using received strip index, prompt user 
    #   get back user input and store it

    # When starting a display, you can use a stored calibration
    # Then, the mapping is calculated
