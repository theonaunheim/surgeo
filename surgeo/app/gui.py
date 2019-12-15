"""Script containing a basic GUI program."""

import pathlib
import sys
import traceback

import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog as filedialog
import tkinter.messagebox as messagebox

import pandas as pd

# Jury rig path
path_dir = pathlib.Path(__file__).resolve().parents[2]
sys.path.append(str(path_dir))

import surgeo

from surgeo.utility.surgeo_exception import SurgeoException
from surgeo import GeocodeModel
from surgeo import SurgeoModel
from surgeo import SurnameModel


class SurgeoGUI(object):

    def __init__(self):
        self._objects = {'root': tk.Tk()}

    def main(self):
        self._window_setup()
        self._add_widgets()
        self._objects['root'].mainloop()

    def _window_setup(self):
        self._objects['frame'] = tk.Frame(master=self._objects['root'])
        self._objects['root'].title(f"Surgeo v.{surgeo.VERSION}")
        self._objects['root'].minsize(700, 150)
        # Add icon
        self._objects['root'].tk.call(
            'wm', 
            'iconphoto', 
            self._objects['root']._w, 
            tk.PhotoImage(file=str(path_dir / 'surgeo' / 'static' / 'logo.gif'))
        )

    def _select_input(self):
        input_filename = filedialog.askopenfilename(
            title='Select Input Path',
            filetypes=(
                ('csv files' , '*.csv' ),
                ('Excel XLSX', '*.xlsx'),
                ('Excel XLS' , '*.xls' )
            )
        )
        self._objects['input_var'].set(input_filename)

    def _select_output(self):
        output_filename = filedialog.asksaveasfilename(
            title='Select Output Path',
            filetypes=(
                ('csv files' , '*.csv' ),
                ('Excel XLSX', '*.xlsx'),
            )
        )
        self._objects['output_var'].set(output_filename)

    def _add_widgets(self):
        # Root alias to save typing
        root = self._objects['root']
        #######################################################################
        # Row 1
        #######################################################################
        # File selection label
        select_label = ttk.Label(root, text='Input File')
        select_label.grid(row=0, column=0, padx=10, sticky='w')
        self._objects['select_label'] = select_label
        # File Selection Path
        input_var = tk.StringVar()
        self._objects['input_var'] = input_var
        select_path_text = ttk.Label(
            root,
            borderwidth=1,
            relief='solid',
            width=80,
            textvariable=input_var,
        )
        self._objects['select_path_text'] = select_path_text
        select_path_text.grid(row=0, column=1, padx=10, stick='w')
        # File selection button
        select_button = ttk.Button(
            root, 
            text='Select',
            command=self._select_input,
        )
        select_button.grid(row=0, column=2, padx=10, sticky='w')
        self._objects['select_button'] = select_button
        #######################################################################
        # Row 2
        #######################################################################
        # Output file label
        output_label = ttk.Label(root, text='Output File')
        output_label.grid(row=1, column=0, padx=10, sticky='w')
        self._objects['output_label'] = output_label
        # File Output path
        output_var = tk.StringVar()
        self._objects['output_var'] = output_var
        output_path_text = ttk.Label(
            root,
            borderwidth=1,
            relief='solid',
            width=80,
            textvariable=output_var,
        )
        self._objects['output_path_text'] = output_path_text
        output_path_text.grid(row=1, column=1, padx=10, sticky='w')
        # Output selection button
        output_button = ttk.Button(
            root, 
            text='Select',
            command=self._select_output,
        )
        output_button.grid(row=1, column=2, padx=10, sticky='w')
        self._objects['output_button'] = output_button
        #######################################################################
        # Row 3
        #######################################################################
        # Surname selection
        surname_label = ttk.Label(
            root, 
            text='Surname Column Header', 
        )
        surname_label.grid(row=2, column=0, padx=10, sticky='w')
        self._objects['surname_label'] = surname_label
        name_var = tk.StringVar()
        self._objects['name_var'] = name_var
        surname_entry = ttk.Entry(
            root,
            text='Enter Name Column Header',
            textvariable=name_var,
        )
        surname_entry.grid(row=2, column=1, padx=10, sticky='w')
        self._objects['surname_entry'] = surname_entry
        #######################################################################
        # Row 4
        #######################################################################
        # ZCTA selection
        zcta_label = ttk.Label(
            root, 
            text='ZIP/ZCTA Column Header', 
        )
        zcta_label.grid(row=3, column=0, padx=10, sticky='w')
        self._objects['zcta_label'] = zcta_label
        zip_var = tk.StringVar()
        self._objects['zip_var'] = zip_var
        zcta_entry = ttk.Entry(
            root,
            text='Enter ZIP/ZCTA Column Header',
            textvariable=zip_var,
        )
        zcta_entry.grid(row=3, column=1, padx=10, pady=3, sticky='w')
        self._objects['zcta_entry'] = zcta_entry
        #######################################################################
        # Row 5
        #######################################################################
        # Model selector
        model_label = ttk.Label(root, text='Model Type')
        model_label.grid(row=4, column=0, padx=10, sticky='w')
        self._objects['model_label'] = model_label
        model_var = tk.StringVar()
        self._objects['model_var'] = model_var
        model_selector = ttk.OptionMenu(
            root,
            model_var,
            'Surgeo (Surname + Geocode)',
            'Surname',
            'Geocode',
        )
        model_selector.grid(row=4, column=1, padx=10, sticky='w')
        self._objects['model_selector'] = model_selector
        #######################################################################
        # Row 6
        #######################################################################
        # Model selector
        execute_button = ttk.Button(
            root, 
            text='Execute',
            command=self._execute,
        )
        execute_button.grid(row=5, column=2, padx=10, sticky='w')
        self._objects['execute_button'] = execute_button

    def _check_inputs(self, df):
        """Raise error if improper column names given"""
        name_var   = self._objects['name_var']
        zip_var    = self._objects['zip_var']
        model_var  = self._objects['model_var']
        if model_var == 'Geocode':
            if zip_var not in df.columns:
                raise SurgeoException(f'{name_var} not in input data.')
        elif model_var == 'Surname':
            if name_var not in df.columns:
                raise SurgeoException(f'{name_var} not in input data.')
        else:
            if zip_var not in df.columns:
                raise SurgeoException(f'{name_var} not in input data.')
            if name_var not in df.columns:
                raise SurgeoException(f'{name_var} not in input data.')

    def _load_df(self, input_path):
        """This creates a dataframe based on self._input_path"""
        path = pathlib.Path(input_path)
        suffix = path.suffix
        # If it's excel, read_excel()
        if suffix == '.xlsx' or suffix == 'xls':
            df = pd.read_excel(path)
        # If CSV, read read_csv()
        elif suffix == '.csv':
            df = pd.read_csv(path)
        # If path is unrecognized, throw error
        else:
            raise SurgeoException(
                f'File ending for "{path}" not '
                'recognized. Please use .csv or .xlsx.'
            )
        return df

    def _execute(self):
        # Get variables
        input_var  = self._objects['input_var']
        output_var = self._objects['output_var']
        name_var   = self._objects['name_var']
        zip_var    = self._objects['zip_var']
        model_var  = self._objects['model_var']
        try:
            df = self._load_df(input_var)
            self._check_inputs(df)            
        except Exception:
            err = traceback.format_exc()
            messagebox.showerror('Error', err)


if __name__ == '__main__':
    # Error handling within application.
    gui = SurgeoGUI()
    gui.main()
