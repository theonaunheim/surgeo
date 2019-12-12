import pandas as pd

from .base_model import BaseModel


class GeocodeModel(BaseModel):

    def __init__(self):
        super().__init__()
    
    def get_probabilities(self, 
                          zcta: pd.Series,
                          missing='nan') -> pd.Series:
        normalized_zctas = self._normalize_zctas(zcta)
        result = (
            self._GEOCODE_DF.map(
                normalized_zctas,
                left_index=True,
            )
        )
