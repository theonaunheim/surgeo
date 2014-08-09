'''surgeo is a Bayesian Improved Surname Geocoding model written in Python 3.
 ___ _   _ _ __ __ _  ___  ___  
/ __| | | | '__/ _` |/ _ \/ _ \ 
\__ \ |_| | | | (_| |  __/ (_) |
|___/\__,_|_|  \__, |\___|\___/ 
               |___/            
               
Python code by Theo Naunheim. Model created by Mark N. Elliot et al.

############################################################################### 
License
###############################################################################

The MIT License (MIT)

Copyright (c) 2014 Theo Naunheim

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

'''

import os
import sys

# Version check before imports. If not Python3, kill import
if sys.hexversion < 0x03000000:
    raise ImportError('Python version of 3.0 or higher required.')

# Put SurgeoModel, SurgeoResult, and SurgeoError in surgeo namespace
from surgeo.utilities.class_file import SurgeoModel
from surgeo.utilities.class_file import SurgeoResult
from surgeo.utilities.class_file import SurgeoError
from surgeo.utilities.class_file import ErrorResult

import surgeo.db
import surgeo.model
import surgeo.utilities

def data_setup(verbose=True):
    '''Downloads data needed to instantiate SurgeoModel.
    
    Args:
        verbose: True/False determines whether text is output.
    Returns:
        None
    Raises:
        None
    
    '''
    
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


