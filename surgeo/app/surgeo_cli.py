"""Script containing a basic command line program."""

import argparse
import pathlib
import sys
import traceback

import pandas as pd

import surgeo

from surgeo.utility.surgeo_exception import SurgeoException
from surgeo.models.bifsg_model import BIFSGModel
from surgeo.models.first_name_model import FirstNameModel
from surgeo.models.geocode_model import GeocodeModel
from surgeo.models.surgeo_model import SurgeoModel
from surgeo.models.surname_model import SurnameModel


class SurgeoCLI(object):
    """A CLI application class to function as an executable

    This script adds surgeo to path and runs a simple command line script.
    The class pulls in a parser, parses the command line arguments as
    needed, loads the data, processes the data, and sends the output to a
    file. It uses the "main()" function and then uses other methods as
    helpers.

    Example
    -------
        .. code-block::

            $ surgeo --help

            usage: cli.py [-h] [--zcta_column ZCTA_COLUMN]
                          [-ct]
                          [--first_name_column FIRST_NAME_COLUMN]
                          [--surname_column SURNAME_COLUMN]
                          [--state_column STATE_COLUMN]
                          [--county_column COUNTY_COLUMN]
                          [--tract_column TRACT_COLUMN]
                          input output type

            Get Surgeo arguments.

            input                 Input CSV or XLSX of data.
            output                Output CSV or XLSX of data.
            type                  The model type being run ("first", "sur", "geo", "bifsg", or "surgeo")

            optional arguments:
            -h, --help            show this help message and exit
            -ct                  Process for CENSUS Tract as opposed to ZCTA/ZIP
            --zcta_column ZCTA_COLUMN
                                The input column to analyze as ZCTA/ZIP
            --first_name_column FIRST_NAME_COLUMN
                                The input column to analyze as first name
            --surname_column SURNAME_COLUMN
                                The input column to analyze as surname
            --state_column STATE_COLUMN input column containing two digit FIPS state code
            --county_column input column containing three digit FIPS County Code
            --tract_column input column containing six digit tract code

    """

    def __init__(self):
        # Parse args
        args = self._get_parsed_args()
        # Add those arguments as members
        self._input_path = pathlib.Path(args.input)
        self._output_path = pathlib.Path(args.output)
        self._model_type = args.type.lower()
        self._zcta_col = args.zcta_column
        self._first_col = args.first_name_column
        self._sur_col = args.surname_column
        self._state_col = args.state_column
        self._county_col = args.county_column
        self._tract_col = args.tract_column
        self._ct = args.ct
        self._zcta_col_default = 'zcta5'
        self._first_col_default = 'first_name'
        self._sur_col_default = 'name'

    def main(self):
        """This is the public interface function for this CLI.

        In summary, this function triggers various routines that:

        1. Read arguments;
        2. Take a user defined path argument and load an Excel or CSV into a
           dataframe;
        3. Route that dataframe to a speciic processing function based on the
           "type" function argument (e.g. first_name, surname, geocoding, bifsg, or surgeo);
        4. Optional specifies the column names to analyze (if not using the
           default "zcta5", "name", or "first_name" headers);
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
            # xlrd doesn't support xlsx as of 2021-01-23
            df = pd.read_excel(self._input_path, engine='openpyxl')
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
        if self._ct:
            model = GeocodeModel("TRACT")
        else:
            model = GeocodeModel("ZCTA")
        # If an optional name is specified, select that column and run
        if self._zcta_col is not None and not self._ct:
            model = GeocodeModel()
        # TODO: if they supply a name not found in CSV ... more specific error?
        # If an optional name is specified, select that column and run
        if self._zcta_col is not None:
            target = df[self._zcta_col]
            result = model.get_probabilities(target)
        # Otherwise use 'zcta5' (and raise error if need be.)
        elif self._state_col is not None and self._ct:
            target = df[[self._state_col, self._county_col, self._tract_col]]
            result = model.get_probabilities_tract(target)
        elif self._ct:
            try:
                target = df[['state', 'column', 'tract']]
            except KeyError:
                raise SurgeoException("Columns for state, county, and tract not found.")
        else:
            try:
                target = df[self._zcta_col_default]
                result = model.get_probabilities(target)
            except KeyError:
                raise SurgeoException(f'No "{self._zcta_col_default}" column '
                                       'and no column specified.')
        return result

    def _run_sur(self, df):
        """This runs a surname model for a given dataframe"""
        # Instantiate model
        model = SurnameModel()
        # If target is specified, get probabilities based on that target
        # TODO: if they supply a name not found in CSV ... more specific error?
        if self._sur_col is not None:
            target = df[self._sur_col]
            result = model.get_probabilities(target)
        # Otherwise use "name" as default (will throw error if unfound)
        else:
            try:
                target = df[self._sur_col_default]
                result = model.get_probabilities(target)
            except KeyError:
                raise SurgeoException(f'No "{self._sur_col_default}" column '
                                       'and no column specified.')
        return result

    def _run_first(self, df):
        """This runs a first name model for a given dataframe"""
        # Instantiate model
        model = FirstNameModel()
        # If target is specified, get probabilities based on that 
        # TODO: if they supply a name not found in CSV ... more specific error?
        if self._first_col is not None:
            target = df[self._first_col]
            result = model.get_probabilities(target)
        # Otherwise use "name" as default (will throw error if unfound)
        else:
            try:
                target = df[self._first_col_default]
                result = model.get_probabilities(target)
            except KeyError:
                raise SurgeoException(f'No "{self._first_col_default}" column '
                                       'and no column specified.')
        return result

    def _run_surgeo(self, df):
        """Runs a BISG model for a given dataframe"""
        
        # If ZIP target is specified, check accuracy
        if self._zcta_col is not None and not self._ct:
            try:
                geo_target = df[self._zcta_col]
                model = SurgeoModel()
            except KeyError:
                raise SurgeoException(f'Column "{self._zcta_col}"" not found.')
        elif self._ct and self._state_col is not None:
            try:
                geo_target = df[[self._state_col, self._county_col, self._tract_col]]
                model = SurgeoModel(geo_level='TRACT')
            except KeyError:
                raise SurgeoException(f'Columns for state, county, and tract not found.')
        elif self._ct:
            geo_target = df[['state','county','tract']]
            model = SurgeoModel(geo_level='TRACT')
        # Otherwise use zcta5 for ZIP target
        else:
            geo_target = df[self._zcta_col_default]
            model = SurgeoModel()
        # If Surname target spcified, check for accuracy
        if self._sur_col is not None:
            sur_target = df[self._sur_col]
            try:
                sur_target = df[self._sur_col]
            except KeyError:
                raise SurgeoException(f'Column "{self._sur_col}" not found.')
        # Otherwise, use name for surname column
        else:
            sur_target = df[self._sur_col_default]
        # Get probabilities
        result = model.get_probabilities(sur_target, geo_target)
        return result

    def _run_bifsg(self, df):
        """Runs a BIFSG model for a given dataframe"""
        # Instantiate model
        model = BIFSGModel()
        # If ZIP target is specified, check accuracy
        if self._zcta_col is not None:
            try:
                geo_target = df[self._zcta_col]
            except KeyError:
                raise SurgeoException(f'Column "{self._zcta_col}"" not found.')
        # Otherwise use zcta5 for ZIP target
        else:
            geo_target = df[self._zcta_col_default]
        # If Surname target specified, check for accuracy
        if self._sur_col is not None:
            sur_target = df[self._sur_col]
            try:
                sur_target = df[self._sur_col]
            except KeyError:
                raise SurgeoException(f'Column "{self._sur_col}" not found.')
        # Otherwise, use name for surname column
        else:
            sur_target = df[self._sur_col_default]
        # If first name target specified, check for accuracy
        if self._first_col is not None:
            first_target = df[self._first_col]
            try:
                first_target = df[self._first_col]
            except KeyError:
                raise SurgeoException(f'Column "{self._first_col}" not found.')
        # Otherwise, use name for surname column
        else:
            first_target = df[self._first_col_default]
        # Get probabilities
        result = model.get_probabilities(first_target, sur_target, geo_target)
        return result

    def _process_df(self, df):
        """Dispach function to proper model based on arguments"""
        # Get model type and create type map
        model_type = self._model_type
        type_map = {
            'first' : self._run_first,
            'sur'   : self._run_sur,
            'geo'   : self._run_geo,
            'bifsg' : self._run_bifsg,
            'surgeo': self._run_surgeo,
        }
        # Look up model in type_map and process
        try:
            process_func = type_map[model_type]
        # And throw error if not present
        except KeyError:
            raise SurgeoException(
                f'"{model_type}" is not valid model type. '
                f'Please use one of {type_map.keys()}.'
            )
        result_df = process_func(df)
        return result_df

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
            help='The model type being run ("first", "sur", "geo", "bifsg", or "surgeo")',
        )
        parser.add_argument(
            '--census_tract', action='store_true', help='Process at Census Tract Level instead of default ZCTA/Zip',
            dest='ct',  default=False
        )
        # Optional zcta column argument
        parser.add_argument(
            '--zcta_column',
            help='The input column to analyze as ZCTA/ZIP',
            dest='zcta_column'
        )
        # Optional surname column argument
        parser.add_argument(
            '--surname_column',
            help='The input column to analyze as surname',
            dest='surname_column'
        )

        parser.add_argument(
            '--state_column',
            help='The input column to analyze as two digit state code (required for census tract calculation)',
            dest='state_column'
        )
        parser.add_argument(
            '--county_column',
            help='The input column to analyze as 3 digit county code (required for census tract calculation)',
            dest='county_column'
        )
        parser.add_argument(
            '--tract_column',
            help='The input column to analyze as the 6 digit census tract  (required for census tract calculation)',
            dest='tract_column')
        # Optional first name column argument
        parser.add_argument(
            '--first_name_column',
            help='The input column to analyze as first name',
            dest='first_name_column'
        )
        # Parse args and return
        parsed_args = parser.parse_args()
        return parsed_args


if __name__ == '__main__':
    cli = SurgeoCLI()
    cli.main()
    sys.exit(0)
