"""Script to create and run a test suite."""
import unittest

from surgeo import app
from surgeo import models

# Import test modules
import app.test_cli
import app.test_gui
import models.test_base_model
import models.test_bifsg_model
import models.test_first_name_model
import models.test_geocode_model
import models.test_surgeo_model
import models.test_surname_model

# List test modules
test_modules = [
    app.test_cli,
    app.test_gui,
    models.test_base_model,
    models.test_bifsg_model,
    models.test_first_name_model,
    models.test_geocode_model,
    models.test_surgeo_model,
    models.test_surname_model,
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
