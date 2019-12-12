import pandas as pd

from .base_model import BaseModel


class GeocodeModel(BaseModel):

    def __init__(self):
        super().__init__()
    
    def get_probabilities(self, zctas: pd.Series) -> pd.DataFrame:
        geocode_probs = self._get_geocode_probs(zctas)
        return geocode_probs
