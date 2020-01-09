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

    def test_run(self):
        with tempfile.NamedTemporaryFile(suffix='.csv') as out_file:
            p = subprocess.run(
                [
                    sys.executable, 
                    self._CLI_SCRIPT,
                    str(self._DATA_FOLDER / 'both_inputs.csv'),
                    out_file,
                    'surgeo',
                ], capture_output=True
            )
            print(p.stderr)
            print(out_file.read())
            reconstitued = pd.read_csv(out_file)
            print(reconstitued)



if __name__ == '__main__':
    unittest.main()
