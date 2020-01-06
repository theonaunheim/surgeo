Usage
=====

Surgeo can be used as a stand-alone executable or a Python module. Details
follow.

As a Module
-----------

Surgeo is best used as a module with pandas and the Jupyter notebook. The
general workflow will be for you to import surgeo, then create a model, and
then run the analysis using the get_probabilities() function along with the
data being analyzed.

The available models are:

    1. `GeocodeModel`, which uses a series of ZIP codes and gives the
       racial percentage make up of that ZIP code (e.g. 81% of those people
       in ZIP 65201 are white).
    2. `SurnameModel`, which uses a series of surnames and gives the racial
       percentage of that surname (e.g. 5% of people with the surname DIAZ
       are white); and,
    3. `SurgeoModel`, which takes a series of surnames and a series of ZIP
       codes and gives the BISG results of those inputs (e.g. someone named
       DIAZ in ZIP 65201 has a 26% probability of being white).

.. code-block:: python

    import pandas as pd
    import surgeo

    # Instatiate your model (or all three)
    g = surgeo.GeocodeModel()
    s = surgeo.SurnameModel()
    sg = surgeo.SurgeoModel()

    # Create pd.Series objects to analze (or load them)
    names = pd.Series(['DIAZ', 'JOHNSON', 'WASHINGTON'])
    zctas = pd.Series(['65201', '63144', '63110'])

    # Get results using the get_probabilities() function
    g_results = g.get_probabilities(zctas)
    s_results = s.get_probabilities(names)
    sg_results = sg.get_probabilities(names, zctas)

    # Show Surgeo results
    sg_results

.. image:: ./_static/model_results.gif

As a Program
------------

To use the GUI, type in "surgeo". 

Simply supply the input and output file paths as required and then select
the model type. Then select any column names in your .xlsx/.csv associated
with surname/ZIP, and click "Execute". The results will be written to the
output file.

.. code-block::

    $ surgeo

.. image:: ./_static/gui_example.gif

To use the CLI, type in "surgeo" followed by your arguments. The first
argument is the input file path, the second argument is the output file
path, and the third argument is the model being used. There are also
optional argument to define the name of the ZCTA and surname columns if
they are not the defaults ("zcta5" and "surname" respectively).

.. code-block::

    $ surgeo --help

    usage: surgeo [-h] [--zcta_column ZCTA_COLUMN]
                        [--surname_column SURNAME_COLUMN]
                        input output type

    Get Surgeo arguments.

    input                 Input CSV or XLSX of data.
    output                Output CSV or XLSX of data.
    type                  The model type being run ("sur", "geo" or "surgeo")

    optional arguments:
    -h, --help            show this help message and exit
    --zcta_column ZCTA_COLUMN
                        The input column to analyze as ZCTA/ZIP)
    --surname_column SURNAME_COLUMN
                        The input column to analyze as surname")
