import unittest
from calibration import Display

class TestPanelCalibration(unittest.TestCase):
    def test_2_by_2(self):
        d = Display(2, 2, 2)

        # TODO: All corners, counter-clockwise and clockwise
        top_left_clockwise = d.calibrate_panel(10, 11)
        self.assertDictEqual(top_left_clockwise, {0: 10, 1: 11, 2: 15, 3: 14})

if __name__ == '__main__':
    unittest.main()