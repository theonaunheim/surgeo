import pathlib
import unittest

import pandas as pd

from surgeo.models.bifsg_model import BIFSGModel


class TestSurgeoModel(unittest.TestCase):

    _BIFSG_MODEL = BIFSGModel()

    _DATA_FOLDER = pathlib.Path(__file__).resolve().parents[1] / 'data'

    def test_get_probabilities(self):
        """Test BIFSG model versus known result"""
        # Load data
        surname_data = pd.read_csv(
            self._DATA_FOLDER / 'surname_input.csv',
            skip_blank_lines=False,
        )
        first_name_data = pd.read_csv(
            self._DATA_FOLDER / 'first_name_input.csv',
            skip_blank_lines=False,
        )
        geocode_data = pd.read_csv(
            self._DATA_FOLDER / 'geocode_input.csv',
            skip_blank_lines=False,
        )
        # Get probs
        result = self._BIFSG_MODEL.get_probabilities(
            first_name_data['first_name'],
            surname_data['name'],
            geocode_data['zcta5'],
        )
        true_result = pd.read_csv(
            self._DATA_FOLDER / 'bifsg_output.csv'
        )
        # Clean for consistency
        result = result.round(4).fillna('')
        true_result = true_result.round(4).fillna('')
        # Check that all items in the series are equal
        pd.testing.assert_frame_equal(result, true_result)


if __name__ == '__main__':
    unittest.main()
