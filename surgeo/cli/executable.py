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
from surgeo import GeocodeModel
from surgeo import SurgeoModel
from surgeo import SurnameModel


class SurgeoApplication(object):

    def __init__(self):
        args = SurgeoArgParser().get_parsed_args()
        self._input_path = pathlib.Path(args.input)
        self._output_path = pathlib.Path(args.output)
        self._model_type = args.type.lower()
        self._zcta_col = args.zcta_column
        self._sur_col = args.surname_column

    def _load_df(self):
        suffix = self._input_path.suffix
        if suffix == '.xlsx' or suffix == 'xls':
            df = pd.read_excel(self._input_path)
        elif suffix == '.csv':
            df = pd.read_csv(self._input_path)
        else:
            raise SurgeoException(f'File ending {suffix} not recognized.')
        return df

    def _run_geo(self, df):
        model = GeocodeModel()
        if self._zcta_col is not None:
            target = df[self._zcta_col]
            result = model.predict_prob(target)
        else:
            target = df['zcta5']
            result = model.predict_prob(target)
        return result

    def _run_sur(self):
        pass

    def _run_surgeo(self):
        pass

    def _process_df(self, df):
        model_type = self._model_type
        type_map = {
            'sur'   : self._run_sur,
            'geo'   : self._run_geo,
            'surgeo': self._run_surgeo,
        }
        try:
            process_func = type_map[model_type]
            result_df = process_func(df)
            return df
        except KeyError:
            raise SurgeoException(f'{model_type} is not valid model type. '
                                'Please use "sur", "geo", or "surgeo".')            

    def surgeo_main(self):
        # Load df
        input_df = self._load_df()
        processed_df = self._process_df(input_df)
        processed_df.to_csv(self._output_path)


if __name__ == '__main__':
    try:
        app = SurgeoApplication()
        app.surgeo_main()
        sys.exit(0)
    except Exception as e:
        sys.stderr.write(str(e))
        sys.exit(1)
