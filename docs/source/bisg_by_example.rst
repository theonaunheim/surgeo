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

1. Obtain :math:`P(i \mid j)` (probability of race given surname) and
   :math:`r(k \mid i)` (proprtion of ZCTA given race);
2. Multiply each probability with each proprtion on a race-by-race basis to
   obtain :math:`u(i,j,k)` (probability intermediate) for each race; and
   then,
3. Divide the posterior probability of each individual race dividing the
   intermediate above by the sum of all intermediates to give
   :math:`q(i \mid j,k)` (the probability of race given a surname and ZIP
   code).

Using Surname Data To Obtaining :math:`P(i \mid j)`
---------------------------------------------------

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

Using Geocoding Data to Obtain :math:`r(k \mid i)`
--------------------------------------------------

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

Multiplying Probabilities to Obtain :math:`u(i,j,k)`
----------------------------------------------------

The next step is to multiply our vectors together to obtain
:math:`u(i,j,k)`, which is an intermediate used to calculate the final
posterior probability. This uses is a simple element-wise multiplication
operation defined by:

:math:`u(i,j,k) = P(i \mid j) \times r(k \mid i)`

Step-by-step, we can take the numbers above from :math:`P(i \mid j)`:

+--------+--------+--------+--------+----------+-----------+
| White  | Black  | API    | Native | Multiple | Hispanic  |
+========+========+========+========+==========+===========+
| 0.0538 | 0.0045 | 0.0141 | 0.0047 | 0.0026   | 0.9203    |
+--------+--------+--------+--------+----------+-----------+

... and then multiply it by our numbers for :math:`r(k \mid i)`:

+----------+----------+----------+----------+-----------+-------------+
| White    | Black    | API      | Native   | Multiple  | Hispanic    |
+==========+==========+==========+==========+===========+=============+
| 0.000039 | 0.000007 | 0.000037 | 0.000005 | 0.000025  | 0.000005    |
+----------+----------+----------+----------+-----------+-------------+

... which then results in :math:`u(i,j,k)`:

+----------+----------+----------+----------+-----------+-------------+
| White     | Black   | API      | Native   | Multiple  | Hispanic    |
+==========+==========+==========+==========+===========+=============+
| 2.07e-06 | 3.04e-08 | 5.21e-07 | 2.30e-08 | 6.48e-08  | 4.33e-06    |
+----------+----------+----------+----------+-----------+-------------+

As you can see from the above, the "White" probability for this surname is
0.0538 and the "White" proportion for this ZIP is .000039. If we multiply
0.0538 times .000039, we get 0.00000207. This is also done for the
remaining races.

Obtaining Final Probability Vector :math:`q(i \mid j,k)`
--------------------------------------------------------

The final step is defined by the following equation:

:math:`q(i \mid j,k) = \Large \frac{u(i,j,k)}{u(1,j,k) \, + \, u(2,j,k) \, + \, u(3,j,k) \, + \, u(4,j,k) \, + \, u(5,j,k) \, + \, u(6,j,k)}`

What this means is simply that in order to obtain our final probability for
a given race :math:`i`, we must take the intermediate value for that race
and then divide it by the sum of all races. For example, to run This
calculation for "White" the formula would read:

:math:`q(\text{white} \mid \text{Garcia},\text{63144}) = \Large \frac{u(\text{white},\text{Garcia},\text{63144})}{u(\text{hispanic},\text{Garcia},\text{63144}) \, + \, u(\text{white},\text{Garcia},\text{63144}) \, + \, u(\text{black},\text{Garcia},\text{63144}) \, + \, u(\text{api},\text{Garcia},\text{63144}) \, + \, u(\text{native},\text{Garcia},\text{63144}) \, + \, u(\text{multi},\text{Garcia},\text{63144})}`

And pluging in the intermediate values from :math:`u(i,j,k)`:

+----------+----------+----------+----------+-----------+-------------+
| White     | Black   | API      | Native   | Multiple  | Hispanic    |
+==========+==========+==========+==========+===========+=============+
| 2.07e-06 | 3.04e-08 | 5.21e-07 | 2.30e-08 | 6.48e-08  | 4.33e-06    |
+----------+----------+----------+----------+-----------+-------------+

We would have the following calculation for "White" (29.4%):

:math:`.294 = \Large \frac{2.07e-06}{4.33e-06 \, + \, 2.07e-06 \, + \, 3.04e-08 \, + \, 5.21e-07 \, + \, 2.30e-08 \, + \, 6.48e-08 }`

And the following final percentages for "GARCIA" and "63144":

+----------+---------+----------+----------+-----------+-------------+
| White    | Black   | API      | Native   | Multiple  | Hispanic    |
+==========+=========+==========+==========+===========+=============+
| .294     | .004    | .084     | .003     | .009      | .615        |
+----------+---------+----------+----------+-----------+-------------+

This comes out very much like we might expect--the 63144 ZIP skews White,
but "GARCIA" is overwhelmingly a Hispanic.
