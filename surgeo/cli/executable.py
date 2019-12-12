import sys
import pathlib
import warnings

import pandas as pd

# Jury rig path
path_dir = pathlib.Path(__file__).resolve().parents[2]
sys.path.append(str(path_dir))

import surgeo

from surgeo.cli.parser import SurgeoArgParser
from surgeo.utility.surgeo_exception import SurgeoException


def surgeo_main():
    # Get arguments
    args = SurgeoArgParser().get_parsed_args()
    input_path = pathlib.Path(args.input)
    output_path = pathlib.Path(args.output)
    model_type = args.type
    zcta_col = args.zcta_column
    sur_col = args.surname_column



if __name__ == '__main__':
    try:
        surgeo_main()
        sys.exit(0)
    except Exception as e:
        sys.stderr.write(str(e))
        sys.exit(1)
else:
    warnings.warn('executable.py is not intended to be imported.')