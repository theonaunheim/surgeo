'''Sets up a user folder and accompanying files.'''

import configparser
import os
import sys

def setup_folder(verbose):
    '''This method sets up a user folder and accompanying files.'''
    if verbose == True:
        sys.stdout.write('Checking folder setup ... \t\t\t')
    home_dir_path = os.path.expanduser("~")
    data_dir_path = os.path.join(home_dir_path, '.surgeo')
    # Create file application data folder if needed.
    if not os.path.exists(data_dir_path):
        os.mkdir(data_dir_path)
    # Create configuration file if needed
    config_path = os.path.join(data_dir_path, 'configuration.txt')
    if not os.path.exists(config_path):
        parser_instance = configparser.ConfigParser()
        #
        parser_instance['GENERAL'] = {'placeholder' : 'placetext'}
        parser_instance['DATA'] = {'url' : 
            'http://www.census.gov/genealogy/www/data/2000surnames/names.zip'}
        #
        with open(config_path, 'w+') as config_file:
            parser_instance.write(config_file)
    # 'OK' in green
    if verbose == True:
        sys.stdout.write('{}OK{}\n'.format('\033[92m','\033[0m'))

