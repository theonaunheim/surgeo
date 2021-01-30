"""Module containing the SurnameModel class."""

import pandas as pd

from surgeo.models.base_model import BaseModel


class SurnameModel(BaseModel):
    """Provides a way to look up race percentages by surname.

    This class uses a get_probabilities() method to provide a simple
    mechanism for obtaining race data. It is created using a simple join
    of a race data table and the surnames that are input.

    Notes
    -----
    The manner in which the surname data file was created can be found in
    the "fetch_surnames" Jupyter notebook.

    The surname probability dataframe for this model is generated from the
    `prob_race_given_surname_2010.csv` file.

    """

    def __init__(self):
        super().__init__()
        self._PROB_RACE_GIVEN_SURNAME = self._get_prob_race_given_surname()

    def get_probabilities(self, names):
        """Obtain race probabilities for a set of surnames.

        Parameters
        ----------
        names : pd.Series
            names to which to attach race probability data

        Return
        ------
        pd.DataFrame
            Dataframe of race probability results

        """

        # Clean and process names (consistent with Word et al)
        normalized_names = (
            self._normalize_names(names)
                .to_frame()
        )
        # Do a simple join to obtain the names along with provs.
        surname_probs = normalized_names.merge(
            self._PROB_RACE_GIVEN_SURNAME,
            left_on='name',
            right_index=True,
            how='left',
        )
        return surname_probs
