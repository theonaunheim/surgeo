import unittest

import pandas as pd

from surgeo.models.base_model import BaseModel


class TestBaseModel(unittest.TestCase):

    _NORMALIZED_NAME_MAPPING = {
        'Davis Jr.'  : 'DAVIS',
        'Mapother IV': 'MAPOTHER',
        'P3T3RS0N'   : 'PTRSN',
        'D\'angelo'  : 'DANGELO',
        'DE SANTIS'  : 'DESANTIS',
    }

    _BASE_MODEL = BaseModel()

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get_prob_race_given_zcta(self):
        pass

    def test_normalize_surnames(self):
        # Generate series
        original = pd.Series(list(self._NORMALIZED_NAME_MAPPING.keys()))
        correct = pd.Series(list(self._NORMALIZED_NAME_MAPPING.values()))
        function_output = self._BASE_MODEL._normalize_names(original)
        # Zip and test correct string and function output.
        zip_object = zip(correct.values, function_output.values)
        for correct_output, function_output in zip_object:
            self.assertEqual(correct_output, function_output)


if __name__ == '__main__':
    unittest.main()