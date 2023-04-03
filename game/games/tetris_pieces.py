import numpy as np

# Pieces
S = [['.....',
      '.....',
      '..00.',
      '.00..',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

# Replaces the inner "lists of strings" (above) with "5x5 boolean arrays"
SHAPES = [S, Z, I, O, J, L, T]
SHAPES = [[np.array([[(letter == '0') for letter in list(line)] for line in orientation]) for orientation in shape] for shape in SHAPES]

# Pre-compute offsets for all the positions, relative to center-bottom
SHAPE_OFFSETS = [[np.flip(np.transpose(np.nonzero(bool_array))) + np.array([-2, -4]) for bool_array in shape] for shape in SHAPES]

# Hard-coded colors per shape
SHAPE_COLORS = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]

# Save number of shapes
NUM_SHAPES = len(SHAPES)
assert(len(SHAPES) == len(SHAPE_COLORS))

class TetrisPiece:
    def __init__(self, x, y, shape_index):
        # Pivot point located at center-bottom of 5x5 array
        self.x = x
        self.y = y
        self.shape_index = shape_index
        self.rotation = 0

    def get_color(self):
        return SHAPE_COLORS[self.shape_index]
    
    def get_offsets(self):
        return SHAPE_OFFSETS[self.shape_index][self.rotation % len(SHAPE_OFFSETS[self.shape_index])].copy()

    def get_positions(self):
        return self.get_offsets() + np.array([self.x, self.y])
