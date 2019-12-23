BISG by Example
===============

This section is intended to provide a high-level walkthrough of how one
might perform BISG by hand. For this example we are going to determine the
probability of the surname "Garcia" in the ZIP code "63144".

Surname Data
------------

According to the Census Bureau, the surname "GARCIA" has the following
racial/ethnic probabilities.

+---------+-------+--------+--------+----------+-----------+
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

In otherwords, these are the probabilities of a race given the surname
"Garcia", which is represented mathematically as
:math:`P(i \mid j)`. It is the so-called "prior probability" that we will
be updating with our location information.

Geocode Data
------------

According to Census Data



