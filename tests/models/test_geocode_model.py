import pathlib
import unittest

import numpy as np
import pandas as pd

from surgeo.models.geocode_model import GeocodeModel


class TestGeocodeModel(unittest.TestCase):

    _GEOCODE_MODEL = GeocodeModel()
    _GEOCODE_MODEL_TRACT = GeocodeModel(geo_level='TRACT')

    _DATA_FOLDER = pathlib.Path(__file__).resolve().parents[1] / 'data'

    def test_get_probabilities(self):
        """Test Geocode model versus known result"""
        # Get our data and clean it
        input_data = pd.read_csv(
            self._DATA_FOLDER / 'geocode_input.csv',
            skip_blank_lines=False,
        )
        # Get prob
        result = self._GEOCODE_MODEL.get_probabilities(input_data['zcta5'])
        # Get true result
        true_result = pd.read_csv(
            self._DATA_FOLDER / 'geocode_output.csv',
        )
        # Clean for consistency
        result = result.round(4).fillna('')
        true_result = true_result.round(4).fillna('')
        # Check that all items in the series are equal
        self.assertTrue(
            result.equals(true_result)
        )

    def test_get_probabilities_tract(self):
        """Test Geocode model versus known result with Tracts"""
        # Get our data and clean it
        input_data = pd.read_csv(
            self._DATA_FOLDER / 'tract_input.csv',
            skip_blank_lines=False,
        )
        # Get prob
        result = self._GEOCODE_MODEL_TRACT.get_probabilities_tract(input_data[['state','county','tract']])
        # Get true result
        true_result = pd.read_csv(
            self._DATA_FOLDER / 'tract_output.csv',             
        )
        # Clean for consistency
        result = result.round(4).fillna('')
        true_result = result.round(4).fillna('')
        # Check that all items in the series are equal
        self.assertTrue(
            result.equals(true_result)
        )

if __name__ == '__main__':
    unittest.main()
