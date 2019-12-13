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
        parser = SurgeoArgParser()
        args = parser.get_parsed_args()
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
            raise SurgeoException(
                f'File ending for "{self._input_path}" not '
                'recognized. Please use .csv or .xlsx.'
            )
        return df

    def _run_geo(self, df):
        model = GeocodeModel()
        if self._zcta_col is not None:
            target = df[self._zcta_col]
            result = model.get_probabilities(target)
        else:
            target = df['zcta5']
            result = model.get_probabilities(target)
        return result

    def _run_sur(self, df):
        model = SurnameModel()
        if self._sur_col is not None:
            target = df[self._sur_col]
            result = model.get_probabilities(target)
        else:
            target = df['name']
            result = model.get_probabilities(target)
        return result

    def _run_surgeo(self, df):
        model = SurgeoModel()
        if self._zcta_col is not None:
            geo_target = df[self._zcta_col]
        else:
            geo_target = df['zcta5']
        if self._sur_col is not None:
            sur_target = df[self._sur_col]
        else:
            sur_target = df['name']
        result = model.get_probabilities(sur_target, geo_target)
        return result

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
            return result_df
        except KeyError:
            raise SurgeoException(
                f'"{model_type}" is not valid model type. '
                'Please use "sur", "geo", or "surgeo".'
            )            

    def _write_df(self, df):
        suffix = self._output_path.suffix
        if suffix == '.xlsx':
            df.to_excel(self._output_path, index=False)
        elif suffix == '.csv':
            df.to_csv(self._output_path, index=False)
        else:
            raise SurgeoException(
                f'"{self._output_path}" is not a valid. '
                'Please specify a path ending in ".csv" or ".xlsx".'    
            )

    def surgeo_main(self):
        input_df = self._load_df()
        processed_df = self._process_df(input_df)
        self._write_df(processed_df)        


if __name__ == '__main__':
    try:
        app = SurgeoApplication()
        app.surgeo_main()
        sys.exit(0)
    except Exception as e:
        raise e
        sys.exit(1)
