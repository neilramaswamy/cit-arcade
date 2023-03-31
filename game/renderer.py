from leds.mux import Color 
import numpy as np

# Consumes a 3D array of (rows, cols, pixel) and maps it onto the 1-dimensional pixel strip using
# the provided mapping.
def render_to_strip(strip, rm_pixels: np.ndarray, mapping: dict[int, int]):
    num_rows = len(rm_pixels)

    for i in range(num_rows):
        row = rm_pixels[i]
        num_cols = len(row)

        for j in range(num_cols):
            rm_index = (i * num_cols) + j

            if rm_index not in mapping:
                raise Exception(f"Index {rm_index} is not in mapping")
            else:
                strip_index = mapping[rm_index]

            pixel = rm_pixels[i][j]

            strip.setPixelColor(strip_index, Color(int(pixel[0]), int(pixel[1]), int(pixel[2])))
    strip.show()