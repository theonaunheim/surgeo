"""Module for base BaseMixin class."""

import abc
import pathlib
import sys


class BaseLoader(abc.ABC):
    """Base class for all loader data mixins.

    These loader mixins are included within models to given them access
    to the data they need. The code in this abstract class simply
    includes information to establish common loader functionality (namely)
    establishing self._package_root and self._data_root.

    """

    @property
    def _package_root(self):
        """pathlib.Path: the path of the module"""

        # https://cx-freeze.readthedocs.io/en/latest/faq.html#using-data-files
        # If it's frozen, we can't use __file__
        if getattr(sys, 'frozen', False):
            # The application is frozen
            freeze_package = pathlib.Path(sys.executable).parents[0]
            package_root = freeze_package / 'Lib' / 'surgeo'
        else:
            # The application is not frozen
            package_root = pathlib.Path(__file__).resolve().parents[2]
        return package_root

    @property
    def _data_dir(self):
        """pathlib.Path: the path of the data folder in the module"""

        data_dir = self._package_root / 'data'
        return data_dir




'''

class ForenameLoader(BaseLoader):
    """This mixin loader loads data for use in forename models.

    Notes
    -----
    The probability dataframe for this model is generated can be found
    in the `data` folder of the module and is named:

    `prob_race_given_forename.csv`
    
    The script for creating the CSV file itself was created can be found
    in the `scripts` folder of the main repository and is named:

    `create_prob_race_given_forename.py`

    """

    def __init__(self):
        super().__init__()
        self._PROB_RACE_GIVEN_FORENAME = self._get_prob_race_given_forename()

    def _get_prob_race_given_forname(self):
        """Create dataframe of race probabilities given first names (for First)"""
        # Create first name df (beware ... some NA values like "NAN" are names)
        prob_race_given_first_name = pd.read_csv(
            self._package_root / 'data' / 'prob_race_given_first_name_harvard.csv',
            index_col='name',
            na_values=[''],
            keep_default_na=False,
        )
        return prob_race_given_first_name

'''