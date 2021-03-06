#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

# :Date:      $Date: 2009-03-05 11:16:49 -0500 (Thu, 05 Mar 2009) $
# :Version:   SVN-Revision $Revision: 104 $
# :URL:       $URL:  $
# :Copyright: 2006 Guenter Milde.
#             Released without any warranty under the terms of the
#             GNU General Public License (v. 2 or later)
#
# testmod_literate
# ================
#
# The module docstring should give a concise description of the working,
# details are in the literate source so the docstrings are not bloated::

"""
This is the "testmod_literate" module.

It supplies one function, `factorial()`.  For example,

>>> factorial(5)
120

"""

__docformat__ = 'restructuredtext'


# **Beware:** as the docstring is not parsed as separate unit but as part of
# the file, there must be a blank line also after the last doctest block.
# Otherwise `doctest` expects ``"""`` to be part of the output.
#
#
# factorial
# ---------
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
#       >>> factorial(30)
#       265252859812191058636308480000000
#
#
# Self Test
# ---------
#
# The traditional test function parses the docstrings of all objects in this
# module. It misses doctests in comments::

def _test():
    import doctest
    doctest.testmod()

# Test all doctest blocks (both in docstrings and in text parts (well
# formatted comments) if the module is called as `__main__` (i.e. from the
# command line)::

def _test_all_doctests():
    import pylit, sys
    pylit.run_doctest(infile=sys.argv[0], txt2code=False,
                      globs=sys.modules.get('__main__').__dict__)

# (Future versions of `pylit` might contain a convenience function for a simpler
# invocation of this test.)
#
# Doctests can still be disabled or commented - make sure they are not
# recognised as text block (no double colon here):
#
#   # a silly doctest
#   # >>> False
#   # True
#
# or (with non-canonical comments)::

# a silly doctest
#>>> False
#True

# Doctests in doc-strings can be skipped with the `strip` option::

def _test_text_doctests():
    import pylit, sys
    pylit.run_doctest(infile=sys.argv[0], txt2code=False, strip=True,
                      globs=sys.modules.get('__main__').__dict__)



# Do a self test::

if __name__ == "__main__":
    #_test()
    _test_all_doctests()

