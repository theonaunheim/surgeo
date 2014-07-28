import os
import sys

# Version check before imports. If not Python3, kill import
if sys.hexversion < 0x03000000:
    raise ImportError('Python version of 3.0 or higher required.')

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
import surgeo.gui
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
    # Fetch logo for GUI
    surgeo.utilities.fetch()
    # Remove zip and other unnecessary files
    surgeo.utilities.folder_cleanup()
    
