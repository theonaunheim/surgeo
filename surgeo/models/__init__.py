
import importlib
import inspect
import os
import sys

import surgeo

from surgeo.models.model_base import BaseModel
from surgeo.models.geocode_model import GeocodeModel
from surgeo.models.surname_model import SurnameModel


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

