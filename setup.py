#!/usr/local/bin/python3
#coding: utf-8

from distutils.core import setup

setup(name='surgeo',
      version='0.1.2000',
      description='Disparate impact testing through surname geocoding analysis',
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
