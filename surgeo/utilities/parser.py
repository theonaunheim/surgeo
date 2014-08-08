
import argparse

def get_parser_args():
    '''This creates a parser and is invoked from main program.'''
    parser = argparse.ArgumentParser(description='Get Surgeo arguments.')
    # File argumets
    parser.add_argument('--file',
                        nargs=2,
                        help='Takes input file and output file as arguments.',
                        dest='file')
    # Simple arguments
    parser.add_argument('--simple',
                        nargs=2,
                        help='Takes zip and surname, returns string.',
                        dest='simple')
    # Complex arguments
    parser.add_argument('--complex',
                        nargs=2,
                        help='Takes zip and name, returns csv string.',
                        dest='complex')
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
    #parse and return args  
    parsed_args = parser.parse_args()
    return parsed_args

