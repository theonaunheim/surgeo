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
    

