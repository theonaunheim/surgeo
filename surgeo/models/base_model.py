"""Containins the base model for Surname, Geocode, and Surgeo models."""

import pathlib
import string

import numpy as np
import pandas as pd


class BaseModel(object):
    """Base class for the surname, geocode, and surname-geocode models.

    Class creation is greatly simplified by placing most of the
    funcionality wihtin a single base class and leaving only small areas
    of responsibility for the subclass. This base class does the following
    operations:

    1. Creating geocode and surname lookup dataframes upon instantiation;
    2. Houseing normalization routines for dirty ZIP code and surname data;
    3. Getting probabilities for a set of ZIPs or surnames by joining the
    input data with the aforementioned lookup frames.

    Note
    ----
    Surnames are normalized in a manner consistent with Word et. al (2007),
    below. This includes removing all whitespace/punctuation/digits,
    making the strings upper case, and then removing elements such as
    "JR", "SR", "IV" from the tail of the string. AN example would be
    "Dav 3idson" being translated to "DAVIDSON".

    ZCTAs, which serve as a proxy for ZIP codes, are normalized by simply
    translating them to stirngs and then .zfill()ing them. An example would
    be "531" to "00531".

    References
    ----------
    .. [1] Word, David L., Charles D. Coleman, Robert Nunziata and Robert 
    Kominski.  2007.  "Demographic Aspects of Surnames from Census 2000".   
    http://www2.census.gov/topics/genealogy/2000surnames/surnames.pdf.  
    
    """

    def __init__(self):
        self._package_root = pathlib.Path(__file__).parents[1]
        # Attach geocode data as a dataframe for lookups
        self._GEOCODE_DF = pd.read_csv(
            self._package_root / 'data' / 'population_2010.csv',
            index_col='zcta5',
            na_values=[''],
            keep_default_na=False,
        )
        # Convert geocode zip codes to 00000-formatted strings
        self._GEOCODE_DF.index = (
            self._GEOCODE_DF.index.astype('str')
                                  .str.zfill(5)
        )
        # Attach surname df (beware ... some NA values like "NAN" are names)
        self._SURNAME_DF = pd.read_csv(
            self._package_root / 'data' / 'surname_2010.csv',
            index_col='name',
            na_values=[''],
            keep_default_na=False,
        )

    def _normalize_names(self, names: pd.Series) -> pd.Series:
        """Take names and run a normalization routine"""
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

    def get_probabilities(self, *args):
        """Main method for subclasses to implement"""
        raise NotImplementedError('This class is not intended for direct use.')
