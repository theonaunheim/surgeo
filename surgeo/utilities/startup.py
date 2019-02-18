import logging
import importlib
import inspect
import os
import sys

import surgeo


def setup_default_modules():
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


def setup_all_dbs():
    '''Does not run automatically. Creates database.'''
    parent_directory = os.path.dirname(os.path.abspath(__file__))
    file_list = os.listdir(parent_directory)
    for item in file_list:
        if not '_model.py' in item:
            continue
        else:
            #remove '.py'
            item = ''.join(['surgeo.models.', item[:-3]])
            module = importlib.import_module(item)
            for _, member_object in inspect.getmembers(module):
                if inspect.isclass(member_object):
                    member_instance = member_object()
                    if member_instance.db_check() is False:
                        member_instance.db_create()


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
    surgeo.adapter = surgeo.utilities.redirector_adapter.RedirectorAdapter()
    setup_directories()
    setup_logger()
    setup_default_modules()
    # setup_all_dbs

