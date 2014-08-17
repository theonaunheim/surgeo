#!/usr/local/bin/python3
#coding: utf-8
'''cx_Freeze setup script (does not work in Py 3.4.1, only 3.4.0)'''
from cx_Freeze import setup, Executable
# cd directory then 'python setup.py bdist_msi --add-to-path True'
exe = Executable(
    script = 'surgeo.py',
    initScript = None,
    base = None,
    targetName = 'surgeo.exe',
    copyDependentFiles = True,
    appendScriptToExe = True,
    appendScriptToLibrary = True,
    shortcutName='surgeo',
    icon = None,
    compress = True)

setup(name='surgeo',
      version='0.6.6',
      description='Disparate impact testing and surname geocoding analysis',
      url='https://github.com/theonaun/surgeo',
      author='Theo Naunheim',
      author_email='theonaunheim@gmail.com',
      license='MIT',
      packages=['surgeo', 'surgeo.db', 'surgeo.model', 'surgeo.utilities'],
      executables=[exe],
      classifiers=['Development Status :: 4 - Beta',
                   'Intended Audience :: Financial and Insurance Industry',
                   'License :: OSI Approved :: MIT License',
                   'Natural Language :: English',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python :: 3',
                   'Topic :: Office/Business :: Financial']
      )
