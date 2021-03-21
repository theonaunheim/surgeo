Surgeo
==============

.. image:: static/logo.gif

|rtd_badge| |travis_badge| |shieldio_badge|

.. |rtd_badge| image:: https://readthedocs.org/projects/surgeo/badge/?version=master

.. |travis_badge| image:: https://travis-ci.org/theonaunheim/surgeo.svg?branch=master

.. |shieldio_badge| image:: https://badge.fury.io/py/surgeo.svg

.. image:: https://badges.gitter.im/Surgeo_project/community.svg
   :target: https://gitter.im/Surgeo_project/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge

The documentation for Surgeo may be found here: `<https://surgeo.readthedocs.io/en/master/>`_

Contributors
------------
* `Adam Weeden <https://github.com/TheCleric>`_
* `Algorex Health <https://github.com/AlgorexHealth>`_
* `Theo Naunheim <https://github.com/theonaunheim>`_

Overview
--------

**Surgeo** is a module that contains a variety of open source demographic
tools that allow you to construct race probabilities from more commonly
available information such as location, first name, and last name
information. This imputed race data is often used in the public health
and fair lending contexts when race information is not otherwise
available.

Specifically Surgeo contains the following models:

* **Bayesian Improved First Name Surname Geocode (BIFSG)**: an adaptation
  of an algorithm created by Ioan Voicu that uses forename, surname, and
  location information to obtain probable races
* **Bayesian Improved Surname Geocode (BISG)**: an adaptation of an algorithm
  created by Mark Elliot and popularized by the Consumer Financial Protection
  Bureau (CFPB) that uses surname and location to obtain probable races
* **Forename**: a helper model to pull race data based on first name
* **Surname**: a helper model to pull race data based on last name
* **Geocode**: a helper model to pull race data based on location

Please see the ReadTheDocs link above for additional information on the
data sources used and the implementations themselves.

Installation
------------

To install surgeo as an executable, please see the installer below.

To install as a Python module, you can use pip:

.. code-block::

    $ pip install surgeo

Usage
-----

Surgeo can be used as a stand-alone executable or a Python module. Details
follow.

As a Program
~~~~~~~~~~~~

To use the GUI, simply type in "surgeo_gui" or use the Start Menu after
installing the executable. For Mac or Linux users, ensure that you have tkinter
setup on your
`Python distribution <https://stackoverflow.com/questions/22550068/python-not-configured-for-tk>`_.

.. code-block::

    $ surgeo_gui
    # Or alternatively if you have installed the module
    $ python -m surgeo

.. image:: ./static/gui_example.gif

To use the CLI, type in "surgeo" followed by your arguments.

.. code-block::

    $ surgeo_cli --help
    # Or alternatively if you have installed the module
    $ python -m surgeo -h

    usage: cli.py [-h] [--zcta_column ZCTA_COLUMN]
    [-ct]
    [--first_name_column FIRST_NAME_COLUMN]
    [--surname_column SURNAME_COLUMN]
    [--state_column STATE_COLUMN]
    [--county_column COUNTY_COLUMN]
    [--tract_column TRACT_COLUMN]
    input output type

    Get Surgeo arguments.

    input                 Input CSV or XLSX of data.
    output                Output CSV or XLSX of data.
    type                  The model type being run ("first", "sur", "geo", "bifsg", or "surgeo")

    optional arguments:
    -h, --help            show this help message and exit
    -ct                  Process for CENSUS Tract as opposed to ZCTA/ZIP
    --zcta_column ZCTA_COLUMN
              The input column to analyze as ZCTA/ZIP
    --first_name_column FIRST_NAME_COLUMN
              The input column to analyze as first name
    --surname_column SURNAME_COLUMN
              The input column to analyze as surname
    --state_column STATE_COLUMN input column containing two digit FIPS state code
    --county_column input column containing three digit FIPS County Code
    --tract_column input column containing six digit tract code

As a Module
~~~~~~~~~~~

Surgeo is best used as a module.

.. code-block:: python

    import pandas as pd
    import surgeo

    # Instatiate your model
    fsg = surgeo.BIFSGModel()

    # Create pd.Series objects to analze (or load them)
    first_names = pd.Series(['HECTOR', 'PHILLIP', 'JANICE'])
    surnames = pd.Series(['DIAZ', 'JOHNSON', 'WASHINGTON'])
    zctas = pd.Series(['65201', '63144', '63110'])

    # Get results using the get_probabilities() function
    fsg_results = fsg.get_probabilities(first_names, surnames, zctas)

    # Show Surgeo BIFSG results
    fsg_results

.. image:: static/model_results.gif

Prefab Files
------------

A link to the Windows GUI/CLI is below.

`Windows installer <https://github.com/theonaunheim/surgeo/releases/download/v1.1.1/surgeo-amd64.msi>`_.
