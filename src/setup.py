#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# setup.py
# ********
# Literate programming with reStructuredText
# ++++++++++++++++++++++++++++++++++++++++++
#
# :Date:      $Date$
# :Revision:  $Revision$
# :URL:       $URL$
# :Copyright: © 2005, 2007 Günter Milde.
#             Released without warranty under the terms of the
#             GNU General Public License (v. 2 or later)
#
# ::

"""pylit: bidirectional text <-> code converter

Covert between a *text source* with embedded computer code and a *code source*
with embedded documentation.
"""

# Requirements for installation::

from distutils.core import setup

# Module Definition::

setup(name='PyLit',
      version='3.1',
      description='Python Literate Programming',
      author='S.Lott',
      author_email='slott56@gmail.com',
      url='http://developer.berlios.de/svn/?group_id=7974',
      py_modules=['pylit'],
     )

# And that's it. This will be installed into the site-packages directory.

# Technically, this isn't necessary.  A simple copy will do.
# Further, the :envvar:`PYTHONPATH` environment variable can name a directory
# that has PyLit.py in it.
