import unittest

import pandas as pd

from surgeo.models.surgeo_model import SurgeoModel


class TestSurgeoModel(unittest.TestCase):

    _SURGEO_MODEL = SurgeoModel()

    _INPUT_NAMES = pd.Series(['DIAZ', 'JOHNSON', 'WASHINGTON'])

    _INPUT_ZCTAS = pd.Series(['65201', '63144', '63110'])

    _SURGEO_WHITE_RESULT = pd.Series([0.264680, 0.872022, 0.014138])

    _SURNAME_PROBS_INPUT = pd.DataFrame({
        'name': ['VAN ROSSUM', 'THOMPSON', 'HOPPER'],
        'white': [.01, .02, .03], 
        'black': [.04, .05, .06], 
        'api': [.07, .08, .09]
    })

    _ZIP_PROBS_INPUT = pd.DataFrame({
        'zcta5': ['63110', '63144', '65201'],
        'white': [.11, .12, .13], 
        'black': [.14, .15, .16], 
        'api': [.17, .18, .19]
    })

    _COMBINED_PROBS_WHITE_RESULT = pd.Series([0.059140, 0.098765, 0.127451])    

    _GET_SURNAME_PROBS_WHITE_RESULT = pd.Series([0.0519, 0.5897, 0.0517])

    _GET_GEOCODE_PROBS_WHITE_RESULT = pd.Series([0.000163, 0.000039, 0.000045])

    def test_get_probabilities(self):
        """Test Surgeo model versus known result"""
        # Get probs
        result = self._SURGEO_MODEL.get_probabilities(
            self._INPUT_NAMES,
            self._INPUT_ZCTAS,
        )
        # Check probs with known values
        self.assertTrue(
            (result['white'].round(6) == self._SURGEO_WHITE_RESULT).all()
        )

    def test_combined_probs(self):
        """Test calculation of probabilities is done properly"""
        # Run Surgeo algorithm
        surgeo_probs = self._SURGEO_MODEL._combined_probs(
            self._SURNAME_PROBS_INPUT,
            self._ZIP_PROBS_INPUT,
        )
        # Check probs with known values
        self.assertTrue(
            (
                surgeo_probs['white'].round(6) == 
                self._COMBINED_PROBS_WHITE_RESULT
            ).all()
        )

    def test_get_surname_probs(self):
        """Test the surname probability fetching function"""
        result = self._SURGEO_MODEL._get_surname_probs(self._INPUT_NAMES)
        self.assertTrue(
            (
                result['white'].round(4) ==
                self._GET_SURNAME_PROBS_WHITE_RESULT
            ).all()
        )

    def test_get_geocode_probs(self):
        """Test the geocoding probability fetching function"""
        result = self._SURGEO_MODEL._get_geocode_probs(self._INPUT_ZCTAS)
        self.assertTrue(
            (
                result['white'].round(6) ==
                self._GET_GEOCODE_PROBS_WHITE_RESULT
            ).all()
        )


if __name__ == '__main__':
    unittest.main()
