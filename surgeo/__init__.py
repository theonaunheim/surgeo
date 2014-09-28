import sys

# Version check before imports. If not Python3, kill import
if sys.hexversion < 34014960:
    raise ImportError('Python version of 3.4 or higher required.')

import logging
import os

import surgeo.models
import surgeo.utilities


def setup_directories():
    '''This function sets up the necessary directories to run Surgeo.'''
    for path in [ os.path.join(os.path.expanduser('~'), '.surgeo'),
                  os.path.join(os.path.expanduser('~'), '.surgeo', 'models'),
                  os.path.join(os.path.expanduser('~'), '.surgeo', 'temp') ]:
        if not os.path.exists(path):
            os.mkdir(path)

def setup_logger():
    logging.basicConfig(format='%(asctime)s : %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p',
                        filename=(os.path.join(os.path.expanduser('~'),
                                               '.surgeo',
                                               'surgeo_log.txt')),
                        filemode='w',
                        level=logging.DEBUG)

def autoload_default_modules():
    '''Loads modules in default and sets up databases'''
    # Import all model object from modules with '_model.py'
    parent_directory = os.path.dirname(os.path.abspath(__file__))
    file_list = os.listdir(parent_directory)
    for item in file_list:
        if not '_model.py' in item:
            continue
        else:
            item = ''.join(['surgeo.models.', item[:-3]])
            module = importlib.import_module(item) 
            for member_name, member_object in inspect.getmembers(module):
                if inspect.isclass(member_object):
                    setattr(sys.modules['surgeo.models'],
                            member_name,
                            member_object)
                    # Check validity
                    if member_object.db_check() is False:
                        member_object.db_create()

def setup_functions():
    setup_directories()
    setup_logger()
    autoload_default_modules()

