import pathlib
import unittest

import pandas as pd

from surgeo.models.surgeo_model import SurgeoModel


class TestSurgeoModel(unittest.TestCase):

    _SURGEO_MODEL = SurgeoModel()
    _SURGEO_MODEL_TRACT = SurgeoModel("TRACT")

    _DATA_FOLDER = pathlib.Path(__file__).resolve().parents[1] / 'data'

    def test_get_probabilities(self):
        """Test Surgeo model versus known result"""
        # Load data
        surname_data = pd.read_csv(
            self._DATA_FOLDER / 'surname_input.csv',
            skip_blank_lines=False,
        )
        geocode_data = pd.read_csv(
            self._DATA_FOLDER / 'geocode_input.csv',
            skip_blank_lines=False,
        )
        # Get probs
        result = self._SURGEO_MODEL.get_probabilities(
            surname_data['name'],
            geocode_data['zcta5'],
        )
        true_result = pd.read_csv(
            self._DATA_FOLDER / 'surgeo_output.csv'
        )
        # Clean for consistency
        result = result.round(4).fillna('')
        true_result = true_result.round(4).fillna('')
        # Check that all items in the series are equal
        self.assertTrue(
            result.equals(true_result)
        )

    def test_get_probabilities_tract(self):
        """Test Surgeo model versus known result"""
        # Load data
        surname_data = pd.read_csv(
            self._DATA_FOLDER / 'tract_input.csv',
            skip_blank_lines=False,
        )
        geocode_data = pd.read_csv(
            self._DATA_FOLDER / 'tract_input.csv',
            skip_blank_lines=False,
        )
        # Get probs
        result = self._SURGEO_MODEL_TRACT.get_probabilities(
            surname_data['name'],
            geocode_data,
        )
        true_result = pd.read_csv(
            self._DATA_FOLDER / 'surgeo_tract_output.csv'
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
