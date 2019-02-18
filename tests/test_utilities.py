import pathlib
import sys
import unittest

import pandas as pd


class UtilityFunctions(unittest.TestCase):
    '''Utility functions include functions that don't fit elsewhere.'''

    def setUp(self):
        '''Add surgeo to path and other operations.'''

        # Add surgeo module to path.
        self.module_path = pathlib.Path(__file__)
        self.top_level_path = self.module_path.parent.parent
        sys.path.append(str(self.top_level_path))

    def tearDown(self):
        '''Remove from path and other random operations.'''
        
        # Remove surgeo module from path.
        sys.path.remove(str(self.top_level_path))

    def test_normalize_surnames(self):
        '''This function transforms surnames based on a series of rules.'''

        # Import function to test
        from surgeo.utilities import normalize_surnames

        # Setup mapping
        NORMALIZED_MAPPING = {
            'Davis Jr.'  : 'DAVIS',
            'Mapother IV': 'MAPOTHER',
            'P3T3RS0N'   : 'PTRSN',
            'D\'angelo'  : 'DANGELO',
            'DE SANTIS'  : 'DESANTIS',
        }

        # Generate series
        original        = pd.Series(list(NORMALIZED_MAPPING.keys()))
        correct         = pd.Series(list(NORMALIZED_MAPPING.values()))
        function_output = normalize_surnames(original)

        # Zip and test correct string and function output.
        zip_object = zip(correct.values, function_output.values)
        for correct_output, function_output in zip_object:
            self.assertEqual(correct_output, function_output)


if __name__ == '__main__':
    unittest.main()