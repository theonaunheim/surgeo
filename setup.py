#!/usr/local/bin/python3
#coding: utf-8

import sys

from distutils.core import setup
from distutils.core import DistutilsError

# Version check before imports. If not Python3, kill import
if sys.hexversion < 0x03000000:
    raise DistutilsError('Python version of 3.0 or higher required.')
    
setup(name='surgeo',
      version='0.1.2000',
      description='Disparate impact testing through surname geocoding analysis',
      url = 'https://github.com/theonaun/surgeo',
      author='Theo Naunheim',
      author_email='theonaunheim@gmail.com',
      license='MIT',
      packages=['surgeo.db','surgeo.gui','surgeo.model','surgeo.utilities'],
      classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Financial and Insurance Industry',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Office/Business :: Financial'
        ]
     )
