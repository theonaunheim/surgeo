import os
import pathlib
import subprocess
import sys
import tempfile
import unittest

import pandas as pd

import surgeo.app.cli


class TestSurgeoCLI(unittest.TestCase):

    _CLI_SCRIPT = surgeo.app.cli.__file__

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

    def compare(self, input_name, model_type, true_output_name):
        """"Helper function that runs the comparison"""
        # Generate input name based on input file
        input_path = str(self._DATA_FOLDER / input_name)
        # Run a process that writes to CSV output
        subprocess.run([
            sys.executable, 
            self._CLI_SCRIPT,
            input_path,
            self._CSV_OUTPUT_PATH,
            model_type
        ], stderr=None)
        # Read the newly generated information
        df_generated = pd.read_csv(self._CSV_OUTPUT_PATH)
        # Read the true information
        df_true = pd.read_csv(self._DATA_FOLDER / true_output_name)
        # Compare values
        self.assertTrue(
            df_generated.equals(df_true)
        )        

    def test_surgeo_cli(self):
        """Test BISG model functionality of CLI"""
        self.compare(
            'surgeo_input.csv',
            'surgeo',
            'surgeo_output.csv',
        )

    def test_sur_cli(self):
        """Test surname model functionality of CLI"""
        self.compare(
            'surname_input.csv',
            'sur',
            'surname_output.csv',
        )

    def test_geo_cli(self):
        """Test geocode model functionality of CLI"""
        self.compare(
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
        df_generated = pd.read_excel(self._EXCEL_OUTPUT_PATH)
        # Read the true information
        df_true = pd.read_excel(self._DATA_FOLDER / 'surgeo_output.xlsx')
        # Compare values
        self.assertTrue(
            df_generated.equals(df_true)
        )        

    def test_malformed(self):
        pass

if __name__ == '__main__':
    unittest.main()
