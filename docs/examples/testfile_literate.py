#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

# :Date:      $Date: 2009-03-05 11:16:49 -0500 (Thu, 05 Mar 2009) $
# :Version:   SVN-Revision $Revision: 104 $
# :URL:       $URL:  $
# :Copyright: 2006 Guenter Milde.
#             Released without any warranty under the terms of the
#             GNU General Public License (v. 2 or later)
#
# testfile_literate
# =================
#
# Import
# ------
#
# As this module is not loaded when the file is tested with
# ``pylit --doctest``, the first doctest must import it before any of its
# objects can be used.
# An elegant solution is to give a usage example in the module's docstring::

"""
This is the "testfile_literate" module.

It supplies one function, `factorial()` that returns the factorial of its
argument, e.g.:

>>> import testfile_literate
>>> testfile_literate.factorial(5)
120

"""

__docformat__ = 'restructuredtext'


# .. attention:: As the docstring is not parsed as separate unit but as part of the
#          file, there must be a blank line also after the last doctest block.
#          Otherwise `doctest` expects ``"""`` to be part of the output.
#
# Alternatives for easier access to the defined objects are:
#
#   >>> import testfile_literate as fac
#   >>> fac.factorial(5)
#   120
#
#   >>> from testfile_literate import *
#   >>> factorial(5)
#   120
#
# This imports the *code source* of the literal script:
#
# * ``testfile_literate.py`` must be present in the PYTHONPATH or the current
#   working directory.
#
# * The doctest examples in the file argument to ``pylit --doctest`` (be it
#   text source or code source) are tested with the code definitions in the
#   last saved version of the code source.
#
#
# factorial
# ---------
#
# The functions docstring can be kept concise and additional discussion
# referred to the text part of the literate source::

def factorial(n):
    """Return the factorial of `n`, an exact integer >= 0.

    >>> [factorial(n) for n in range(6)]
    [1, 1, 2, 6, 24, 120]
    >>> factorial(30)
    265252859812191058636308480000000

    Factorials of floats are OK, but the float must be an exact integer:

    >>> factorial(30.0)
    265252859812191058636308480000000

    """

    import math
    if not n >= 0:
        raise ValueError("n must be >= 0")
    if math.floor(n) != n:
        raise ValueError("n must be exact integer")
    if n+1 == n:  # catch a value like 1e300
        raise OverflowError("n too large")
    result = 1
    factor = 2
    while factor <= n:
        result *= factor
        factor += 1
    return result


# Discussion and test
# ~~~~~~~~~~~~~~~~~~~
#
# `factorial()` accepts input as int, long or float:
#
#       >>> factorial(30)
#       265252859812191058636308480000000
#       >>> factorial(30)
#       265252859812191058636308480000000
#       >>> factorial(30.0)
#       265252859812191058636308480000000
#
# However, the float must be an exact integer and it must also not be
# ridiculously large:
#
#       >>> factorial(30.1)
#       Traceback (most recent call last):
#           ...
#       ValueError: n must be exact integer
#
#       >>> factorial(1e100)
#       Traceback (most recent call last):
#           ...
#       OverflowError: n too large
#
# The factorial of negative values is not defined:
#
#       >>> factorial(-1)
#       Traceback (most recent call last):
#           ...
#       ValueError: n must be >= 0
#
# The type of the return value depends on the size of the result.
#
#   If the result is small enough to fit in an int, return an int.
#   Else return a long:
#
#       >>> [factorial(n) for n in range(6)]
#       [1, 1, 2, 6, 24, 120]
#       >>> [factorial(n) for n in range(6)]
#       [1, 1, 2, 6, 24, 120]
#       >>> factorial(30)
#       265252859812191058636308480000000
#       >>> factorial(30)
#       265252859812191058636308480000000
#
#
# Default Action
# --------------
#
# The script is tested by calling ``pylit --doctest testfile_literate.py``
# or ``pylit --doctest testfile_literate.py.txt``.
#
# This is especially handy for scripts that should perform some default
# action other than a self test, e.g.
#
# Print the first 10 natural numbers and their factorials if
# called as `__main__` (i.e. from the command line)::

if __name__ == "__main__":
    print( "n n!" )
    for n in range(10):
        print( n, factorial(n) )


