#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ********
# setup.py
# ********
#
# Literate programming with reStructuredText
#
# ::

"""pylit: bidirectional text <-> code converter

Convert between a *text source* with embedded computer code and a *code source*
with embedded documentation.
"""

# Requirements for installation::

from setuptools import setup, find_packages
import pathlib

# Module Definition::

setup(
      name='pylit',
      version='3.1.1',
      description='Python Literate Programming',
      long_description=pathlib.Path('README.rst').read_text(),
      author='S.Lott',
      author_email='slott56@gmail.com',
      python_requires=">=3.5",
      url='https://github.com/slott56/PyLit-3',
      project_urls={
            "Documentation": 'https://slott56.github.io/PyLit-3/index.html',
            "Source Code": 'https://github.com/slott56/PyLit-3',
            "Bug Tracker": 'https://github.com/slott56/PyLit-3/issues',
      },
      provides='pylit',
      py_modules=['pylit'],
      classifiers=[
            "Development Status :: 6 - Mature",
            "Intended Audience :: Developers",
            "Operating System :: OS Independent",
            "Programming Language :: Python :: 3 :: Only",
            "Topic :: Software Development :: Build Tools",
      ],
      license='GNU General Public License (v. 2 or later)',
     )

# And that's it. This will be installed into the site-packages directory.

# Technically, this isn't necessary.  A simple copy will do.
# Further, the :envvar:`PYTHONPATH` environment variable can name a directory
# that has :file:`pylit.py` in it.
