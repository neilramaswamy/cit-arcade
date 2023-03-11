import unittest
from inferer import Inferer
from calibrator import Calibrator
from schemas import Schema, SchemaDisplayConf, SchemaPanelConf

class TestPanelCalibration(unittest.TestCase):
    def test_2x2_panel_mapping(self):
        inferer = Inferer(2, 2, 2)

        top_left_clockwise = inferer.compute_panel_mapping(10, 11)
        self.assertDictEqual(top_left_clockwise, {0: 10, 1: 11, 2: 15, 3: 14})

        top_left_c_clockwise = inferer.compute_panel_mapping(10, 14)
        self.assertDictEqual(top_left_c_clockwise, {0: 10, 1: 14, 2: 15, 3: 11})

        bottom_right_clockwise = inferer.compute_panel_mapping(15, 14)
        self.assertDictEqual(bottom_right_clockwise, { 0: 15, 1: 14, 2: 10, 3: 11 })

    def test_2x2_mapping_from_schema(self):
        calibrator = Calibrator(2, 2, 2)

        # TODO(neil): The ordering of SchemaPanelConf is backwards... figure out why it's
        # alphabetized!
        calibration = Schema(SchemaDisplayConf(2, 2, 2), "2 by 2", [
            SchemaPanelConf(14, 15, 0),
            SchemaPanelConf(3, 7, 1),
            SchemaPanelConf(1, 5, 2),
            SchemaPanelConf(12, 8, 3),
        ])

        [got, got_inv] = calibrator.compute_mappings(calibration)
        expected = {
            0: 15,
            1: 14,
            2: 10,
            3: 11,
            4: 7,
            5: 3,
            6: 2,
            7: 6,
            8: 5,
            9: 1,
            10: 0,
            11: 4,
            12: 8,
            13: 12,
            14: 13,
            15: 9
        }

        self.assertDictEqual(got, expected)

        for k, v in got.items():
            self.assertEqual(k, got_inv.get(v))
        
        for k, v in got_inv.items():
            self.assertEqual(k, got.get(v))
    
# Assemble an in-memory calibration and call compute_mapping on it
# Create a calibration, make updates to it, read it back, and compute_mapping
class TestE2EPanelCalibration(unittest.TestCase):
    # Create a calibration, write to disk 
    # Read that back, pass it to the inferer, and make sure the inferred map is correct
    pass

if __name__ == '__main__':
    unittest.main()