import pathlib

import pandas as pd


class BaseModel(object):

    def __init__(self):
        self._package_root = pathlib.Path(__file__).parents[1]
        self._GEOCODE_DF = pd.read_csv(
            self._package_root /
            'data' /
            'geocode_2010.csv'
        )
        self._SURNAME_DF = pd.read_csv(
            self._package_root /
            'data' /
            'surname_2010.csv'
        )

    def _normalize_name(self):
        pass

    def _normalize_zcta(self):
        pass

