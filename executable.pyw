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
# Bootstrap
################################################################################

import os
import sys

# Kludgy fix for path   
file_path = os.path.abspath(__file__)
parent_dir = os.path.dirname(file_path)
grandparent_dir = os.path.dirname(parent_dir)
sys.path.append(grandparent_dir)

################################################################################
# Bootstrap
################################################################################

import argparse
import sys

import surgeo

def main(*args):
    '''This is the main application when running the program from a CLI.'''
    parsed_args = surgeo.utilities.get_parser_args()
##### Setup
    if parsed_args.setup:
        surgeo.data_setup(verbose=True)
    model = surgeo.SurgeoModel()
    # Pipe
    if parsed_args.pipe:
        try:
            while True:
                for line in sys.stdin:
                    # Remove surrounding whitespace
                    line.strip()
                    zcta, surname = line.split()
                    result = model.race_data(zcta, surname)
                    sys.stdout.write(result.as_string())
        except EOFError:
            pass  
##### Simple
    elif parsed_args.simple:
        zcta = parsed_args.simple[0]
        surname = parsed_args.simple[1]
        race = model.guess_race(zcta, surname)
        print(race)    
##### Complex
    elif parsed_args.complex:
        zcta = parsed_args.complex[0]
        surname = parsed_args.complex[1]
        result = model.race_data(zcta, surname)
        print(result.to_string())  
##### File
    elif parsed_args.file:
        infile = parsed_args.file[0]
        outfile = parsed_args.file[1]
        model.process_csv(infile, outfile)
##### GUI
    else:
        gui = surgeo.gui.Gui(model)
        gui.root.mainloop()
    
if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
    

