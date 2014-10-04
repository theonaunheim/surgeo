import sys

# Version check before imports. If not Python3, kill import
if sys.hexversion < 34014960:
    raise ImportError('Python version of 3.4 or higher required.')

import logging
import os

import surgeo.models
import surgeo.utilities

from surgeo.utilities.redirector_class import Redirector
from surgeo.utilities.download_bar import graphical_download


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


def construct_db(verbose=True):
    '''Does not run automatically. Creates database.'''
    if verbose is False:
        surgeo.redirector.direct_to_null()
    db_path = os.path.join(os.path.expanduser('~'),
                           '.surgeo',
                           'surgeo.sqlite')
    if not os.path.exists(db_path):
        try:
            surgeo.redirector.add('Trying prefab database ...')
            pass  # Download dropbox link here
        except:
            surgeo.redirector.add('No prefab database availible ...')
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
    surgeo.redirector.direct_to_stdout()


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
                                               'surgeo_log.txt')),
                        filemode='w',
                        level=logging.DEBUG)


def setup_functions():
    '''Runs automatically and consolidates the necessary functions to run.'''
    surgeo.redirector = Redirector()
    surgeo.redirector.start()
    setup_directories()
    setup_logger()
    autoload_default_modules()

# Bad, bad Python to run on import, but oh so convenient.
setup_functions()

