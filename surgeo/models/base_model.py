import pathlib
import string

import numpy as np
import pandas as pd


class BaseModel(object):

    def __init__(self):
        self._package_root = pathlib.Path(__file__).parents[1]
        # Add geocode df
        self._GEOCODE_DF = pd.read_csv(
            self._package_root / 'data' / 'population_2010.csv',
            index_col='zcta5',
            na_values=[''],
            keep_default_na=False,
        )
        # Convert geocode zip codes to strings
        self._GEOCODE_DF.index = (
            self._GEOCODE_DF.index.astype('str')
                                  .str.zfill(5)
        )
        # Add surname df
        self._SURNAME_DF = pd.read_csv(
            self._package_root / 'data' / 'surname_2010.csv',
            index_col='name',
            na_values=[''],
            keep_default_na=False,
        )

    def _normalize_names(self, names: pd.Series) -> pd.Series:
        # Make a transalation table of unwanted characers
        unwanted_characters = (
            string.digits +
            string.punctuation +
            string.whitespace
        )
        translation_table =  str.maketrans('', '', unwanted_characters)
        # Run our string operations (remember NAN is a valid name)
        output = (
            names.fillna('')
                 .astype(str)
                 .str.translate(translation_table)
                 .str.upper()
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

    def _get_surname_probs(self, names: pd.Series) -> pd.DataFrame:
        normalized_names = (
            self._normalize_names(names)
                .to_frame()
        )
        surname_probs = normalized_names.merge(
            self._SURNAME_DF,
            left_on='name',
            right_index=True,
            how='left',
        )
        return surname_probs

    def _get_geocode_probs(self, zctas: pd.Series) -> pd.DataFrame:
        normalized_zctas = (
            self._normalize_zctas(zctas)
                .to_frame()
        )
        geocode_probs = normalized_zctas.merge(
            self._GEOCODE_DF,
            left_on='zcta5',
            right_index=True,
            how='left',
        )
        return geocode_probs
