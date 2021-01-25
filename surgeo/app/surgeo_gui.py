"""Script containing a basic GUI program."""

import pathlib
import sys
import traceback

import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog as filedialog
import tkinter.messagebox as messagebox

import pandas as pd

import surgeo

from surgeo.utility.surgeo_exception import SurgeoException
from surgeo.models.bifsg_model import BIFSGModel
from surgeo.models.first_name_model import FirstNameModel
from surgeo.models.geocode_model import GeocodeModel
from surgeo.models.surgeo_model import SurgeoModel
from surgeo.models.surname_model import SurnameModel


class SurgeoGUI(object):
    """A GUI application class to function as an executable

    This script creates a single window tkinter application. This
    application allows a user to specify inputs/outputs, specify which
    model that they want to run, and then define the column headers for the
    ZCTA, first name, and surname fields as applicable. It then runs the
    model and stores the results in a file.

    It also has various helper functions to integrate the surgeo logic
    within the program.

    It currently supports .xlsx, .xls, and .csv inputs; it currently
    supports .xlsx and .csv outputs.

    """

    def __init__(self):
        # Create dictionary to track all objects and populate with root
        self._objects = {'root': tk.Tk()}
        # https://cx-freeze.readthedocs.io/en/latest/faq.html#using-data-files
        # If it's frozen, we can't use __file__
        if getattr(sys, 'frozen', False):
            # The application is frozen
            freeze_package = pathlib.Path(sys.executable).parents[0]
            self._package_root = freeze_package / 'Lib' / 'surgeo'
        else:
            # The application is not frozen
            self._package_root = pathlib.Path(__file__).parents[1]
        self._app_static = self._package_root / 'static'

    def main(self):
        """This is the entry point for the GUI program.

        It calls a function to create a root window, then adds widgets to
        that root window, and then finally triggers the tkinter main loop.

        """
        # Application setup
        self._window_setup()
        self._add_widgets()
        # Run mainloop
        self._objects['root'].mainloop()

    def _window_setup(self):
        """This sets up the main window."""
        # Create a frame object for layouts.
        self._objects['frame'] = tk.Frame(master=self._objects['root'])
        # Set title and window size
        self._objects['root'].title(f"Surgeo v.{surgeo.VERSION}")
        self._objects['root'].minsize(700, 160)
        # Bind enter to a function that starts the analysis
        self._objects['root'].bind('<Return>', self._execute)
        # Add icon
        self._objects['root'].tk.call(
            'wm',
            'iconphoto',
            self._objects['root']._w,
            tk.PhotoImage(
                file=str(self._app_static / 'logo.gif')
            )
        )

    def _select_input(self):
        """File selection window for input path (button triggered)"""
        # Get filename from dialog
        input_filename = filedialog.askopenfilename(
            title='Select Input Path',
            filetypes=(
                ('CSV files' , '*.csv' ),
                ('Excel XLSX', '*.xlsx'),
                ('Excel XLS' , '*.xls' )
            )
        )
        # Populate variable (in turn, updates screen)
        self._objects['input_var'].set(input_filename)

    def _select_output(self):
        """File selection window for output path (button triggered)"""
        # This has to be used twice (filetypes and defaultextention)
        files = (
            ('CSV files' , '*.csv' ),
            ('Excel XLSX', '*.xlsx'),
        )
        # Get filename from dialog
        output_filename = filedialog.asksaveasfilename(
            title='Select Output Path',
            filetypes=files,
            defaultextension=files,
        )
        # Populate variable (in turn updates screen)
        self._objects['output_var'].set(output_filename)

    def _add_widgets(self):
        """This huge function sets up the Surgeo interface row by row.

        For a visual, see:
        https://github.com/theonaunheim/surgeo/static/surgeo_example.gif

        Generally speaking, this goes row by row to create each and every
        widget used. The widget is created, assigned to a spot in the
        window using its .grid() method, and then it is stored in the
        self._objects to allow for later reference.
        """
        # Root alias to save typing
        root = self._objects['root']
        #######################################################################
        # Row 1: INPUT
        #######################################################################
        # File selection label
        select_label = ttk.Label(root, text='Input File')
        select_label.grid(row=0, column=0, padx=10, sticky='w')
        self._objects['select_label'] = select_label
        # File Selection Path Label and variable to store its data
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
        # Row 2: OUTPUT
        #######################################################################
        # Output file label
        output_label = ttk.Label(root, text='Output File')
        output_label.grid(row=1, column=0, padx=10, sticky='w')
        self._objects['output_label'] = output_label
        # File Output path and associated variable
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
        # Row 3 FIRST NAME
        #######################################################################
        # First Name label
        first_name_label = ttk.Label(
            root,
            text='First Name Column Header',
        )
        first_name_label.grid(row=2, column=0, padx=10, sticky='w')
        self._objects['first_name_label'] = first_name_label
        # Text entry box and associated variable
        first_name_var = tk.StringVar()
        self._objects['first_name_var'] = first_name_var
        first_name_entry = ttk.Entry(
            root,
            text='Enter First Name Column Header',
            textvariable=first_name_var,
        )
        first_name_entry.grid(row=2, column=1, padx=10, pady=3, sticky='w')
        self._objects['first_name_entry'] = first_name_entry
        #######################################################################
        # Row 4 SURNAME
        #######################################################################
        # Surname label
        surname_label = ttk.Label(
            root,
            text='Surname Column Header',
        )
        surname_label.grid(row=3, column=0, padx=10, sticky='w')
        self._objects['surname_label'] = surname_label
        # Text entry box and associated variable
        surname_var = tk.StringVar()
        self._objects['surname_var'] = surname_var
        surname_entry = ttk.Entry(
            root,
            text='Enter Surname Column Header',
            textvariable=surname_var,
        )
        surname_entry.grid(row=3, column=1, padx=10, pady=3, sticky='w')
        self._objects['surname_entry'] = surname_entry
        #######################################################################
        # Row 5 ZCTA
        #######################################################################
        # ZCTA label
        zcta_label = ttk.Label(
            root,
            text='ZIP/ZCTA Column Header',
        )
        zcta_label.grid(row=4, column=0, padx=10, sticky='w')
        self._objects['zcta_label'] = zcta_label
        # String variable and text entry box
        zip_var = tk.StringVar()
        self._objects['zip_var'] = zip_var
        zcta_entry = ttk.Entry(
            root,
            text='Enter ZIP/ZCTA Column Header',
            textvariable=zip_var,
        )
        zcta_entry.grid(row=4, column=1, padx=10, pady=3, sticky='w')
        self._objects['zcta_entry'] = zcta_entry
        #######################################################################
        # Row 6 MODEL TYPE
        #######################################################################
        # Model selector label
        model_label = ttk.Label(root, text='Model Type')
        model_label.grid(row=5, column=0, padx=10, sticky='w')
        self._objects['model_label'] = model_label
        # Dropdown to select which model to use. Also create variable
        model_var = tk.StringVar()
        self._objects['model_var'] = model_var
        model_selector = ttk.OptionMenu(
            root,
            model_var,
            # Default value
            'Surgeo (Surname + Geocode)',
            # Other values
            'Surgeo (Surname + Geocode)',
            'BIFSG',
            'First Name',
            'Surname',
            'Geocode',
        )
        model_selector.grid(row=5, column=1, padx=10, sticky='w')
        self._objects['model_selector'] = model_selector
        #######################################################################
        # Row 7 EXECUTE
        #######################################################################
        # Proces inputs button (this runs self._execute)
        # Note: this is also bound to <Enter> in the window setup func.
        execute_button = ttk.Button(
            root,
            text='Execute',
            command=self._execute,
        )
        execute_button.grid(row=6, column=2, padx=10, pady=3, sticky='w')
        self._objects['execute_button'] = execute_button

    def _check_inputs(self, df):
        """Take DF and raise error if improper column names given"""
        # Create shortnames for variables
        first_name_var = self._objects['first_name_var'].get()
        surname_var = self._objects['surname_var'].get()
        zip_var = self._objects['zip_var'].get()
        model_var = self._objects['model_var'].get()
        # If it's first name, make sure column is there. Otherwise error.
        if model_var == 'First Name':
            if first_name_var not in df.columns:
                # Otherwise raise error
                raise SurgeoException(f'{first_name_var} not in input data. '
                                      f'Columns are: {df.columns}.')
        # If it's geocode, make sure column is there. Otherwise error.
        elif model_var == 'Geocode':
            if zip_var not in df.columns:
                # Otherwise raise error
                raise SurgeoException(f'{surname_var} not in input data. '
                                      f'Columns are: {df.columns}.')
        # If Surname, make sure the user-specified surname column is there.
        elif model_var == 'Surname':
            # Otherwise raise error
            if surname_var not in df.columns:
                raise SurgeoException(f'{surname_var} not in input data. '
                                      f'Columns are: {df.columns}.')
        # If BIFSG, make sure the user-specified columns are present.
        elif model_var == 'BIFSG':
            if first_name_var not in df.columns:
                raise SurgeoException(f'{first_name_var} not in input data. '
                                      f'Columns are: {df.columns}.')
            if zip_var not in df.columns:
                raise SurgeoException(f'{surname_var} not in input data. '
                                      f'Columns are: {df.columns}.')
            if surname_var not in df.columns:
                raise SurgeoException(f'{surname_var} not in input data. '
                                      f'Columns are: {df.columns}.')
        # If Surgeo, make sure both user-specified columns are present.
        else:
            if zip_var not in df.columns:
                raise SurgeoException(f'{surname_var} not in input data. '
                                      f'Columns are: {df.columns}.')
            if surname_var not in df.columns:
                raise SurgeoException(f'{surname_var} not in input data. '
                                      f'Columns are: {df.columns}.')

    def _load_df(self, input_path):
        """This creates a dataframe based on self._input_path"""
        path = pathlib.Path(input_path)
        suffix = path.suffix
        # If it's excel, read_excel()
        if suffix == '.xlsx' or suffix == 'xls':
            df = pd.read_excel(path, engine='openpyxl')
        # If CSV, read read_csv()
        elif suffix == '.csv':
            df = pd.read_csv(path, skip_blank_lines=False)
        # If path is unrecognized, throw error
        else:
            raise SurgeoException(
                f'File ending for "{path}" not '
                'recognized. Please use .csv or .xlsx.'
            )
        return df

    def _execute(self, event=None, show_msgbox=True):
        """This takes all the user inputs and runs the analysis.

        It can be triggered by the enter key (in which case it supplied an
        event), or it can be triggered by clicking the "Execute" button.
        The outcome in either event is identical.

        """

        # Get tkinter variables and stuff strings in short names.
        # Input path from file selection
        input_var = self._objects['input_var'].get()
        # Output path from file selection
        output_var = self._objects['output_var'].get()
        # Surname column header from text field
        first_name_var = self._objects['first_name_var'].get()
        # Surname column header from text field
        surname_var = self._objects['surname_var'].get()
        # ZCTA column header from text field
        zip_var = self._objects['zip_var'].get()
        # Model being run from drop down window
        model_var = self._objects['model_var'].get()
        # Output path suffix (to determine if .csv or .xlsx)
        suffix = pathlib.Path(output_var).suffix
        # This large try block captures any errors for error window
        try:
            # Load the dataframe
            input_df = self._load_df(input_var)
            # Ensure the inputs are OK
            self._check_inputs(input_df)
            # If first name, run the first name model assign result to df
            if model_var == 'BIFSG':
                bifsg = BIFSGModel()
                output_df = bifsg.get_probabilities(
                    input_df[first_name_var],
                    input_df[surname_var],
                    input_df[zip_var]
                )
            # If first name, run the first name model assign result to df
            elif model_var == 'First Name':
                first = FirstNameModel()
                output_df = first.get_probabilities(input_df[first_name_var])
            # If geo, run the geo model assign result to df
            elif model_var == 'Geocode':
                geo = GeocodeModel()
                output_df = geo.get_probabilities(input_df[zip_var])
            # If sur, run the sur model and assign result to df
            elif model_var == 'Surname':
                sur = SurnameModel()
                output_df = sur.get_probabilities(input_df[surname_var])
            # If surgeo, run the surgeo model and assign to df
            else: # model_var == 'Surgeo (Surname + Geocode)':
                surgeo = SurgeoModel()
                # Note that surgeo takes two input columns unlike others
                output_df = surgeo.get_probabilities(
                    input_df[surname_var],
                    input_df[zip_var]
                )
            # If output is .xlsx, write to Excel
            if suffix == '.xlsx':
                output_df.to_excel(output_var, index=False)
            # Otherwise write to CSV
            else:
                output_df.to_csv(output_var, index=False)
            # Show message on success
            if show_msgbox:
                messagebox.showinfo(
                    'Success',
                    f'{len(output_df)} items successfully written.'
                )
        except Exception:
            # Show error box on fail
            err = traceback.format_exc()
            if show_msgbox:
                messagebox.showerror('Error', err)


if __name__ == '__main__':
    # Error handling within application.
    gui = SurgeoGUI()
    gui.main()
