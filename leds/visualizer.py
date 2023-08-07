import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.collections as collections
import numpy as np
import time

class Visualizer:
    def __init__(self, horz_side_length, vert_side_length, horz_panels, vert_panels):
        
        self.fig = None
        
        # Init hardcoded image and its hardcoded parameters
        self.img = plt.imread("leds/cit.png")
        self.grid_tl = np.array([49, 212])
        self.grid_br = np.array([744, 914])
        self.grid_gap = 14
        self.pixel_circle_max_fill_proportion = 0.9

        # Derive values from the above
        self.sub_grid_tls, self.sub_grid_wh = getSubGrid(
            horz_panels,
            vert_panels,
            self.grid_tl,
            self.grid_br,
            self.grid_gap)
        self.pixel_xys = getPixelXYs(
            horz_side_length,
            vert_side_length,
            self.sub_grid_tls,
            self.sub_grid_wh)
        self.pixel_radius = np.min(
            self.pixel_circle_max_fill_proportion / 2 *
            np.divide(self.sub_grid_wh, (horz_side_length, vert_side_length)))
        
    def displayColors(self, colors):
        
        if self.fig == None:
            plt.ion()
            plt.show()
            self.fig, self.ax = plt.subplots()
            self.ax.imshow(self.img)

            # Set up squares
            squares_list = [patches.Rectangle(tl, self.sub_grid_wh[0], self.sub_grid_wh[1]) for tl in self.sub_grid_tls]
            self.squares_coll = collections.PatchCollection(squares_list, facecolors='#888', zorder=1)
            squares = self.ax.add_collection(self.squares_coll)

            # Set up circles
            circles_list = [patches.Circle(xy, self.pixel_radius) for xy in self.pixel_xys]
            self.circles_coll = collections.PatchCollection(circles_list, facecolors=colors, zorder=2)
            circles = self.ax.add_collection(self.circles_coll)

        # Update colors
        self.circles_coll.set_facecolors(colors)

        # Required to give plt chance to update display;
        # See https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.pause.html
        plt.pause(0.01)


# Helper functions

def getSubGrid(h_panels, v_panels, grid_tl, grid_br, grid_gap):
    """
    Let n = h_panels * v_panels
    Returns:
    sub_grid_tls - an array of shape (n, 2), the top-left positions of each sub-grid
    sub_grid_wh  - an array of shape (2),    the (width, height) of each sub-grid     
    """

    grid_wh = grid_br - grid_tl

    sub_grid_wh = np.divide(grid_wh + grid_gap, (h_panels, v_panels)) - grid_gap

    xv, yv = np.meshgrid(
        np.linspace(0, 1, h_panels),
        np.linspace(0, 1, v_panels))
    sub_grid_tls = np.dstack((xv,yv)) * (grid_wh - sub_grid_wh) + grid_tl
    sub_grid_tls = sub_grid_tls.reshape(-1, 2)

    return sub_grid_tls, sub_grid_wh

def getPixelXYs(horz_side_length, vert_side_length, sub_grid_tls, sub_grid_wh):
    
    pixel_spacing = sub_grid_wh / (horz_side_length, vert_side_length)
    
    # For one panel
    xv, yv = np.meshgrid(
        np.linspace(0, 1, horz_side_length + 1)[:-1],
        np.linspace(0, 1, vert_side_length + 1)[:-1])
    panel_pixel_xys = np.dstack((xv,yv)) * sub_grid_wh + pixel_spacing / 2

    # For all panels
    pixel_xys = np.array([panel_pixel_xys + tl for tl in sub_grid_tls]).reshape(-1, 2)

    return pixel_xys
 
if __name__ == "__main__":
    
    horz_side_length = 9
    vert_side_length = 10
    horz_panels = 4
    vert_panels = 4

    visualizer = Visualizer(horz_side_length, vert_side_length, horz_panels, vert_panels)

    num_pixels = horz_side_length * vert_side_length * horz_panels * vert_panels

    # input("Press [enter] to show first set of random colors.")
    while True:
        print("Displaying random colors.")
        visualizer.displayColors(np.random.random((num_pixels, 3)))
        time.sleep(1)
