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

    1. Creating functions to provide lookup dataframes; and,
    2. Houseing normalization routines for dirty ZIP code and surname data.

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
    1.  Word, David L., Charles D. Coleman, Robert Nunziata and Robert 
        Kominski. 2007. Demographic Aspects of Surnames from Census 2000.   
        `<http://www2.census.gov/topics/genealogy/2000surnames/surnames.pdf>`_.  

    """

    def __init__(self):
        self._package_root = pathlib.Path(__file__).parents[1]

    def _get_prob_race_given_zcta(self):
        """Create dataframe of race probs given ZCTA (for Geo)"""
        prob_race_given_zcta = pd.read_csv(
            self._package_root / 'data' / 'prob_race_given_zcta_2010.csv',
            index_col='zcta5',
            na_values=[''],
            keep_default_na=False,
        )
        # Convert geocode zip codes to 00000-formatted strings
        prob_race_given_zcta.index = (
            prob_race_given_zcta.index.astype('str')
                                .str.zfill(5)
        )
        return prob_race_given_zcta

    def _get_prob_zcta_given_race(self):
        """Create dataframe of ZCTA ratios given a race (for SurGeo)"""
        prob_zcta_given_race = pd.read_csv(
            self._package_root / 'data' / 'prob_zcta_given_race_2010.csv',
            index_col='zcta5',
            na_values=[''],
            keep_default_na=False,
        )
        # Convert geocode zip codes to 00000-formatted strings
        prob_zcta_given_race.index = (
            prob_zcta_given_race.index.astype('str')
                                .str.zfill(5)
        )
        return prob_zcta_given_race

    def _get_prob_race_given_surname(self):
        """Create dataframe of race probabilities given surnames (for Sur)"""
        # Create surname df (beware ... some NA values like "NAN" are names)
        prob_race_given_surname = pd.read_csv(
            self._package_root / 'data' / 'prob_race_given_surname_2010.csv',
            index_col='name',
            na_values=[''],
            keep_default_na=False,
        )
        return prob_race_given_surname

    def _normalize_names(self, names: pd.Series) -> pd.Series:
        """Take names and run a normalization routine"""
        # Make a transalation table of unwanted characers
        unwanted_characters = (
            string.digits +
            string.punctuation +
            string.whitespace
        )
        # Remove unwanted characters efficiently
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
        """Transform ZCTAs into standardized strings"""
        converted = pd.Series(zcta.values, dtype=str)
        zfilled = converted.str.zfill(5)
        zfilled.name = 'zcta5'
        return zfilled
