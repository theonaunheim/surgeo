"""Script containing a basic command line program."""

import argparse
import pathlib
import sys
import traceback

import pandas as pd

import surgeo

from surgeo.utility.surgeo_exception import SurgeoException
from surgeo import GeocodeModel
from surgeo import SurgeoModel
from surgeo import SurnameModel


class SurgeoCLI(object):
    """A CLI application class to function as an executable

    This script adds surgeo to path and runs a simple command line script.
    The class pulls in a parser, parsers the command line arguments as
    needed, loads the data, processes the data, and sends the output to a
    file. It uses the "main()" function and then uses other methods as
    helpers.

    Example
    -------
        .. code-block::

            $ surgeo --help

            usage: cli.py [-h] [--zcta_column ZCTA_COLUMN]
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
        # Parse args
        args = self._get_parsed_args()
        # Add those arguments as members
        self._input_path = pathlib.Path(args.input)
        self._output_path = pathlib.Path(args.output)
        self._model_type = args.type.lower()
        self._zcta_col = args.zcta_column
        self._sur_col = args.surname_column

    def main(self):
        """This is the public interface function for this CLI.

        In summary, this function triggers various routines that:

        1. Read arguments;
        2. Take a user defined path argument and load an Excel or CSV into a
           dataframe;
        3. Route that dataframe to a speciic processing function based on the
           "type" function argument (e.g. surname, geocoding, or surgeo);
        4. Optional specifies the column names to analyze (if not using the
           default "zcta5" or "name" headers);
        5. Runs the appropriate algorithm and returns a new dataframe;
        6. Writes the resulting data to a new CSV based to output path
           specified by user.

        Raises
        ------
        surgeo.utility.SurgeoException
            Raised if 1) file endings are not correct, 2) inappropriate columns
            are specified, 3) an incorrect model type is supplied, or 4) an
            inappropriate outputs are not specified.

        """
        input_df = self._load_df()
        processed_df = self._process_df(input_df)
        self._write_df(processed_df)

    def _load_df(self):
        """This creates a dataframe based on self._input_path"""
        suffix = self._input_path.suffix
        # If it's excel, read_excel()
        if suffix == '.xlsx' or suffix == 'xls':
            df = pd.read_excel(self._input_path)
        # If CSV, read read_csv()
        elif suffix == '.csv':
            df = pd.read_csv(
                self._input_path, 
                skip_blank_lines=False,
            )
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
        """This runs a surname model for a given dataframe"""
        # Instantiate model
        model = SurnameModel()
        # If target is specified, get probabilities based on that target
        if self._sur_col is not None:
            target = df[self._sur_col]
            result = model.get_probabilities(target)
        # Otherwise use "name" as default (will throw error if unfound)
        else:
            try:
                target = df['name']
                result = model.get_probabilities(target)
            except KeyError:
                raise SurgeoException('No "name" column and no column '
                                      'specified.')
        return result

    def _run_surgeo(self, df):
        """Runs a BISG model for a given dataframe"""
        # Instantiate model
        model = SurgeoModel()
        # If ZIP target is specified, check accuracy
        if self._zcta_col is not None:
            try:
                geo_target = df[self._zcta_col]
            except KeyError:
                raise SurgeoException(f'Column "{self._zcta_col}"" not found.')
        # Otherwise use zcta5 for ZIP target
        else:
            geo_target = df['zcta5']
        # If Surname target spcified, check for accuracy
        if self._sur_col is not None:
            sur_target = df[self._sur_col]
            try:
                sur_target = df[self._sur_col]
            except KeyError:
                raise SurgeoException(f'Column "{self._sur_col}" not found.')
        # Otherwise, use name for surname column
        else:
            sur_target = df['name']
        # Get probabilities
        result = model.get_probabilities(sur_target, geo_target)
        return result

    def _process_df(self, df):
        """Dispach function to proper model based on arguments"""
        # Get model type and create type map
        model_type = self._model_type
        type_map = {
            'sur'   : self._run_sur,
            'geo'   : self._run_geo,
            'surgeo': self._run_surgeo,
        }
        # Look up model in type_map and process
        try:
            process_func = type_map[model_type]
            result_df = process_func(df)
            return result_df
        # And throw error if not present
        except KeyError:
            raise SurgeoException(
                f'"{model_type}" is not valid model type. '
                f'Please use "sur", "geo", or "surgeo".'
            )

    def _write_df(self, df):
        """Write to CSV or XLSX depending on file suffix"""
        suffix = self._output_path.suffix
        # If excel, write to Excel
        if suffix == '.xlsx':
            df.to_excel(self._output_path, index=False)
        # If CSV write to CSV
        elif suffix == '.csv':
            df.to_csv(self._output_path, index=False)
        # Otherwise throw error.
        else:
            raise SurgeoException(
                f'"{self._output_path}" is not a valid. '
                f'Please specify a path ending in ".csv" or ".xlsx".'
            )

    def _get_parsed_args(self):
        """Create an argument parser and parse CLI arguments"""
        # Create parser
        parser = argparse.ArgumentParser(description='Get Surgeo arguments.')
        # Add input file path argument
        parser.add_argument(
            'input',
            help='Input CSV or XLSX of data.',
        )
        # Output file path argument
        parser.add_argument(
            'output',
            help='Output CSV or XLSX of data.',
        )
        # Model type argument
        parser.add_argument(
            'type',
            help='The model type being run ("sur", "geo" or "surgeo")',
        )
        # Optional zcta column argument
        parser.add_argument(
            '--zcta_column',
            help='The input column to analyze as ZCTA/ZIP)',
            dest='zcta_column'
        )
        # Optional surname column argument
        parser.add_argument(
            '--surname_column',
            help='The input column to analyze as surname")',
            dest='surname_column'
        )
        # Parse args and return
        parsed_args = parser.parse_args()
        return parsed_args


if __name__ == '__main__':
    cli = SurgeoCLI()
    cli.main()
    sys.exit(0)
