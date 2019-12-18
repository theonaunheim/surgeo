import pandas as pd

from .base_model import BaseModel


class GeocodeModel(BaseModel):

    def __init__(self):
        super().__init__()
        self._PROB_RACE_GIVEN_ZCTA = self._get_prob_race_given_zcta()

    def get_probabilities(self, zctas: pd.Series) -> pd.DataFrame:
        normalized_zctas = (
            self._normalize_zctas(zctas)
                .to_frame()
        )
        geocode_probs = normalized_zctas.merge(
            self._PROB_RACE_GIVEN_ZCTA,
            left_on='zcta5',
            right_index=True,
            how='left',
        )
        return geocode_probs
