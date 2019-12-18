import pandas as pd

from .base_model import BaseModel


class SurnameModel(BaseModel):

    def __init__(self):
        super().__init__()
        self._PROB_RACE_GIVEN_SURNAME = self._get_prob_race_given_surname()

    def get_probabilities(self, names: pd.Series) -> pd.DataFrame:
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
