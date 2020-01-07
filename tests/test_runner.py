"""Script to create and run a test suite."""
import pathlib
import sys
import unittest

# Add surgeo directory to path
this_file = pathlib.Path(__file__).absolute()
repo_dir = this_file.parents[1]
path = str(repo_dir)
sys.path.append(path)

# Import test modules
# import app.test_cli
# import app.test_common_entry
# import app.test_gui
import models.test_base_model
import models.test_geocode_model
import models.test_surgeo_model
# import models.test_surname_model
# import utility.test_surgeo_exception

# List test modules
test_modules = [
    # app.test_cli,
    # app.test_common_entry,
    # app.test_gui,
    models.test_base_model,
    models.test_geocode_model,
    models.test_surgeo_model,
    # models.test_surname_model,
    # utility.test_surgeo_exception,
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
