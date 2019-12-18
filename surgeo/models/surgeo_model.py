import pandas as pd

from .base_model import BaseModel
from ..utility.surgeo_exception import SurgeoException


class SurgeoModel(BaseModel):
    """

    References
    ----------
    .. [1] Elliott, M.N., Morrison, P.A., Fremont, A. et al. "Using the 
    Census Bureau’s surname list to improve estimates of race/ethnicity and 
    associated disparities". Health Serv Outcomes Res Method (2009) 9: 69.
    https://link.springer.com/article/10.1007/s10742-009-0047-1

    """
    def __init__(self):
        super().__init__()
        self._PROB_ZCTA_GIVEN_RACE = self._get_prob_zcta_given_race()
        self._PROB_RACE_GIVEN_SURNAME = self._get_prob_race_given_surname()

    def get_probabilities(self, 
                          names: pd.Series,
                          zctas: pd.Series, 
                          base_data=False) -> pd.DataFrame:
        # Check inputs
        self._check_inputs(names, zctas)
        # Get components
        sur_probs = self._get_surname_probs(names)
        geo_probs = self._get_geocode_probs(zctas)
        # Get surgeo probs
        surgeo_probs = self._combined_probs(sur_probs, geo_probs)
        result = self._adjust_frame(
            sur_probs,
            geo_probs,
            surgeo_probs,
            base_data,
        )
        return result

    def _combined_probs(self,
                        sur_probs: pd.DataFrame,
                        geo_probs: pd.DataFrame) -> pd.DataFrame:
        # Calculate each of the numerators
        surgeo_numer = sur_probs.iloc[:, 1:] * geo_probs.iloc[:, 1:]
        # Calculate the denominator
        surgeo_denom = surgeo_numer.sum(axis=1)
        # Caluclate the surgeo probabilities
        surgeo_probs = surgeo_numer.div(surgeo_denom, axis=0)
        surgeo_probs = surgeo_probs.round(4)
        return surgeo_probs

    def _adjust_frame(self,
                      sur_probs: pd.DataFrame,
                      geo_probs: pd.DataFrame,
                      surgeo_probs: pd.DataFrame,
                      base_data: bool) -> pd.DataFrame:
        # Build base
        surgeo_data = pd.concat([
            geo_probs['zcta5'].to_frame(),
            sur_probs['name'].to_frame(),
            surgeo_probs
        ], axis=1)
        if base_data is True:
            sur_data = sur_probs.iloc[:, 1:]
            geo_data = geo_probs.iloc[:, 1:]
            merged_data = sur_data.merge(
                geo_data, 
                left_index=True,
                right_index=True,
                suffixes=['_sur', '_geo']
            )
            surgeo_data = pd.concat([
                surgeo_data,
                merged_data,
            ], axis=1)
            return surgeo_data
        else:
            return surgeo_data

    def _check_inputs(self, 
                      names: pd.Series,
                      zctas: pd.Series):
        if len(names) != len(zctas):
            err_string = (
                f'Length mismatch. '
                f'Name length: {len(names)}. '
                f'ZCTA length: {len(zctas)}.'
            )
            raise SurgeoException(err_string)

    def _get_surname_probs(self, names: pd.Series) -> pd.DataFrame:
        normalized_names = (
            self._normalize_names(names)
                .to_frame()
        )
        surname_probs = normalized_names.merge(
            self._PROB_RACE_GIVEN_SURNAME,
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
            self._PROB_ZCTA_GIVEN_RACE,
            left_on='zcta5',
            right_index=True,
            how='left',
        )
        return geocode_probs
