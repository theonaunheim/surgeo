"""Module for base BaseMixin class."""

import abc
import pathlib
import sys


class BaseMixin(abc.ABC):
    """Base class for all mixins data mixins.

    It mainly exists to establish self._package_root and self._data_root

    """

    @property
    def _package_root(self):
        """str: Properties should be documented in their getter method.
        
        """

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
        """

        """

        data_dir = self._package_root / 'data'
        return data_dir
