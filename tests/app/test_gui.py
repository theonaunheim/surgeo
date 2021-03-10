import os
import pathlib
import tempfile
import unittest

import tkinter as tk

import numpy as np
import pandas as pd

import surgeo.app.surgeo_gui


class TestSurgeoGUI(unittest.TestCase):

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

    _GUI = surgeo.app.surgeo_gui.SurgeoGUI()

    @classmethod
    def setUpClass(cls):
        """Set up everything but do not run mainloop"""
        # Add in new root window that is invisible
        cls._GUI._objects['root'].iconify()
        # Setup window and add widgets
        cls._GUI._window_setup()
        cls._GUI._add_widgets()

    def tearDown(self):
        if pathlib.Path(self._CSV_OUTPUT_PATH).exists():
            os.unlink(self._CSV_OUTPUT_PATH)
        if pathlib.Path(self._EXCEL_OUTPUT_PATH).exists():
            os.unlink(self._EXCEL_OUTPUT_PATH)

    def _run_model(self,
                   input_name,
                   model,
                   output_path,
                   first_name_header,
                   surname_header,
                   zip_header):
        """Helper function that actually runs the model"""
        # Input variables
        self._GUI._objects['input_var'].set(input_name)
        self._GUI._objects['model_var'].set(model)
        self._GUI._objects['output_var'].set(output_path)
        self._GUI._objects['first_name_var'].set(first_name_header)
        self._GUI._objects['surname_var'].set(surname_header)
        self._GUI._objects['zip_var'].set(zip_header)
        # Update events (required)
        self._GUI._objects['root'].update()
        # Execute
        self._GUI._execute(show_msgbox=False)

    def _is_close_enough(self, df_generated, df_true):
        """Helper function to select floats, round them, and compare"""
        df_generated = df_generated.select_dtypes(np.float64).round(4)
        df_true = df_true.select_dtypes(np.float64).round(4)
        self.assertTrue(df_generated.equals(df_true))

    def test_bifsg(self):
        """Test GUI BIFSG functionality"""
        INPUT = 'bifsg_input.csv'
        MODEL = 'BIFSG'
        TRUE_OUTPUT = 'bifsg_output.csv'
        SURNAME_HEADER = 'surname'
        FIRST_NAME_HEADER = 'first_name'
        ZIP_HEADER = 'zcta5'
        self._run_model(
            self._DATA_FOLDER / INPUT,
            MODEL,
            self._CSV_OUTPUT_PATH,
            FIRST_NAME_HEADER,
            SURNAME_HEADER,
            ZIP_HEADER,
        )
        # Get our data
        df_generated = pd.read_csv(self._CSV_OUTPUT_PATH)
        df_true = pd.read_csv(self._DATA_FOLDER / TRUE_OUTPUT)
        # Compare values
        self._is_close_enough(df_generated, df_true)

    def test_first_name(self):
        """Test GUI First Name functionality"""
        INPUT = 'first_name_input.csv'
        MODEL = 'First Name'
        TRUE_OUTPUT = 'first_name_output.csv'
        SURNAME_HEADER = 'surname'
        FIRST_NAME_HEADER = 'first_name'
        ZIP_HEADER = 'zcta5'
        self._run_model(
            self._DATA_FOLDER / INPUT,
            MODEL,
            self._CSV_OUTPUT_PATH,
            FIRST_NAME_HEADER,
            SURNAME_HEADER,
            ZIP_HEADER,
        )
        # Get our data
        df_generated = pd.read_csv(self._CSV_OUTPUT_PATH)
        df_true = pd.read_csv(self._DATA_FOLDER / TRUE_OUTPUT)
        # Compare values
        self._is_close_enough(df_generated, df_true)

    def test_geocode(self):
        """Test GUI geocode functionality"""
        INPUT = 'geocode_input.csv'
        MODEL = 'Geocode'
        TRUE_OUTPUT = 'geocode_output.csv'
        SURNAME_HEADER = 'name'
        FIRST_NAME_HEADER = 'first_name'
        ZIP_HEADER = 'zcta5'
        self._run_model(
            self._DATA_FOLDER / INPUT,
            MODEL,
            self._CSV_OUTPUT_PATH,
            FIRST_NAME_HEADER,
            SURNAME_HEADER,
            ZIP_HEADER,
        )
        # Get our data
        df_generated = pd.read_csv(self._CSV_OUTPUT_PATH)
        df_true = pd.read_csv(self._DATA_FOLDER / TRUE_OUTPUT)
        # Compare values
        self._is_close_enough(df_generated, df_true)

    def test_surname(self):
        """Test GUI surname functionality"""
        INPUT = 'surname_input.csv'
        MODEL = 'Surname'
        TRUE_OUTPUT = 'surname_output.csv'
        SURNAME_HEADER = 'name'
        FIRST_NAME_HEADER = 'first_name'
        ZIP_HEADER = 'zcta5'
        self._run_model(
            self._DATA_FOLDER / INPUT,
            MODEL,
            self._CSV_OUTPUT_PATH,
            FIRST_NAME_HEADER,
            SURNAME_HEADER,
            ZIP_HEADER,
        )
        # Get our data
        df_generated = pd.read_csv(self._CSV_OUTPUT_PATH)
        df_true = pd.read_csv(self._DATA_FOLDER / TRUE_OUTPUT)
        # Compare values
        self._is_close_enough(df_generated, df_true)

    def test_surgeo(self):
        """Test GUI BISG functionality"""
        INPUT = 'surgeo_input.csv'
        MODEL = 'Surgeo (Surname + Geocode)'
        TRUE_OUTPUT = 'surgeo_output.csv'
        SURNAME_HEADER = 'name'
        FIRST_NAME_HEADER = 'first_name'
        ZIP_HEADER = 'zcta5'
        self._run_model(
            self._DATA_FOLDER / INPUT,
            MODEL,
            self._CSV_OUTPUT_PATH,
            FIRST_NAME_HEADER,
            SURNAME_HEADER,
            ZIP_HEADER,
        )
        # Get our data
        df_generated = pd.read_csv(self._CSV_OUTPUT_PATH)
        df_true = pd.read_csv(self._DATA_FOLDER / TRUE_OUTPUT)
        # Compare values
        self._is_close_enough(df_generated, df_true)

    def test_malformed(self):
        """Test custom input names"""
        INPUT = 'surgeo_input_misnamed.csv'
        MODEL = 'Surgeo (Surname + Geocode)'
        TRUE_OUTPUT = 'surgeo_output.csv'
        SURNAME_HEADER = 'info_name'
        FIRST_NAME_HEADER = 'info_first_name'
        ZIP_HEADER = 'info_zip'
        self._run_model(
            self._DATA_FOLDER / INPUT,
            MODEL,
            self._CSV_OUTPUT_PATH,
            FIRST_NAME_HEADER,
            SURNAME_HEADER,
            ZIP_HEADER,
        )
        # Get our data
        df_generated = pd.read_csv(self._CSV_OUTPUT_PATH)
        df_true = pd.read_csv(self._DATA_FOLDER / TRUE_OUTPUT)
        # Compare values
        self._is_close_enough(df_generated, df_true)

    def test_excel(self):
        """Test Excel input and output"""
        INPUT = 'surgeo_input.xlsx'
        MODEL = 'Surgeo (Surname + Geocode)'
        TRUE_OUTPUT = 'surgeo_output.xlsx'
        SURNAME_HEADER = 'name'
        FIRST_NAME_HEADER = 'first_name'
        ZIP_HEADER = 'zcta5'
        self._run_model(
            self._DATA_FOLDER / INPUT,
            MODEL,
            self._EXCEL_OUTPUT_PATH,
            FIRST_NAME_HEADER,
            SURNAME_HEADER,
            ZIP_HEADER,
        )
        # Get our data
        df_generated = pd.read_excel(self._EXCEL_OUTPUT_PATH, engine='openpyxl')
        df_true = pd.read_excel(self._DATA_FOLDER / TRUE_OUTPUT, engine='openpyxl')
        # Compare values
        self._is_close_enough(df_generated, df_true)


if __name__ == '__main__':
    unittest.main()
