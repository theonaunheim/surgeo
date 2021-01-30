import unittest

import pandas as pd

from surgeo.models.base_model import BaseModel


class TestBaseModel(unittest.TestCase):

    _NORMALIZED_NAME_MAPPING = {
        'Davis Jr. '  : 'DAVIS',
        ' Mapother IV': 'MAPOTHER',
        'P3T3RS0N '   : 'PTRSN',
        ' D\'angelo'  : 'DANGELO',
        'DE SANTIS '  : 'DESANTIS',
    }

    _NORMALIZED_ZCTA_MAPPING = {
        63144   : '63144',
        631     : '00631',
        '65201' : '65201',
        ' 63110': '63110',
    }

    _BASE_MODEL = BaseModel()

    _ZCTA_DF_LENGTH = 33_120

    _SURNAME_DF_LENGTH = 162_254

    def test_get_prob_race_given_zcta(self):
        """Check function returns appropriate race given ZCTA df"""
        # Test return type and length
        df = self._BASE_MODEL._get_prob_race_given_zcta()
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(len(df), self._ZCTA_DF_LENGTH)

    def test_get_prob_zcta_given_race(self):
        """Check function returns appropriate ZCTA given race df"""
        # Test return type and length
        df = self._BASE_MODEL._get_prob_zcta_given_race()
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(len(df), self._ZCTA_DF_LENGTH)

    def test_get_prob_race_given_surname(self):
        """Check function returns appropriate race given surname df"""
        # Test return type and length
        df = self._BASE_MODEL._get_prob_race_given_surname()
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(len(df), self._SURNAME_DF_LENGTH)

    def test_normalize_names(self):
        """Test string normalization routines for names"""
        # Generate series
        original = pd.Series(list(self._NORMALIZED_NAME_MAPPING.keys()))
        correct = pd.Series(list(self._NORMALIZED_NAME_MAPPING.values()))
        function_output = self._BASE_MODEL._normalize_names(original)
        # Zip and test correct string and function output.
        zip_object = zip(correct.values, function_output.values)
        for correct_output, function_output in zip_object:
            self.assertEqual(correct_output, function_output)

    def test_normalize_zctas(self):
        """Test string normalization routines for ZCTAs"""
        # Generate series
        original = pd.Series(list(self._NORMALIZED_ZCTA_MAPPING.keys()))
        correct = pd.Series(list(self._NORMALIZED_ZCTA_MAPPING.values()))
        function_output = self._BASE_MODEL._normalize_zctas(original)
        # Zip and test correct string and function output.
        zip_object = zip(correct.values, function_output.values)
        for correct_output, function_output in zip_object:
            self.assertEqual(correct_output, function_output)


if __name__ == '__main__':
    unittest.main()
