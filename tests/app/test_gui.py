import pathlib
import subprocess
import unittest

import surgeo.app.cli


class TestSurgeoCLI(unittest.TestCase):

    _FILE_PATH = surgeo.app.cli.__file__

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_run(self):
        p = subprocess.run(['python', self._FILE_PATH], capture_output=True)
        print(p.stderr)

if __name__ == '__main__':
    unittest.main()
