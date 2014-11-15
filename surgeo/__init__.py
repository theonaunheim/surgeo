import sys


# Version check before imports. If not Python3, kill import
# python 34 = 50594032; python 30 = 0x03000000
if sys.hexversion < 0x03000000:
    raise ImportError('Python version of 3.0 or higher required.')


import importlib
import inspect
import logging
import os

import surgeo.calculate
import surgeo.gui
import surgeo.models
import surgeo.scripts
import surgeo.utilities

from surgeo.utilities.error import SurgeoError
from surgeo.utilities.redirector_adapter import RedirectorAdapter


def autoload_default_modules():
    '''Runs automatically. Loads modules in default and sets up databases'''
    # Import all model object from modules with '_model.py'
    parent_directory = os.path.dirname(os.path.abspath(__file__))
    file_list = os.listdir(parent_directory)
    for item in file_list:
        #TODO, does parent directory point us to the right spot
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


def construct_db():
    '''Does not run automatically. Creates database.'''
    db_path = os.path.join(os.path.expanduser('~'),
                           '.surgeo',
                           'surgeo.sqlite')
    if not os.path.exists(db_path):
        try:
            surgeo.adapter.write('Trying prefab database ...\n')
            pass  # Download dropbox link here
        except:
            surgeo.adapter.write('No prefab database availible ...\n')
            # Import all model object from modules with '_model.py'
            # TODO, does parent directory point us to the right spot
            parent_directory = os.path.dirname(os.path.abspath(__file__))
            file_list = os.listdir(parent_directory)
            for item in file_list:
                if not '_model.py' in item:
                    continue
                else:
                    item = ''.join(['surgeo.models.', item[:-3]])
                    module = importlib.import_module(item)
                    for name, member_object in inspect.getmembers(module):
                        if inspect.isclass(member_object):
                            if member_object.db_check() is False:
                                member_object.db_create()


def setup_directories():
    '''Runs automatically and sets up the directories to run Surgeo.'''
    for path in [os.path.join(os.path.expanduser('~'), '.surgeo'),
                 os.path.join(os.path.expanduser('~'), '.surgeo', 'models'),
                 os.path.join(os.path.expanduser('~'), '.surgeo', 'temp')]:
        if not os.path.exists(path):
            os.mkdir(path)


def setup_logger():
    '''Runs automatically and sets up logger.'''
    logging.basicConfig(format='%(asctime)s : %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p',
                        filename=(os.path.join(os.path.expanduser('~'),
                                               '.surgeo',
                                               'log.txt')),
                        filemode='w',
                        level=logging.DEBUG)


def setup_functions():
    '''Runs automatically and consolidates the necessary functions to run.'''
    global adapter
    adapter = RedirectorAdapter()
    setup_directories()
    setup_logger()
    autoload_default_modules()

