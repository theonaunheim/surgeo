import argparse


class SurgeoArgParser(object):

    def get_parsed_args(self):
        parser = argparse.ArgumentParser(description='Get Surgeo arguments.')
        parser.add_argument(
            'input',
            help='Input CSV or XLSX of data.',
        )
        parser.add_argument(
            'output',
            help='Output CSV or XLSX of data.',
        )
        parser.add_argument(
            'type',
            help='The model type being run ("sur", "geo" or "surgeo")',
        )
        parser.add_argument(
            '--zcta_column',
            help='The input column to analyze as ZCTA/ZIP)',
            dest='zcta_column'
        )
        parser.add_argument(
            '--surname_column',
            help='The input column to analyze as surname")',
            dest='surname_column'
        )
        parsed_args = parser.parse_args()
        return parsed_args
