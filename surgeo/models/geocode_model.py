"""This module contains the GeocodeModel class"""

import pandas as pd

from surgeo.models.base_model import BaseModel


class GeocodeModel(BaseModel):
    """Provides a way to look up race percentages by ZIP/ZCTA code

    This class uses a get_probabilities() method to provide a simple
    mechanism for obtaining race data. It is created using a simple join
    of a race data table and the ZIPs/ZCTAs that are input.

    Notes
    -----
    ZIP Code Tabulation Areas (ZCTAs) are approximations for US Postal ZIP
    codes. While ZIP codes change, ZCTAs are static for a given census
    cycle. They are not identical.

    The manner in which the geography data file was created can be found in
    the "fetch_geography" Jupyter notebook.

    This does not use the same Geocode data as the Surgeo class. This model
    uses the `prob_race_given_zcta_2010.csv` file, which has the race
    percentages for a given ZCTA (e.g. 90% of ZCTA 63144 is White). The
    SurgeoModel uses the `prob_zcta_given_race_2010.csv` file, which has
    the percentage of a particular race that falls within that ZCTA (e.g.
    .002% of all White US citizens live within this ZIP code).

    """

    def __init__(self, geo_level='ZCTA'):
        super().__init__()
        if geo_level.upper() == 'TRACT':
            self._PROB_RACE_GIVEN_GEO = self._get_prob_race_given_tract()
        else:
            self._PROB_RACE_GIVEN_GEO = self._get_prob_race_given_zcta()

    def get_probabilities(self, zctas):
        """Obtain race probabilities for a set of ZIP codes or ZCTAs.

        Parameters
        ----------
        zctas : pd.Series
            ZIPs/ZCTAs to which to attach race probability data

        Return
        ------
        pd.DataFrame
            Dataframe of race probability results

        """

        # Clean ZCTAs
        normalized_zctas = (
            self._normalize_zctas(zctas)
                .to_frame()
        )
        # Merge ZCTAs to race probabilities
        geocode_probs = normalized_zctas.merge(
            self._PROB_RACE_GIVEN_GEO,
            left_on='zcta5',
            right_index=True,
            how='left',
        )
        return geocode_probs

    def get_probabilities_tract(self, geo_df):
        """Obtain race probabilities for a set of State, County, Tract.

        Parameters
        ----------
        geo_df : pd.DataFrame
            DF of ['state','county','tract'] codes to retrun probabilities for

        Return
        ------
        pd.DataFrame
            Dataframe of race probability results

        """

        normalized_tracts = (
            self._normalize_tracts(geo_df)
        )
        # Merge ZCTAs to race probabilities
        geocode_probs = normalized_tracts.merge(
            self._PROB_RACE_GIVEN_GEO,
            left_on=['state','county','tract'],
            right_index=True,
            how='left',
        )
        return geocode_probs
