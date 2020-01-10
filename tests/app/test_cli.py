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

    def test_surgeo_cli(self):
        # Make closed temporary file
        input_path = str(self._DATA_FOLDER / 'both_inputs.csv')
        subprocess.run([
            sys.executable, 
            self._CLI_SCRIPT,
            input_path,
            self._CSV_OUTPUT_PATH,
            'surgeo'
        ])
        df_new = pd.read_csv(self._CSV_OUTPUT_PATH)
        df_actual = pd.read_csv(self._DATA_FOLDER / 'surgeo_output.csv')
        self.assertTrue(df_new.equals(df_actual))
        

    def test_malformed(self):
        pass

    def test_sur_cli(self):
        pass

    def test_geo_cli(self):
        pass

    def test_excel(self):
        pass
        # both inputs

if __name__ == '__main__':
    unittest.main()
