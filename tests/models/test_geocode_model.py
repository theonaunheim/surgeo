import unittest

import numpy as np
import pandas as pd

from surgeo.models.geocode_model import GeocodeModel


class TestGeocodeModel(unittest.TestCase):

    _GEOCODE_MODEL = GeocodeModel()

    _GEOCODE_DATA = pd.Series([
        '63144',
        '631',
        ' 63110',
        'Will fail',
        np.NaN,
    ])

    _GEOCODE_WHITE_RESULT = pd.Series([
        0.861114,
        0.003240,
        0.518377,
        0.0,
        0.0
    ])

    def test_get_probabilities(self):
        """Test Geocode model versus known result"""
        # Get our data and clean it
        result = self._GEOCODE_MODEL.get_probabilities(self._GEOCODE_DATA)
        clean_result = result['white'].round(6).fillna(0.0)
        # Check that all items in the series are equal
        self.assertTrue(
            (clean_result == self._GEOCODE_WHITE_RESULT).all()
        )


if __name__ == '__main__':
    unittest.main()
