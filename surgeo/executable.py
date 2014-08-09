#!/usr/local/bin/python3
#coding: utf-8
'''This is an executable wrapper for surgeo.'''

################################################################################
# Bootstrap
################################################################################

import os
import sys

# Kludgy fix for path if you want to execute outside of path.  
##file_path = os.path.abspath(__file__)
##parent_dir = os.path.dirname(file_path)
##grandparent_dir = os.path.dirname(parent_dir)
##sys.path.append(grandparent_dir)

################################################################################
# Bootstrap
################################################################################

import argparse
import os
import sys

import surgeo

def main(*args):
    '''This is the main application when running the program from a CLI.
    
    Args:
        --setup: (0 args) downloads and creates database for model instantiation
        --pipe: (0 args) takes stdin, processes, and sends to stdout
        --file: (2 args) takes 1. filepath input csv 2. filepath output csv
        --simple: (2 args) takes zip and surname, returns text string
        --complex: (2 args) takes zip and surname, returns detailed string
    Returns:
        --setup: None
        --pipe: long text string
        --file: None (output to csv file)
        --simple: text string ('White')
        --complex: long text string
    Raises:
        None
    
    '''
    parsed_args = surgeo.utilities.get_parser_args()
##### Setup
    if parsed_args.setup:
        surgeo.data_setup(verbose=True)
##### Pipe
    if parsed_args.pipe:
        model = surgeo.SurgeoModel()
        try:
            while True:
                for line in sys.stdin:
                    try:
                        # Remove surrounding whitespace
                        line.strip()
                        zcta, surname = line.split()
                        result = model.race_data(zcta, surname)
                    except ValueError:
                        result = model.race_data('00000', 'BAD_NAME')
                    print(result.as_string)
        except EOFError:
            pass  
##### Simple
    elif parsed_args.simple:
        model = surgeo.SurgeoModel()
        zcta = parsed_args.simple[0]
        surname = parsed_args.simple[1]
        race = model.guess_race(zcta, surname)
        print(race)    
##### Complex
    elif parsed_args.complex:
        model = surgeo.SurgeoModel()
        zcta = parsed_args.complex[0]
        surname = parsed_args.complex[1]
        result = model.race_data(zcta, surname)
        print(result.as_string)  
##### File
    elif parsed_args.file:
        model = surgeo.SurgeoModel()
        infile = parsed_args.file[0]
        outfile = parsed_args.file[1]
        model.process_csv(infile, outfile)
    elif not any([ parsed_args.setup,
                   parsed_args.pipe,
                   parsed_args.simple,
                   parsed_args.complex,
                   parsed_args.file ]):
        print('No arguments given. Try \'--help\'?')
    
if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
    

