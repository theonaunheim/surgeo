'''This is the main class for using the model in other Python3 programs.'''

import operator
import os
import sqlite3
import sys

import surgeo

################################################################################

class SurgeoModel(object):
    '''Contains data references and methods for running a BISG model.'''

    def __init__(self):
        # Load entire db to memory for performance DISK DATABSE
        db_path = os.path.join(os.path.expanduser('~'),
                               '.surgeo',
                               'census.db')
        if not os.path.exists(db_path):
            raise SurgeoError('DB does not exist. Run surgeo.data_setup().')
        self.db = sqlite3.connect(db_path)

    def guess_race(self, zcta, surname):
        '''zcta and surname goes in, race string.'''
        result = surgeo.model.model1.run_model(zcta,
                                               surname.upper(),
                                               self.db)
        return result.probable_race
        
    def race_data(self, zcta, surname):
        '''zcta and surname goes in, formatted SurgeoResult comes out.'''
        result = surgeo.model.model1.run_model(zcta,
                                               surname.upper(),
                                               self.db)
        return result
    
    def process_csv(self, filepath, verbose=True):
        '''This takes a csv filepath and creates new csv with race data.'''
        with open(filepath, 'r') as input_csv:
            lines = input_csv.readlines()
        # Check if line has header
        if 'zip' and 'name' in lines[0].split(','):
            zip_index = line[0].index('zip')
            name_index = line[0].index('name')
        #TODO
   

################################################################################                      
           
class SurgeoResult(object):
    '''Result class containing BISG data.'''
    def __init__(self, 
                 surname, 
                 zcta, 
                 hispanic, 
                 white, 
                 black, 
                 asian_or_pi, 
                 american_indian, 
                 multiracial):
        self.surname = surname
        self.zcta = zcta
        self.zip = zcta
        self.hispanic = hispanic
        self.white = white
        self.black = black
        self.asian_or_pi = asian_or_pi
        self.american_indian = american_indian
        self.multiracial = multiracial
        
    @property
    def probable_race(self):
        rank_dict = { 'Hispanic' : self.hispanic,
                      'White' : self.white,
                      'Black' : self.black,
                      'Asian / Pacific Islander' : self.asian_or_pi,
                      'American Indian / Alaskan Eskimo' : self.american_indian,
                      'Multiracial' : self.multiracial }
        most_probable_race = sorted(rank_dict.items(),
                                    key=operator.itemgetter(1),
                                    reverse=True)[0][0]
        return most_probable_race

    @property
    def probable_race_percentage(self):
        return max(self.hispanic,
                   self.white,
                   self.black,
                   self.asian_or_pi,
                   self.american_indian,
                   self.multiracial)
       
################################################################################
       
class SurgeoError(Exception):
    '''Custom error class for vanity's sake.'''

    def __init__(self, reason, response=None):
        self.reason = reason
        self.response = response
        Exception.__init__(self, reason)

    def __str__(self):
        return self.reason

