Overview
========

Surgeo is a collection of tools that allows you to determine race by using
substitute (or "proxy") variables such as first name, last name and ZIP code.
These proxies are useful for determining race in contexts where this data might
not otherwise be available, such as in public health and fair lending.

This open source software contains a number of tools for conducting this
analysis, including:

1.  Python objects for doing First Name-base, Geocode-based, Surname-based,
    Bayesian Improved First Name Surname Geocoding (BIFSG), and Bayesian
    Improved Surname Geocoding (BISG) calculations;
2.  A command line interface (CLI) for automating batch processing; and,
3.  A graphical user interface (GUI) for one-off batch processing.

The base data for this module is sourced from publicly available 2010
United States Census files, specifically the `Summary File 1 data set`_ and
the `Frequently Occurring Surnames data set`_. As well it includes data from the `Demographics aspect of first names data set`_ [#]_.

.. _Summary File 1 data set: https://www.census.gov/data/datasets/2010/dec/summary-file-1.html

.. _Frequently Occurring Surnames data set: https://www.census.gov/topics/population/genealogy/data/2010_surnames.html

.. _Demographics aspect of first names data set: https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/TYJKEZ

.. [#]
     Konstantinos Tzioumis, "Data for: Demographic aspects of first names".
     Harvard Dataverse (2018), V1 `<https://doi.org/10.7910/DVN/TYJKEZ>`_
