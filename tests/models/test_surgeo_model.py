import unittest

import pandas as pd

from surgeo.models.surgeo_model import SurgeoModel


class TestSurgeoModel(unittest.TestCase):

    _SURGEO_MODEL = SurgeoModel()

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get_probabilities(self):
        pass

if __name__ == '__main__':
    unittest.main()
