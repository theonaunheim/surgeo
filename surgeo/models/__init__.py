
import importlib
import inspect
import os
import sys

from surgeo.utilities.error_class import SurgeoError

def load_model(model_module_name):
    '''This loads a user-defined module in models namespace.'''
    model_folder_path = os.path.join(os.path.expanduser('~'),
                                     '.surgeo',
                                     'models')
    sys.path.append(model_folder_path)
    for filename in os.listdir(model_folder_path):
        if model_module_name == module_name:
            module = importlib.import_module(model_module_name)
            for member_name, member_object in inspect.getmembers(module):
                if inspect.isclass(member_object):
                    setattr(sys.modules['surgeo.models'],
                            member_name,
                            member_object)
        else:
            raise SurgeoError('No module availible by that name.')
       
def autoload_default_modules():
    '''This is stuffed in a function to keep namespace clean.'''
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

autoload_default_modules()

