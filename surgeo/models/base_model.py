import pathlib
import string

import pandas as pd


class BaseModel(object):

    def __init__(self):
        self._package_root = pathlib.Path(__file__).parents[1]
        # Add geocode df
        self._GEOCODE_DF = pd.read_csv(
            self._package_root / 'data' / 'population_2010.csv',
            index_col='zcta5'
        )
        # Convert geocode zip codes to strings
        self._GEOCODE_DF.index = (
            self._GEOCODE_DF.index
                            .astype('str')
                            .str
                            .zfill(5)
        )
        # Add surname df
        self._SURNAME_DF = pd.read_csv(
            self._package_root / 'data' / 'surname_2010.csv',
            index_col='name'
        )

    def _normalize_names(self, names: pd.Series) -> pd.Series:
        # Make a transalation table of unwanted characers
        unwanted_characters = (
            string.digits + 
            string.punctuation + 
            string.whitespace
        )
        translation_table =  str.maketrans('', '', unwanted_characters)
        # Run our string operations
        output = (
            names.astype(str)
                 .str.strip()
                 .str.upper()
                 .str.translate(translation_table)
                 .str.replace('\sJ\.*R\.*\s*$', '')
                 .str.replace('\sS\.*R\.*\s*$', '')
                 .str.replace('\sIII\s*$',      '')
                 .str.replace('\sIV\s*$',       '')
        )
        output.name = 'name'
        return output

    def _normalize_zctas(self, zcta: pd.Series) -> pd.Series:
        converted = pd.Series(zcta.values, dtype=str)
        zfilled = converted.str.zfill(5)
        zfilled.name = 'zcta5'
        return zfilled
