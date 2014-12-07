import importlib
import inspect
import io
import os
import sys

import surgeo.models


def load_model(model_module_name):
    '''This loads a user-defined module in models namespace.'''
    model_folder_path = os.path.join(os.path.expanduser('~'),
                                     '.surgeo',
                                     'models')
    sys.path.append(model_folder_path)
    for filename in os.listdir(model_folder_path):
        if model_module_name in filename:
            module = importlib.import_module(model_module_name)
            for member_name, member_object in inspect.getmembers(module):
                if inspect.isclass(member_object):
                    setattr(sys.modules['surgeo.models'],
                            member_name,
                            member_object)
                    # Db setup
                    if member_object.db_check() is False:
                        member_object.db_create()
        else:
            raise surgeo.SurgeoError('No module availible by that name.')


def summarize_models():
    '''Presents a summary of all model arguments as a string.'''
    string_buffer = io.StringIO('')
    parent_directory = os.path.dirname(os.path.abspath(__file__))
    file_list = os.listdir(parent_directory)
    member_list = []
    string_buffer.write('\n')
    for item in file_list:
        # Only models.
        if not 'model' in item.lower():
            continue
        module_name = item[:-3]
        module = getattr(surgeo.models, module_name)
        for member_name, member_object in inspect.getmembers(module):
            # Ensure we are getting the model only
            if not 'Model' in member_name:
                continue
            if not member_name in member_list:
                member_list.append(member_name)
                string_buffer.write(member_name)
                string_buffer.write('.get_result_object')
                string_buffer.write('(')
                function_ref = member_object.get_result_object
                arg_list = inspect.getargspec(function_ref)[0]
                arg_list_2 = []
                for arg in arg_list:
                    arg_list_2.append(arg)
                string_buffer.write(', '.join(arg_list_2))
                string_buffer.write(')\n')
    summary_string = string_buffer.getvalue()
    return summary_string

