import unittest
from inferer import Inferer

class TestPanelCalibration(unittest.TestCase):
    def test_2_by_2(self):
        inferer = Inferer(2, 2, 2)

        # TODO(neil): All corners, counter-clockwise and clockwise
        top_left_clockwise = inferer.compute_panel_mapping(10, 11)
        self.assertDictEqual(top_left_clockwise, {0: 10, 1: 11, 2: 15, 3: 14})

# Assemble an in-memory calibration and call compute_mapping on it
# Create a calibration, make updates to it, read it back, and compute_mapping

if __name__ == '__main__':
    unittest.main()