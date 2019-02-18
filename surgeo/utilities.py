'''Utilities.py contains convenience functions of all stripes.'''

import string

import pandas as pd


def normalize_surnames(series):
    '''This mangles a Series of surnames in accordance with census rules.

    In short this means:
        1. Convert to upper case;
        2. Strip certain characters or phrases:
            a. JR, JUNIOR, SR, SENIOR, III, THIRD, IV, FOURTH removed from
               ends of names; 
            b. Intervening blanks and punctuation removed; and,
            c. Numerals dropped.

    Parameters
    ----------
    series : pd.Series
        A pandas series of surname strings (dtype='O').
    
    Returns
    -------
    pd.Series
        A pandas series of normalized surnames (dtype='O').

    Raises
    ------
    TypeError
        If it is not given a pd.Series or composed of an 'O' dtype.

    Notes
    -----
    For detail see docs/2000_surname_methodology.pdf and
    docs/2010_surname_methodology.pdf.

    [1] Joshua Comenetz, "Frequently Occuring Surnames in the 2010 Census",
    2016.

    [2] David L. Word et al., " Demographic Aspects of Surnames from Census
    2000", 2000. 
    
    '''

    # Create a string of illegal characters to drop.
    CHARS_TO_DROP = (
        string.whitespace + 
        string.punctuation +
        string.digits
    )

    # Words to strip
    WORDS_TO_STRIP = [
        'JR' , 'JUNIOR',
        'SR' , 'SENIOR', 
        'III', 'THIRD', 
        'IV' , 'FOURTH',
    ]

    # Type checking
    if type(series) != pd.Series:
        raise TypeError("normalize_names() takes a series.")
    if series.dtype != 'O':
        raise TypeError("normalize_names() takes strings only.")
    
    # Capitalize
    series = series.str.upper()

    # Remove blanks, numerals, and punctuation via translation.
    translation_table = str.maketrans({character: None for character in CHARS_TO_DROP})
    series = series.str.translate(translation_table)

    # Create regex pattern and run regex to strip.
    # I.E. ['JR', 'JUNIOR'] -> '(JR$)|(JUNIOR$)'
    list_of_regexes = ['({}$)'.format(word) for word in WORDS_TO_STRIP]
    combined_regex_pattern = '|'.join(list_of_regexes)
    series = series.str.replace(combined_regex_pattern, '')

    return series
