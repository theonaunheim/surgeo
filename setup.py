#!/usr/local/bin/python3
#coding: utf-8

from distutils.core import setup

setup(name='surgeo',
      version='1.0.0',
      description='Disparate impact testing and surname geocoding analysis',
      url='https://github.com/theonaun/surgeo',
      author='Theo Naunheim',
      author_email='theonaunheim@gmail.com',
      license='MIT',
      packages=['surgeo',
                'surgeo.gui',
                'surgeo.models',
                'surgeo.scripts',
                'surgeo.utilities'],
      classifiers=['Development Status :: 4 - Beta',
                   'Intended Audience :: Financial and Insurance Industry',
                   'License :: OSI Approved :: MIT License',
                   'Natural Language :: English',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python :: 3',
                   'Topic :: Office/Business :: Financial']
      )

