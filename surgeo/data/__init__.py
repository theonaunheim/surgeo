'''This provides the data for surgeo.

It violates two of the cardinal rules of programming:
    1. It mixes data and code;
    2. The imports cause significant and long-lived side effects.

That said, the data involved is so central to the model that there's no way
to meaningfully run surgeo without loading this data first.

'''

import pathlib

import pandas as pd


# Get the folder in which the data is contained.
_module_init_path  = pathlib.Path(__file__)
_data_package_path = _module_init_path.parent

# Get data paths
_sur_path = _data_package_path / '2010_combined_geo_data.csv'
_geo_path = _data_package_path / '2010_surname_data.csv' 

# Create surname dataframe.
sur_df = pd.Series(
    _sur_path
)

# Crate geographic dataframe.
geo_df = pd.Series(
    _geo_path
)
