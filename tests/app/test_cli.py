import os
import pathlib
import subprocess
import sys
import tempfile
import unittest

import numpy as np
import pandas as pd

import surgeo.app.surgeo_cli


class TestSurgeoCLI(unittest.TestCase):

    _CLI_SCRIPT = surgeo.app.surgeo_cli.__file__

    _DATA_FOLDER = pathlib.Path(__file__).resolve().parents[1] / 'data'

    _CSV_OUTPUT_PATH = str(
        pathlib.Path(tempfile.gettempdir())
            .joinpath('temp_surgeo.csv')
            .resolve()
    )

    _EXCEL_OUTPUT_PATH = str(
        pathlib.Path(tempfile.gettempdir())
            .joinpath('temp_surgeo.xlsx')
            .resolve()
    )

    def tearDown(self):
        if pathlib.Path(self._CSV_OUTPUT_PATH).exists():
            os.unlink(self._CSV_OUTPUT_PATH)
        if pathlib.Path(self._EXCEL_OUTPUT_PATH).exists():
            os.unlink(self._EXCEL_OUTPUT_PATH)

    def _compare(self, input_name, model_type, true_output_name, **kwargs):
        """"Helper function that runs the comparison
        
        Parameters
        ----------
        input_name : str
            The file name of the data to be tested
        model_type : str
            The model type being tested: ['bifsg', 'surgeo', 'first', 'sur', 'geo']
        true_output_name: str
            The correct data for comparison
        kwargs : **kwargs
            A kwarg dict with the keys being the --optional arguments and the values
            being the values associated with those arguments.

        """
        # Generate input name based on input file
        input_path = str(self._DATA_FOLDER / input_name)
        # Run a process that writes to CSV output
        subprocess_commands = [
            sys.executable,
            self._CLI_SCRIPT,
            input_path,
            self._CSV_OUTPUT_PATH,
            model_type,
        ]
        if kwargs:
            # Initial clever code:
            # subprocess_commands.extend([command for kvp in [[f'--{key}', kwargs[key]] for key in kwargs.keys()] for command in kvp])
            # 
            # Subsequent dumbed down code:
            # Convert kwarg key, value pairs to optional arguments e.g. ['--surname_column', 'custom_surname_col_name']
            argument_pairs = [
                [f'--{key}', value]
                for key, value
                in kwargs.items()
            ]
            # Add them to the subprocess arguments
            for argument_pair in argument_pairs:
                subprocess_commands.extend(argument_pair)
        subprocess.run(subprocess_commands, stderr=None)
        # Read the newly generated information
        df_generated = pd.read_csv(self._CSV_OUTPUT_PATH)
        # Read the true information
        df_true = pd.read_csv(self._DATA_FOLDER / true_output_name)
        # Compare values
        self._is_close_enough(df_generated, df_true)

    def _is_close_enough(self, df_generated, df_true):
        """Helper function to select floats, round them, and compare"""
        df_generated = df_generated.select_dtypes(np.float64).round(4)
        df_true = df_true.select_dtypes(np.float64).round(4)
        self.assertTrue(df_generated.equals(df_true))

    def test_surgeo_cli(self):
        """Test BISG model functionality of CLI"""
        self._compare(
            'surgeo_input.csv',
            'surgeo',
            'surgeo_output.csv',
        )

    def test_bifsg_cli(self):
        """Test bifsg model functionality of CLI"""
        self._compare(
            'bifsg_input.csv',
            'bifsg',
            'bifsg_output.csv',
            surname_column='surname',
            first_name_column='first_name'
        )

    def test_first_cli(self):
        """Test first name model functionality of CLI"""
        self._compare(
            'first_name_input.csv',
            'first',
            'first_name_output.csv',
        )

    def test_sur_cli(self):
        """Test surname model functionality of CLI"""
        self._compare(
            'surname_input.csv',
            'sur',
            'surname_output.csv',
        )

    def test_geo_cli(self):
        """Test geocode model functionality of CLI"""
        self._compare(
            'geocode_input.csv',
            'geo',
            'geocode_output.csv',
        )

    def test_excel(self):
        """Test Excel functionality of CLI"""
        # Generate input name based on input file
        input_path = str(self._DATA_FOLDER / 'surgeo_input.xlsx')
        # Run a process that writes to CSV output
        subprocess.run([
            sys.executable,
            self._CLI_SCRIPT,
            input_path,
            self._EXCEL_OUTPUT_PATH,
            'surgeo'
        ])
        # Read the newly generated information
        df_generated = pd.read_excel(self._EXCEL_OUTPUT_PATH, engine='openpyxl')
        # Read the true information
        df_true = pd.read_excel(self._DATA_FOLDER / 'surgeo_output.xlsx', engine='openpyxl')
        self._is_close_enough(df_generated, df_true)

    def test_malformed(self):
        """Test arguments to specify column names"""
        # Generate input name based on input file
        input_path = str(self._DATA_FOLDER / 'surgeo_input_misnamed.csv')
        # Run a process that writes to CSV output
        subprocess.run([
            sys.executable,
            self._CLI_SCRIPT,
            input_path,
            self._CSV_OUTPUT_PATH,
            'surgeo',
            '--zcta_column',
            'info_zip',
            '--surname_column',
            'info_name',
        ])
        # Read the newly generated information
        df_generated = pd.read_csv(self._CSV_OUTPUT_PATH)
        # Read the true information
        df_true = pd.read_csv(self._DATA_FOLDER / 'surgeo_output.csv')
        self._is_close_enough(df_generated, df_true)

    def test_tract_simple(self):
        """Test arguments to specify column names for census tract defaults"""
        # Generate input name based on input file
        input_path = str(self._DATA_FOLDER / 'tract_input.csv')
        # Run a process that writes to CSV output
        subprocess.run([
            sys.executable,
            self._CLI_SCRIPT,
            input_path,
            self._CSV_OUTPUT_PATH,
            'geo',
            '--census_tract', 
            '--surname_column',
            'name',
            '--state_column',
            'state', 
            '--tract_column',
            'tract',
            '--county_column',
            'county'
        ])
        # Read the newly generated information
        df_generated = pd.read_csv(self._CSV_OUTPUT_PATH)
        # Read the true information
        df_true = pd.read_csv(self._DATA_FOLDER / 'tract_output.csv')
        self._is_close_enough(df_generated, df_true)

if __name__ == '__main__':
    unittest.main()
