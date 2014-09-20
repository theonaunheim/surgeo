import sys

# Version check before imports. If not Python3, kill import
if sys.hexversion < 0x03000000:
    raise ImportError('Python version of 3.0 or higher required.')

import logging
import os

import surgeo.models
import surgeo.utilities

# Setup folders
for path in [ os.path.join(os.path.expanduser('~'), '.surgeo'),
              os.path.join(os.path.expanduser('~'), '.surgeo', 'models'),
              os.path.join(os.path.expanduser('~'), '.surgeo', 'temp') ]:
    if not os.path.exists(path):
        os.mkdir(path)

# Setup logger
logging.basicConfig(format='%(asctime)s : %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p',
                    filename=(os.path.join(os.path.expanduser('~'),
                                           '.surgeo',
                                           'surgeo_log.txt')),
                    filemode='w',
                    level=logging.DEBUG)
