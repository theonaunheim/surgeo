#!/usr/local/bin/python3
#coding: utf-8
'''surgeo is a Bayesian Improved Surname Geocoding model written in Python 3.
 ___ _   _ _ __ __ _  ___  ___  
/ __| | | | '__/ _` |/ _ \/ _ \ 
\__ \ |_| | | | (_| |  __/ (_) |
|___/\__,_|_|  \__, |\___|\___/ 
               |___/            
               
Python code by Theo Naunheim. Model created by Mark N. Elliot et al.

############################################################################### 
License
###############################################################################

The MIT License (MIT)

Copyright (c) 2014 Theo Naunheim

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.'''

################################################################################
'''
import os
import sys

# Version check before most imports. If not updated, kill import or execution.
sys.stdout.write('Checking Python version ... \t\t\t')
PYTHON_3_4_HEXVERSION = 50594032
if sys.hexversion < PYTHON_3_4_HEXVERSION:
    # If executing raise base exception.
    if __name__ == "__main__":
        raise Exception('Python version of 3.4 or higher required.')
sys.stdout.write('{}OK{}\n'.format('\033[92m','\033[0m'))

# Add top-level namespace 'surgeo' for debug.
if __name__ == "__main__":
    # Get file location, get parent dir, get dir above that, append to path
    file_path = os.path.abspath(__file__)
    parent_dir = os.path.dirname(file_path)
    grandparent_dir = os.path.dirname(parent_dir)
    sys.path.append(grandparent_dir)
    # Now that surgeo module is on path, import
    import surgeo
'''
################################################################################
# Program
################################################################################

import surgeo
import argparse

def main(*args):
    '''This is the main application when running the program from a CLI.'''
    main

    
if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
    

