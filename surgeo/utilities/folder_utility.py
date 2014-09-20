
import configparser
import os
import sys


def setup_folder(verbose):
    '''This method sets up a user folder and accompanying files.

    Args:
        verbose: whether the function prints updates to stdout
    Returns:
        None
    Raises:
        None

    '''

    if verbose is True:
        sys.stdout.write('Checking folder setup ... \t\t\t')
    home_dir_path = os.path.expanduser("~")
    data_dir_path = os.path.join(home_dir_path, '.surgeo')
    # Create file application data folder if needed.
    if not os.path.exists(data_dir_path):
        os.mkdir(data_dir_path)
    if verbose is True:
        sys.stdout.write('OK\n')
