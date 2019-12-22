Overview
========

Surgeo is a collection of tools that allows you to determine race by using
substitute (or "proxy") variables such as last name and ZIP code. These
proxies are useful for determining race in contexts where this data might
not otherwise be available, such as in public health and fair lending.

This open source software contains a number of tools for conducting this
analysis, including:

1.  Python objects for doing Geocode-based, Surname-based, and Bayesian
    Improved Surname Geocoding (BISG) calculations;
2.  A command line interface (CLI) for automating batch processing; and,
3.  A graphical user interface (GUI) for one-off batch processing.

The base data for this module is sourced from publically available 2010
United States Census files, specifically the `Summary File 1 dataset`_ and
the `Frequently Occuring Surnames dataset`_.

.. _Summary File 1 dataset: https://www.census.gov/data/datasets/2010/dec/summary-file-1.html

.. _Frequently Occuring Surnames dataset: https://www.census.gov/topics/population/genealogy/data/2010_surnames.html
