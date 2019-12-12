import pandas as pd

from .base_model import BaseModel


class SurnameModel(BaseModel):

    def __init__(self):
        super().__init__()

    def get_probabilities(self, names: pd.Series) -> pd.DataFrame:
        surname_probs = self._get_surname_probs(names)
        return surname_probs
