"""Module containing Surgeo BISG class"""

import pandas as pd
from typing import Union

from surgeo.models.base_model import BaseModel
from surgeo.utility.surgeo_exception import SurgeoException


class SurgeoModel(BaseModel):
    r"""Subclass for running a Bayesian Improved Surname Geocode model.

    This class:

    1. Loads the appropriate surname and geocode lookup dataframes upon
       instantiation;
    2. Exposes a public get_probabilities() function to compute race
       probabilities based on proxy data (namely surnames and ZIP codes); and,
    3. Contains a number of helper functions for cleaning ZCTA/names,
       multiplying probabilities, checking input values, and obtaining
       ZCTA/name data components.

    Notes
    -----
    The surname probability dataframe for this model is identical to that
    used for the SurnameModel (`prob_race_given_surname_2010.csv`); the
    geocode probability dataframe for this model is not the same as that
    used for the GeocodeModel. This model uses the
    `prob_zcta_given_race_2010.csv` file, which has the percentage of
    a particular race that falls within that ZCTA (e.g. .002% of all
    White US citizens live within this ZIP code). The GeocodeModel uses the
    `prob_race_given_zcta_2010.csv` file, which has the race percentages
    for a given ZCTA (e.g. 90% of ZCTA 63144 is White).

    The manner in which the geography data file was created can be found in
    the "fetch_geography" Jupyter notebook.

    This is based of the following general formula from Elliott et al [#]_.

    | :math:`q(i \mid j,k) = \Large \frac{u(i,j,k)}{u(1,j,k) \, + \, u(2,j,k) \, + \, u(3,j,k) \, + \, u(4,j,k) \, + \, u(5,j,k) \, + \, u(6,j,k)}`
    |
    | Where:
    | :math:`\hspace{25px} u(i,j,k) = P(i \mid j) \times r(k \mid i)`
    |
    | And where:
    | :math:`\hspace{25px} P(i \mid j)` is the probability of a selected race given surname
    | :math:`\hspace{25px} r(k \mid i)` is the probability of a selected census block of residence given race
    | :math:`\hspace{25px} k` is Census Block
    | :math:`\hspace{25px} j` is Surname
    | :math:`\hspace{25px} i` is Race
    |
    | And where:
    | :math:`\hspace{25px} 1 \text{ is } i =` Hispanic
    | :math:`\hspace{25px} 2 \text{ is } i =` White
    | :math:`\hspace{25px} 3 \text{ is } i =` Black
    | :math:`\hspace{25px} 4 \text{ is } i =` Asian or Pacific Islander
    | :math:`\hspace{25px} 5 \text{ is } i =` American Indian / Alaska Native
    | :math:`\hspace{25px} 6 \text{ is } i =` Multi Racial

    References
    ----------

    .. [#]

        Elliott, M.N., Morrison, P.A., Fremont, A. et al. Using the Census
        Bureau’s surname list to improve estimates of race/ethnicity and
        associated disparities. Health Serv Outcomes Res Method (2009) 9:
        69. `<https://link.springer.com/article/10.1007/s10742-009-0047-1>`_

    """
    def __init__(self, geo_level="ZCTA"):
        super().__init__()
        self.geo_level = geo_level.upper()
        if geo_level == "TRACT":
            self._PROB_GEO_GIVEN_RACE = self._get_prob_race_given_tract()
        else:
            self._PROB_GEO_GIVEN_RACE = self._get_prob_zcta_given_race()
        self._PROB_RACE_GIVEN_SURNAME = self._get_prob_race_given_surname()

    def get_probabilities(self, names, geo_df):
        """Obtain a set of BISG probabilities for name/ZCTA series

        This method first takes the data and checks to see if the data is
        formatted appropriately. It triggers the _get_surname_probs() and
        _get_geocode_probs() helper function to merge the probabilities
        for the inputs with their looked-up values. It then runs the
        _combined_probs() helper function to actually conduct the data
        calculation and obtain the BISG probabilities. It finally runs the
        _adjust_frame() method to concatenate the inputs and outputs in a
        single convenient frame.

        Parameters
        ----------
        names : pd.Series
            A series of names to use for the BISG algorithm
        geo_df : Union[pd.Series, pd.DataFrame]
            A series of target ZIP/ZCTA codes or State County Tract for the BISG algorithm

        Returns
        -------
        pd.DataFrame
            Dataframe of BISG probability results

        """

        # Check inputs
        self._check_inputs(names, geo_df)
        # Get component probabilities
        sur_probs = self._get_surname_probs(names)
        geo_probs = self._get_geocode_probs(geo_df)
        # Run Surgeo algorithm
        surgeo_probs = self._combined_probs(sur_probs, geo_probs)
        # Combine inputs with results and adjust as necessary
        result = self._adjust_frame(
            sur_probs,
            geo_probs,
            surgeo_probs,
        )
        return result

    def _combined_probs(self,
                        sur_probs: pd.DataFrame,
                        geo_probs: pd.DataFrame) -> pd.DataFrame:
        """Performs the BISG calculation"""
        # Calculate each of the numerators
        surgeo_numer = sur_probs.iloc[:, 1:] * geo_probs.iloc[:, 1:]
        # Calculate the denominator
        surgeo_denom = surgeo_numer.sum(axis=1)
        # Caluclate the surgeo probabilities (each num / denom)
        surgeo_probs = surgeo_numer.div(surgeo_denom, axis=0)
        return surgeo_probs

    def _adjust_frame(self,
                      sur_probs: pd.DataFrame,
                      geo_probs: pd.DataFrame,
                      surgeo_probs: pd.DataFrame) -> pd.DataFrame:
        # Build frame from zctas, names, and probabilities
        if self.geo_level == 'TRACT':
            surgeo_data = pd.concat([geo_probs[['state','county','tract']], 
                sur_probs['name'].to_frame(),
                surgeo_probs
            ], axis=1)
        else:
            surgeo_data = pd.concat([
                geo_probs['zcta5'].to_frame(),
                sur_probs['name'].to_frame(),
                surgeo_probs
            ], axis=1)
        return surgeo_data

    def _check_inputs(self,
                      names: pd.Series,
                      geo_df: Union[pd.Series, pd.DataFrame]):
        """Check names and ZCTAs and ensure they are same length"""
        if len(names) != len(geo_df):
            err_string = (
                f'Length mismatch. '
                f'Name length: {len(names)}. '
                f'Geo DF length: {len(geo_df)}.'
            )
            raise SurgeoException(err_string)

    def _get_surname_probs(self,
                           names: pd.Series) -> pd.DataFrame:
        """Normalizes names and joins names to their race probabilities."""
        # Normalize names
        normalized_names = (
            self._normalize_names(names)
                .to_frame()
        )
        # Merge names to dataframe, which gives probs for each name
        surname_probs = normalized_names.merge(
            self._PROB_RACE_GIVEN_SURNAME,
            left_on='name',
            right_index=True,
            how='left',
        )
        return surname_probs

    def _get_geocode_probs(self, geo_df: Union[pd.Series, pd.DataFrame]) -> pd.DataFrame:
        """Normalizes ZCTAs/ZIPs and joins them to their race probs."""
        # Normalize
        if self.geo_level == 'TRACT':
            normalized_tracts = (
                self._normalize_tracts(geo_df)
            )
            geocode_probs = normalized_tracts.merge(
                self._PROB_GEO_GIVEN_RACE,
                left_on=['state','county','tract'],
                right_index=True,
                how='left',
            )
        else: 
            normalized_zctas = (
                self._normalize_zctas(geo_df)
                    .to_frame()
            )
            # Merge names to dataframe, which gives probs for each name.
            geocode_probs = normalized_zctas.merge(
                self._PROB_GEO_GIVEN_RACE,
                left_on='zcta5',
                right_index=True,
                how='left',
            )
        return geocode_probs
