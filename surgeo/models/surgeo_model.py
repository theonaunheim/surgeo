import pandas as pd

from .base_model import BaseModel


class SurgeoModel(BaseModel):

    def __init__(self):
        super().__init__()

    def get_probabilities(self, 
                          names: pd.Series,
                          zctas: pd.Series, 
                          base_data=False) -> pd.DataFrame:
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
