import unittest

import pandas as pd

from surgeo.models.base_model import BaseModel


class UtilityFunctions(unittest.TestCase):
    '''Utility functions include functions that don't fit elsewhere.'''

    def setUp(self):
        '''Add surgeo to path and other operations.'''
        pass

    def tearDown(self):
        '''Remove from path and other random operations.'''
        pass

    def test_normalize_surnames(self):
        '''This function transforms surnames based on a series of rules.'''

        # Import function to test

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