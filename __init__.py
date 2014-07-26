import os
import sys

# Version check before imports. If not proper version, kill import.
PYTHON_3_4_HEXVERSION = 50594032
if sys.hexversion < PYTHON_3_4_HEXVERSION:
    raise ImportError('Python version of 3.4 or higher required.')

# Kludgy fix for path   
file_path = os.path.abspath(__file__)
parent_dir = os.path.dirname(file_path)
grandparent_dir = os.path.dirname(parent_dir)
sys.path.append(grandparent_dir)

# Put SurgeoModel, SurgeoResult, and SurgeoError in surgeo namespace
from surgeo.utilities.class_file import SurgeoModel
from surgeo.utilities.class_file import SurgeoResult
from surgeo.utilities.class_file import SurgeoError

import surgeo.db
import surgeo.model
import surgeo.utilities

def data_setup(verbose=True):
    '''Downloads data needed to instantiate SurgeoModel.'''
    # Create necessary user data in home directory
    surgeo.utilities.setup_folder(verbose)
    # Setup surname db
    surgeo.db.setup_surname_table(verbose)
    # Setup race db
    surgeo.db.setup_geocode_table(verbose)
    # Reconstitute items supressed for confidentiality and index
    surgeo.db.reconstitute_data()
    # Remove zip and other unnecessary files
    surgeo.utilities.folder_cleanup()
