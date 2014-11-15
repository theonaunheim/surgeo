'''This creates a parser and is invoked from main program.'''
import argparse


def get_parser_args():
    parser = argparse.ArgumentParser(description='Get Surgeo arguments.')
    # File arguments
    parser.add_argument('--csv',
                        nargs=2,
                        help='Takes input file and output file as arguments.',
                        dest='csv')
    # Model argument
    parser.add_argument('--model',
                        nargs=1,
                        help='Specifies model used.',
                        dest='model')
    # String
    parser.add_argument('--string',
                        nargs='*',
                        help='Takes arguments and returns string.',
                        dest='string')
    # Pipe argument
    parser.add_argument('--pipe',
                        action='store_true',
                        help='Takes no arguments. Used only for piping.',
                        dest='pipe')
    # Setup argument
    parser.add_argument('--setup',
                        action='store_true',
                        help='Takes no inputs and sets up database.',
                        dest='setup')
    # Verbosity
    parser.add_argument('--verbose',
                        action='store_true',
                        help='Unsuppresses output.',
                        dest='verbose')
    # Parse and return args
    parsed_args = parser.parse_args()
    return parsed_args

