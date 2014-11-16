#!/usr/local/bin/python3
#coding: utf-8
'''This is an executable wrapper for Surgeo.'''
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

    # Parse arguments and setup (csv, model, pipe, setup, string, verbose)
    parsed_args = surgeo.utilities.parser.get_parser_args()
    # setup folders and the like
    surgeo.setup_functions()
    # If quiet, no output. Adapter shunts all output.
    if parsed_args.quiet:
        surgeo.adapter.direct_to_null()
    # Pipe argument
    cli_pipe_subroutine(parsed_args)
    # String argument
    cli_string_subroutine(parsed_args)
    # Setup argument
    cli_setup_subroutine(parsed_args)
    # Gui argument (no arguments)
    cli_gui_subroutine(parsed_args)

def cli_pipe_subroutine(parsed_args):
    '''For the "Pipe" argument.'''
    if parsed_args.pipe:
        # Check what model
        if not parsed_args.model:
            raise surgeo.SurgeoError('No model specified.')
        # Instantiate model.
        model_name = parsed_args.model[0]
        module_name = parsed_args.model.lower().replace('model', '_model')
        model_module = getattr(surgeo.models, module_name)
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

def cli_string_subroutine(parsed_args):
    '''"String" argument analyzes and returns a string.'''
    if parsed_args.string:
        if not parsed_args.model:
            raise surgeo.SurgeoError('No model specified.')
        # Instantiate model.
        model_name = parsed_args.model[0]
        module_name = parsed_args.model.lower().replace('model', '_model')
        model_module = getattr(surgeo.models, module_name)
        model_class = getattr(surgeo.models, model_name)
        model = model_class()
        # Convert arguments to dict
        raw_arguments = parsed_args.string.split()
        argument_dict = {argument.split('=')[0]:
                         argument.split('=')[1]
                         for argument in raw_arguments}
        result = model.get_result(**argument_dict)
        surgeo.adapter.adaprint(result.as_string())

def cli_setup_subroutine(parsed_args):
    '''"Setup" argument causes all databases to be created.'''
    if parsed_args.setup:
        if not parsed_args.model:
            raise surgeo.SurgeoError('No model specified.')
        # Instantiate model.
        model_name = parsed_args.model[0]
        module_name = parsed_args.model[0].lower().replace('model', '_model')
        model_module = getattr(surgeo.models, module_name)
        model_class = getattr(model_module, model_name)
        model = model_class()
        # If the model is bad
        if not model.db_check():
            model.db_create()

def cli_gui_subroutine(parsed_args):
    '''If no arguments, run the GUI.'''
    if not any([parsed_args.setup,
                parsed_args.pipe,
                parsed_args.string,
                parsed_args.csv]):
        try:
            from surgeo.scripts import gui_executable
            gui_executable()
        except ImportError:
            raise surgeo.SurgeoError('Cannot start GUI. Do you have tk support?')

if __name__ == "__main__":
    sys.exit(cli_main(sys.argv[1:]))

