BISG by Example
===============

This section is intended to provide a high-level walkthrough of how one
might perform BISG by hand. For this example we are going to determine the
probability of the surname "Garcia" in the ZIP code "63144". The formula
we use to calculate these probabilties is:

    | :math:`q(i \mid j,k) = \Large \frac{u(i,j,k)}{u(1,j,k) \, + \, u(2,j,k) \, + \, u(3,j,k) \, + \, u(4,j,k) \, + \, u(5,j,k) \, + \, u(6,j,k)}`
    |
    | Where:
    | :math:`\hspace{25px} u(i,j,k) = P(i \mid j) \times r(k \mid i)`
    |
    | And where:
    | :math:`\hspace{25px} P(i \mid j)` is the probability of a selected race given surname
    | :math:`\hspace{25px} r(k \mid i)` is the probability of a selected ZCTA of residence given race
    | :math:`\hspace{25px} k` is Census Block
    | :math:`\hspace{25px} j` is Surname
    | :math:`\hspace{25px} i` is Race
    |
    | And where:
    | :math:`\hspace{25px} 1 \text{ is } i =` Hispanic
    | :math:`\hspace{25px} 2 \text{ is } i =` White
    | :math:`\hspace{25px} 3 \text{ is } i =` Black
    | :math:`\hspace{25px} 4 \text{ is } i =` Asian or Pacific Islander
    | :math:`\hspace{25px} 5 \text{ is } i =` American Indian / Alaska Native
    | :math:`\hspace{25px} 6 \text{ is } i =` Multi Racial

The steps for performing this calculation are broken down below. Generally
speaking, the steps are:

1. Obtain probability for :math:`P(i \mid j)` (probability of race given
   surname) and :math:`r(k \mid i)` (proprtion of ZCTA given race);
2. Multiply each probability with each proprtion on a race-by-race basis to
   obtain :math:`u(i,j,k)` (probability of race given a particular ZCTA and
   surname) for each race; and then,
3. Divide the probability of each individual race probability by the sum of
   all race probabilities to obtain conditional probabilities adding up to
   1.

Surname Data (Obtaining :math:`P(i \mid j)`)
--------------------------------------------

According to the Census Bureau data, the surname "GARCIA" has the following
racial/ethnic probabilities.

+--------+--------+--------+--------+----------+-----------+
| White  | Black  | API    | Native | Multiple | Hispanic  |
+========+========+========+========+==========+===========+
| 0.0538 | 0.0045 | 0.0141 | 0.0047 | 0.0026   | 0.9203    |
+--------+--------+--------+--------+----------+-----------+

.. note::

    You may notice that "Hispanic" (i.e. whether someone comes from a
    Spanish-speaking culture) is treated like a race, even though there are
    white hispanics, black hispanics, etc.). Consequently "White" is
    actually "White, Non-Hispanic", and "Hispanic" is all races that come
    from a Spanish-speaking culture.

In other words, these are the probabilities (:math:`P`) of a race
(:math:`i`) given the surname (:math:`j`) "Garcia", which is represented
mathematically as :math:`P(i \mid j)`. It is the so-called "prior
probability" that we will be updating with our location information.

Geocode Data (Obtaining :math:`r(k \mid i)`)
--------------------------------------------

According to Census Bureau data, the ZIP code "63144" contains this
proportion of the United State's race populations.

+----------+----------+----------+----------+-----------+-------------+
| White    | Black    | API      | Native   | Multiple  | Hispanic    |
+==========+==========+==========+==========+===========+=============+
| 0.000039 | 0.000007 | 0.000037 | 0.000005 | 0.000025  | 0.000005    |
+----------+----------+----------+----------+-----------+-------------+

.. note::

    ZIP Code Tabulation Areas (ZCTAs) are not identical to ZIP codes.
    Because ZIP codes change from year-to-year, the Census Bureau uses
    what it calls ZCTAs. These ZCTAs are rough approximations of the ZIP
    code geographic area--but it remains static after being created.

Put simply, .0039% of the United State's White population lives within the
63144 ZIP code; .0007% of the US's Black populaiton lives within 63144,
etc. In other words, these are the proportions (:math:`r`) of a selected
ZIP (:math:`k`) given a particular race (:math:`i`), which is represented
mathematically as :math:`r(k \mid i)`.

Multiplying Probabilities (Obtaining :math:`u(i,j,k)`)
------------------------------------------------------

:math:`\hspace{25px} u(i,j,k) = P(i \mid j) \times r(k \mid i)`



