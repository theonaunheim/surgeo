#!/usr/local/bin/python3
#coding: utf-8
'''This is an executable wrapper for surgeo.'''
import inspect
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
        If not '--quiet' various utf-8 strings are returned.

    Raises
    ------
    sqlite3.Error
        Can occur for any number of database-related reasons. Upon error,
        automatic rollback occurs, but the error is raised because it's
        probably symptomatic of a bigger problem.

    '''

##### Parse arguments and setup
    # default args = csv, model, pipe, setup, string, verbose
    parsed_args = surgeo.utilities.parser.get_parser_args()
    # setup folders and the like
    surgeo.setup_functions()
    # If quiet, no output. Adapter shunts all output.
    if parsed_args.quiet:
        surgeo.adapter.direct_to_null()
##### Pipe
    if parsed_args.pipe:
        # Check what model
        if not parsed_args.model:
            raise surgeo.SurgeoError('No model specified for analysis.')
        # Instantiate model.
        model_name = parsed_args.model
        model_class = getattr(surgeo.models, model_name)
        model = model_class()
        try:
            while True:
                for line in sys.stdin:
                    try:
                        # Remove surrounding whitespace
                        stripped_line = line.strip()
                        raw_arguments = stripped_line.split()
                        argument_dict = {argument.split('=')[0]:
                                         argument.split('=')[1]
                                         for argument in raw_arguments}
                        result = model.get_result(**argument_dict)
                    except ValueError:
                        result = surgeo.utilities.result.Result().errorify()
                    surgeo.adapter.adaprint(result.as_string())
        except EOFError:
            pass
##### String
    elif parsed_args.string:
        if not parsed_args.model:
            raise surgeo.SurgeoError('No model specified for analysis.')
        # Instantiate model.
        model_name = parsed_args.model
        model_class = getattr(surgeo.models, model_name)
        model = model_class()
                        stripped_line = line.strip()
                        raw_arguments = stripped_line.split()
                        argument_dict = {argument.split('=')[0]:
                                         argument.split('=')[1]
                                         for argument in raw_arguments}
                        result = model.get_result(**argument_dict)
                    except ValueError:
                        result = surgeo.utilities.result.Result().errorify()
                    surgeo.adapter.adaprint(result.as_string())
##### Csv
    elif parsed_args.file:
        model = surgeo.SurgeoModel()
        infile = parsed_args.file[0]
        outfile = parsed_args.file[1]
        model.process_csv(infile, outfile)
##### Setup
    elif parsed_args.complex:
        model = surgeo.SurgeoModel()
        zcta = parsed_args.complex[0]
        surname = parsed_args.complex[1]
        result = model.race_data(zcta, surname)
        print(result.as_string)
##### If no argument, GUI. Console should remain.
    elif not any([parsed_args.setup,
                  parsed_args.pipe,
                  parsed_args.string,
                  parsed_args.csv]):
        try:
            from surgeo.scripts import gui_executable
            gui_executable()
        except ImportError:
            raise SurgeoError('Cannot start GUI. Do you have tk support?')

if __name__ == "__main__":
    sys.exit(cli_main(sys.argv[1:]))

