import pathlib
import unittest

import numpy as np
import pandas as pd

from surgeo.models.first_name_model import FirstNameModel


class TestFirstNameModel(unittest.TestCase):

    _FIRST_NAME_MODEL = FirstNameModel()

    _DATA_FOLDER = pathlib.Path(__file__).resolve().parents[1] / 'data'

    def test_get_probabilities(self):
        """Test the main first name probability method"""
        # Get data and clean it
        input_data = pd.read_csv(
            self._DATA_FOLDER / 'first_name_input.csv',
            skip_blank_lines=False,
        )
        # Get prob
        result = self._FIRST_NAME_MODEL.get_probabilities(input_data['first_name'])
        # Get true result
        true_result = pd.read_csv(
            self._DATA_FOLDER / 'first_name_output.csv',
        )
        # Clean for consistency
        result = result.round(4).fillna('')
        true_result = true_result.round(4).fillna('')
        # Check that all items in the series are equal
        pd.testing.assert_frame_equal(result, true_result)

if __name__ == '__main__':
    unittest.main()
