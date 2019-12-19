"""Module containing the SurnameModel class."""

import pandas as pd

from .base_model import BaseModel


class SurnameModel(BaseModel):
    """
    Notes
    -----
    The manner in which the surame data file was created can be found in
    the "fetch_surnames" Jupyter notebook.

    References
    ----------
    .. [1] United States Census Bureau. "Frequently Occurring Surnames from
    the 2010 Census".   
    https://www.census.gov/topics/population/genealogy/data/2010_surnames.html.  
    Last Accessed 2019.12.18.
    """

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
