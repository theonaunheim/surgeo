#!/usr/local/bin/python3
#coding: utf-8

#python setup.py bdist_msi --add-to-path True 
#python3 setup.py bdist_msi --add-to-path True
# Should also have a 'surgeo.py' file in the setup.py directory that contains:
#   from surgeo.executable import main
#   main

from cx_Freeze import setup, Executable

build_exe_options = {'include_msvcr': True}

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
      version='0.7.0',
      description='Disparate impact testing and surname geocoding analysis',
      url='https://github.com/theonaun/surgeo',
      author='Theo Naunheim',
      author_email='theonaunheim@gmail.com',
      license='MIT',
      packages=['surgeo', 'surgeo.db', 'surgeo.model', 'surgeo.utilities'],
      options = {'build_exe': build_exe_options},
      executables=[exe],
      classifiers=['Development Status :: 4 - Beta',
                   'Intended Audience :: Financial and Insurance Industry',
                   'License :: OSI Approved :: MIT License',
                   'Natural Language :: English',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python :: 3',
                   'Topic :: Office/Business :: Financial']
      )
