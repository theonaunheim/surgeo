"""Script to create and run a test suite."""
import pathlib
import sys
import unittest

import models.test_base_model

# Add pyfair directory to path
this_file = pathlib.Path(__file__).absolute()
repo_dir = this_file.parents[1]
path = str(repo_dir)
sys.path.append(path)

# Import test modules

# List test modules
test_modules = [
    models.test_base_model,
]

# Create loader and suite
loader = unittest.TestLoader()
suite = unittest.TestSuite()

# Add to suite
for test_module in test_modules:
    loaded_test = loader.loadTestsFromModule(test_module)
    suite.addTest(loaded_test)

# Create runner and run
runner = unittest.TextTestRunner(verbosity=5)
result = runner.run(suite)
