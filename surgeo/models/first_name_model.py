"""Module containing the FirstNameModel class."""

import pandas as pd

from surgeo.models.base_model import BaseModel


class FirstNameModel(BaseModel):
    """Provides a way to look up race percentages by first name.

    This class uses a get_probabilities() method to provide a simple
    mechanism for obtaining race data. It is created using a simple join
    of a race data table and the first names that are input.

    Notes
    -----
    The manner in which the first name data file was created can be found in
    the "fetch_first_names" Jupyter notebook.

    The first name probability dataframe for this model is generated from the
    `prob_race_given_first_name_harvard.csv` file.

    """

    def __init__(self):
        super().__init__()
        self._PROB_RACE_GIVEN_FIRST_NAME = self._get_prob_race_given_first_name()

    def get_probabilities(self, names):
        """Obtain race probabilities for a set of first names.

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
        first_name_probs = normalized_names.merge(
            self._PROB_RACE_GIVEN_FIRST_NAME,
            left_on='name',
            right_index=True,
            how='left',
        )
        # Rename to avoid clashes with "name"
        first_name_probs = first_name_probs.rename(columns={'name': 'first_name'})
        return first_name_probs
