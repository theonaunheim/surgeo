Background
==========

There are a variety of mechanisms by which one can impute race based one
generally available characaristics. Two popular approaches are
surname-based and location-based.

The surname-based approach works because certain last names are found much
more often in certain racial/ethnic groups. For example, over 90% of people
with the surname "Hernandez" identify as Hispanic according to Census data.
Similarly, over 90 of those with the last name of "Yoo" identify as Asian
or Pacific Islander.

The location-based approach works because racial/ethnic groups often live
in similar areas. For example, roughly 75% of Americans living in the U.S.
Virgin Islands are Black. Similarly, Vermont is approximately 95% White.

These approaches both have their strengths and weaknesses. Surname-based
approaches are excellent at picking out Hispanic and Asian/Pacific
Islander surnames. Surname-based approaches are comparatively weaker when
trying to Blacks, Whites, and Native Americans by name. Location-based
approaches are much better at discerning Black from White areas, but are
not particularly good at separating Asian and Hispanic populations [#]_.

It is possible to combine these approaches using `Bayesian inferencing`_;
this provides result that is superior to using either surname-based or
location-based approaches alone [#]_. To do this we take the probability
of race given a particular surname (prior probability) and then multiply
it by ratio of the population in a particular geograpahical area given that
race. The result is an updated (posterior) probability of race given both a
particular surname and geographic area. This is summarized by the following
formula.

For additional detail on how this works, please see `BISG by Example`_.

.. _Bayesian inferencing: https://en.wikipedia.org/wiki/Bayesian_inference

.. [#]

    Consumer Financial Protection Bureau. "Using Publicly Available
    Information to Proxy for Unidentified Race and Ethnicity". 2014.
    `<https://files.consumerfinance.gov/f/201409_cfpb_report_proxy-methodology.pdf>`_

.. [#]

    Elliott, M.N., Morrison, P.A., Fremont, A. et al. "Using the Census
    Bureau’s surname list to improve estimates of race/ethnicity and
    associated disparities". Health Serv Outcomes Res Method (2009) 9:
    69.
    `<https://link.springer.com/article/10.1007/s10742-009-0047-1>`_




Surgeo uses United States Census data from the 2010 Census. This contains

The United States Census fat

.. warning:: 

    ZIP Code Tabulation Areas (ZCTAs) are not identical to ZIP codes.
    Because ZIP codes change from year-to-year, the Census Bureau uses
    what it calls ZCTAs. These ZCTAs are rough approximations of the ZIP
    code geographic area--but it remains static after being created.

.. warning::

    Racial / Ethnic Groups