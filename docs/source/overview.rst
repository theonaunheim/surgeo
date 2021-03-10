Overview
========

Surgeo is a collection of tools that allows you to determine race by using
substitute (or "proxy") variables such as first name, last name and ZIP code.
These proxies are useful for determining race in contexts where this data might
not otherwise be available, such as in the public health and fair lending.

This open source software contains a number of tools for conducting this
analysis, including:

1.  Python modules for doing first name-based, geocode-based, surname-based,
    Bayesian Improved First Name Surname Geocoding (BIFSG), and Bayesian
    Improved Surname Geocoding (BISG) calculations;
2.  A command line interface (CLI) for automating batch processing; and,
3.  A graphical user interface (GUI) for one-off batch processing.

The base data for this module is sourced from publically available data,
specifically:

1.  2010 United States Census `Summary File 1 data set`_; 
2.  2010 United States Census `Frequently Occurring Surnames data set`_; and,
3.  `Demographics aspect of first names data set`_ [#]_.

.. _Summary File 1 data set: https://www.census.gov/data/datasets/2010/dec/summary-file-1.html

.. _Frequently Occurring Surnames data set: https://www.census.gov/topics/population/genealogy/data/2010_surnames.html

.. _Demographics aspect of first names data set: https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/TYJKEZ

.. [#]
     Konstantinos Tzioumis, "Data for: Demographic aspects of first names".
     Harvard Dataverse (2018), V1 `<https://doi.org/10.7910/DVN/TYJKEZ>`_
