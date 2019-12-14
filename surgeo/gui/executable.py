"""Script containing a basic GUI program."""

import pathlib
import sys
import tkinter as tk
import tkinter.ttk as ttk

import pandas as pd

# Jury rig path
path_dir = pathlib.Path(__file__).resolve().parents[2]
sys.path.append(str(path_dir))

import surgeo


class SurgeoGUI(object):

    def __init__(self):
        self._objects = {'root': tk.Tk()}

    def main(self):
        self._window_setup()
        self._add_widgets()
        self._add_logic()
        self._objects['root'].mainloop()

    def _nonfatal_error_exit(self, error):
        pass

    def _fatal_error_exit(self, error):
        sys.exit(1)

    def _window_setup(self):
        self._objects['frame'] = tk.Frame(master=self._objects['root'])
        self._objects['root'].title(f"Surgeo v.{surgeo.VERSION}")
        self._objects['root'].minsize(500, 500)
        # Add icon
        self._objects['root'].tk.call(
            'wm', 
            'iconphoto', 
            self._objects['root']._w, 
            tk.PhotoImage(file=str(path_dir / 'surgeo' / 'static' / 'logo.gif'))
        )

    def _select_input(self, destination):
        destination['text'] = 'ha'

    def _add_widgets(self):
        # File selection
        select_label = ttk.Label(self._objects['root'], text='Input File')
        select_label.grid(row=0, column=0, padx=10)
        self._objects['select_label'] = select_label
        select_path_text = tk.Label(
            self._objects['root'],
            text='Select Input File',
            borderwidth=1,
            relief='solid',
            width=40
        )
        self._objects['select_path_text'] = select_path_text
        select_path_text.grid(row=0, column=1, padx=10)
        select_button = ttk.Button(
            self._objects['root'], 
            text='Select',
            command=lambda: self._select_input(destination=self._objects['select_path_text']),
        )
        select_button.grid(row=0, column=2, padx=10)
        self._objects['select_button'] = select_button

    def _add_logic(self):
        pass


if __name__ == '__main__':
    # Error handling within application.
    gui = SurgeoGUI()
    gui.main()
