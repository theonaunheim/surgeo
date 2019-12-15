"""Script containing a basic command line program."""

import argparse
import pathlib
import sys
import traceback

import pandas as pd

# Jury rig path
path_dir = pathlib.Path(__file__).resolve().parents[2]
sys.path.append(str(path_dir))

import surgeo

from surgeo.utility.surgeo_exception import SurgeoException
from surgeo import GeocodeModel
from surgeo import SurgeoModel
from surgeo import SurnameModel


class SurgeoCLI(object):
    """A CLI application class to create executable

    This script adds surgeo to path and runs a simple command line script.
    The class pulls in a parser, parsers the command line arguments as
    needed, loads the data, processes the data, and sends the output to a
    file. It uses the "surgeo_main()" function and then uses other methods
    as helpers.

    usage: executable.py [-h] [--zcta_column ZCTA_COLUMN]
                        [--surname_column SURNAME_COLUMN]
                        input output type

    Get Surgeo arguments.

    input                 Input CSV or XLSX of data.
    output                Output CSV or XLSX of data.
    type                  The model type being run ("sur", "geo" or "surgeo")

    optional arguments:
    -h, --help            show this help message and exit
    --zcta_column ZCTA_COLUMN
                        The input column to analyze as ZCTA/ZIP)
    --surname_column SURNAME_COLUMN
                        The input column to analyze as surname")

    """

    def __init__(self):
        # Get args from SurgeoArgParser class
        args = self.get_parsed_args()
        # Add those arguments as members
        self._input_path = pathlib.Path(args.input)
        self._output_path = pathlib.Path(args.output)
        self._model_type = args.type.lower()
        self._zcta_col = args.zcta_column
        self._sur_col = args.surname_column

    def _load_df(self):
        """This creates a dataframe based on self._input_path"""
        suffix = self._input_path.suffix
        # If it's excel, read_excel()
        if suffix == '.xlsx' or suffix == 'xls':
            df = pd.read_excel(self._input_path)
        # If CSV, read read_csv()
        elif suffix == '.csv':
            df = pd.read_csv(self._input_path)
        # If path is unrecognized, throw error
        else:
            raise SurgeoException(
                f'File ending for "{self._input_path}" not '
                'recognized. Please use .csv or .xlsx.'
            )
        return df

    def _run_geo(self, df):
        """Method called from self._process_df() to get geo results"""
        model = GeocodeModel()
        # If an optional name is speicied, select that column and run
        if self._zcta_col is not None:
            target = df[self._zcta_col]
            result = model.get_probabilities(target)
        # Otherwise use 'zcta5' (and raise error if need be.)
        else:
            try:
                target = df['zcta5']
                result = model.get_probabilities(target)
            except KeyError:
                raise SurgeoException('No "zcta5" column and no column '
                                      'specified.')
        return result

    def _run_sur(self, df):
        model = SurnameModel()
        if self._sur_col is not None:
            target = df[self._sur_col]
            result = model.get_probabilities(target)
        else:
            target = df['name']
            result = model.get_probabilities(target)
        return result

    def _run_surgeo(self, df):
        model = SurgeoModel()
        if self._zcta_col is not None:
            geo_target = df[self._zcta_col]
        else:
            geo_target = df['zcta5']
        if self._sur_col is not None:
            sur_target = df[self._sur_col]
        else:
            sur_target = df['name']
        result = model.get_probabilities(sur_target, geo_target)
        return result

    def _process_df(self, df):
        model_type = self._model_type
        type_map = {
            'sur'   : self._run_sur,
            'geo'   : self._run_geo,
            'surgeo': self._run_surgeo,
        }
        try:
            process_func = type_map[model_type]
            result_df = process_func(df)
            return result_df
        except KeyError:
            raise SurgeoException(
                f'"{model_type}" is not valid model type. '
                'Please use "sur", "geo", or "surgeo".'
            )            

    def _write_df(self, df):
        suffix = self._output_path.suffix
        if suffix == '.xlsx':
            df.to_excel(self._output_path, index=False)
        elif suffix == '.csv':
            df.to_csv(self._output_path, index=False)
        else:
            raise SurgeoException(
                f'"{self._output_path}" is not a valid. '
                'Please specify a path ending in ".csv" or ".xlsx".'    
            )

    def get_parsed_args(self):
        parser = argparse.ArgumentParser(description='Get Surgeo arguments.')
        parser.add_argument(
            'input',
            help='Input CSV or XLSX of data.',
        )
        parser.add_argument(
            'output',
            help='Output CSV or XLSX of data.',
        )
        parser.add_argument(
            'type',
            help='The model type being run ("sur", "geo" or "surgeo")',
        )
        parser.add_argument(
            '--zcta_column',
            help='The input column to analyze as ZCTA/ZIP)',
            dest='zcta_column'
        )
        parser.add_argument(
            '--surname_column',
            help='The input column to analyze as surname")',
            dest='surname_column'
        )
        parsed_args = parser.parse_args()
        return parsed_args

    def main(self):
        input_df = self._load_df()
        processed_df = self._process_df(input_df)
        self._write_df(processed_df)        


if __name__ == '__main__':
    cli = SurgeoCLI()
    cli.main()
    sys.exit(0)
