"""Module containing the common entry class."""

import pathlib
import sys

import surgeo

from surgeo.app.surgeo_cli import SurgeoCLI
from surgeo.app.surgeo_gui import SurgeoGUI


class SurgeoCommonEntry(object):
    """An entry point for both the GUI and CLI Surgeo applications

    This class simply gets the number of args sent to the entry point. If
    there is a single argument, the GUI is run. If addtional arguments are
    supplied, the CLI is run. The CLI will then parse the arguments as
    nothing it is not necessary to pass the arguments from the common entry
    to the CLI.

    """

    def main(self):
        """The entry point's main function

        This gets the number of arguments supplied. If no arguments are
        supplied in addition to the 'surgeo' command, the GUI is run.
        Otherwise, the CLI is run.

        """

        # Get arg count
        arg_count = len(sys.argv)
        # If 1, run GUI.
        if arg_count == 1:
            gui = SurgeoGUI()
            gui.main()
        # Else, run CLI
        else:
            cli = SurgeoCLI()
            cli.main()


if __name__ == '__main__':
    common = SurgeoCommonEntry()
    common.main()
