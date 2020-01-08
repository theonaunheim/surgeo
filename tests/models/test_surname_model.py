import unittest

import numpy as np
import pandas as pd

from surgeo.models.surname_model import SurnameModel


class TestSurnameModel(unittest.TestCase):

    _SURNAME_MODEL = SurnameModel()

    _SURNAME_DATA = pd.Series([
        'WILSON',
        'ROBINSON',
        'PEREZ',
        np.NaN,
    ])

    _SURNAME_WHITE_RESULT = pd.Series([
        0.6736,
        0.4870,
        0.0496,
        0.0000,
    ])

    def test_get_probabilities(self):
        """Test the main surname probability method"""
        # Get data and clean it
        result = self._SURNAME_MODEL.get_probabilities(
            self._SURNAME_DATA
        )
        round_result = result['white'].round(6).fillna(0.0)
        # Check that all items in the series are equal
        self.assertTrue(
            (round_result == self._SURNAME_WHITE_RESULT).all()
        )

if __name__ == '__main__':
    unittest.main()
