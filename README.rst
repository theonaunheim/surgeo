surgeo
==============

**THIS IS THE DEVELOPMENT BRANCH. NOT FOR PRODUCTION.**

.. image:: static/logo.gif
    :alt: logo
    :width: 50px

|rtd_badge| |travis_badge|

.. |rtd_badge| image:: https://readthedocs.org/projects/surgeo/badge/?version=dev

.. |travis_badge| image:: https://travis-ci.org/theonaunheim/surgeo.svg?branch=dev

The documentation for Surgeo may be found here:
`<https://surgeo.readthedocs.io/en/dev/>`_

Overview
--------

Surgeo is an open source Bayesian Improved Surname Geocode Analysis (BISG)
algorithm. In other words, Surgeo allows you to construct race
probabilities from commonly available data such as ZIP codes and surnames.
It is inspired by the work of the Consumer Financial Protection Bureau
(CFPB) and was initially created by Mark Elliot et al.

Please see the ReadTheDocs link above for information on the implementation
itself.

New In Version 2010.1.1
-----------------------

Version 2010.1.1 is a complete rewrite that adds the following features:

1.  Usage of the pandas library for clarity and vectorized calculations;
2.  Modular construction to allow for future census data updates;
3.  A rudimentary GUI to aid in batch processing;
4.  APIs for Surname, Geocoding, and Surname-Geocoding models to aid in
    data science; and,
5.  Enhanced documentation to provide a detailed view of how the algorithm
    works.

Installation
------------

To install surgeo as an executable, please see the installer below.

To install as a Python module, you can use pip:

.. code-block:: shell

    $ pip3 install surgeo

Usage
-----

Surgeo can be used as a stand-alone executable or a Python module.

As a Program
-----------~

To use the GUI, simply type in "surgeo".

.. code-block:: shell

    $ surgeo

image:: ./static/gui_example.gif

To use the CLI, type in "surgeo" followed by your arguments.

.. code-block:: shell

    $ surgeo --help

    usage: executable.py [-h] [--zcta_column ZCTA_COLUMN]
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

As a module
~~~~~~~~~~~

Surgeo is best used as a module.

:: python3

    import pandas as pd
    import surgeo

    # Series of names
    names = pd.Series(['DIAZ', 'JOHNSON', 'WASHINGTON'])
    zctas = pd.Series(['65201', '63144', '63110'])

    # Create model
    model = surgeo.SurgeoModel()

    # Run model and get dataframe
    results = model.get_probabilities(names, zctas)

.. image:: static/model_results.gif

Prefab files
------------

Windows installer:
TODO: Link to Windows installer