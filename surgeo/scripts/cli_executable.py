#!/usr/local/bin/python3
#coding: utf-8
'''This is an executable wrapper for surgeo.'''
import sys

import surgeo


def cli_main(*args):
    '''This is the main application when running the program from a CLI.

    Parameters
    ----------
    --csv: string (x2)
        Takes an input filepath and an output filepath for csv processing.
    --model: string
        Takes a string which specifies the argument used.
    --string: string (number of string args variable)
        Takes a number of strings (# of strings depends on model type).
    --pipe: None
        This is an adapter to allow for Unix-like pipes.
    --setup: None
        This sets up databases for all models
    --verbose: None
        Takes no arguments, and prevents the suppression of output.

    Returns
    -------
    None: NoneType
        Settlement.
    Result string: string
        Both the '--string' and '--pipe' return a utf-8 string.
    Status string: string
        If '--verbose' various utf-8 strings are returned.

    Raises
    ------
    sqlite3.Error
        Can occur for any number of database-related reasons. Upon error,
        automatic rollback occurs, but the error is raised because it's
        probably symptomatic of a bigger problem.

    '''
# TEST eclipse egit plugin.
##### Parse arguments and setup
    parsed_args = surgeo.utilities.get_parser_args()
    surgeo.setup_functions()
    if parsed_args.verbose:
        surgeo.adapter.direct_to_null()
##### Pipe
    if parsed_args.pipe:
        surgeo.redirector.direct_to_stdout()
        
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
##### If no argument, GUI. Console should remain.
    elif not any([parsed_args.setup,
                  parsed_args.pipe,
                  parsed_args.simple,
                  parsed_args.complex,
                  parsed_args.file]):
        try:
            from surgeo.scripts import gui_executable
            gui_executable()
        except ImportError:
            raise SurgeoError('Cannot start GUI. Do you have ttk support?')

if __name__ == "__main__":
    sys.exit(cli_main(sys.argv[1:]))

