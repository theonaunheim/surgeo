import pathlib
import unittest

import numpy as np
import pandas as pd

from surgeo.models.surname_model import SurnameModel


class TestSurnameModel(unittest.TestCase):

    _SURNAME_MODEL = SurnameModel()

    _DATA_FOLDER = pathlib.Path(__file__).resolve().parents[1] / 'data'

    def test_get_probabilities(self):
        """Test the main surname probability method"""
        # Get data and clean it
        input_data = pd.read_csv(
            self._DATA_FOLDER / 'surname_input.csv',
            skip_blank_lines=False,
        )
        # Get prob
        result = self._SURNAME_MODEL.get_probabilities(input_data['name'])
        # Get true result
        true_result = pd.read_csv(
            self._DATA_FOLDER / 'surname_output.csv',
        )
        # Clean for consistency
        result = result.round(4).fillna('')
        true_result = true_result.round(4).fillna('')
        # Check that all items in the series are equal
        self.assertTrue(
            result.equals(true_result)
        )

if __name__ == '__main__':
    unittest.main()
