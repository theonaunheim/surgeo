Background
==========

.. note::

    If you are only looking for how to use Surgeo and are not interested in
    the mechanics, please skip to `Usage`_.

There are a variety of mechanisms by which one can impute race based on
generally available characteristics. Three popular approaches are
surname-based (last name), forename-based (first name), and location-based.

The surname-based approach works because certain last names are found much
more often in specific racial/ethnic groups. For example, over 90% of people
with the surname "Hernandez" identify as Hispanic according to Census data.
Similarly, over 90% of those with the last name of "Yoo" identify as Asian
or Pacific Islander.

The forename-based approach works similarly to the surname-based approach,
with first name being used as the proxy for racial/ethnic probability.

The location-based approach works because racial/ethnic groups often live
in similar areas. For example, roughly 75% of Americans living in the U.S.
Virgin Islands are Black. Similarly, Vermont is approximately 95% White.

These approaches all have their strengths and weaknesses. Surname-based
approaches are excellent at picking out Hispanic and Asian/Pacific
Islander surnames. Surname-based approaches are comparatively weaker when
trying to identify Blacks, Whites, and Native Americans by name.
Forename-based approaches compensate for weaknesses in the surname-only
approach [#]_. Location-based approaches are much better at discerning
Black from White areas, but are not particularly good at separating Asian
and Hispanic populations [#]_.

It is possible to combine these approaches using `Bayesian inference`_;
this provides result that is superior to using any approach alone [#]_.
For a combination of surname-based and location-based, for example, this
can be performed as follows.

First one takes the probability of race given a particular surname
(prior probability) and then multipies it by ratio of the population in a
particular geographical area given that race. The result is an updated
(posterior) probability of race given a particular surname and a particular
geographic area. This can be further refined with the addition of forename
data.

For additional detail on how this works, please see `BISG by Example`_.

.. _Bayesian inference: https://en.wikipedia.org/wiki/Bayesian_inference

.. [#]

     Ioan Voicu "Using First Name Information to Improve Race and Ethnicity
     Classification". Statistics and Public Policy (2018) 5:1, 1-13,
     `<https://www.tandfonline.com/doi/full/10.1080/2330443X.2018.1427012>`_

.. [#]

    Consumer Financial Protection Bureau. "Using Publicly Available
    Information to Proxy for Unidentified Race and Ethnicity". 2014.
    `<https://files.consumerfinance.gov/f/201409_cfpb_report_proxy-methodology.pdf>`_

.. [#]

    Elliott, M.N., Morrison, P.A., Fremont, A. et al. "Using the Census
    Bureau’s surname list to improve estimates of race/ethnicity and
    associated disparities". Health Serv Outcomes Res Method (2009) 9:
    69. `<https://link.springer.com/article/10.1007/s10742-009-0047-1>`_
