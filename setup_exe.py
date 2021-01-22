#from distutils.core import setup
from cx_Freeze import setup
from cx_Freeze import Executable

OPTIONS = {
    'bdist_msi': {
        "add_to_path": True,
        "target_name": "surgeo",
        "all_users": True,
    }
}

setup(
    # cx_Freeze setup.py
    executables=[
        Executable(
            "./surgeo/app/surgeo_gui.py", 
            base='Win32GUI',
            shortcutName='surgeo_gui',
            shortcutDir='ProgramMenuFolder',
        ),
        Executable(
            "./surgeo/app/surgeo_cli.py", 
            shortcutName='surgeo_cli',
            shortcutDir='ProgramMenuFolder',
        ),
    ],
    options=OPTIONS,
    # Normal setup.py
    name='surgeo',
    version='1.0.2',
    description='Bayesian Improved Surname Geocoder model',
    long_description="""
        Surgeo is an impelmentation of the Bayesian Improved Surname
        Geocode (BISG) model created by Mark N. Elliot et al. and
        incluenced by the Consumer Financial Protection Bureau's (CFPB)
        implementation of the same. It also includes an implementation
        of the Bayesian Improved First Name Surname Geocode (BIFSG) model
        created by Ioan Voicu.

    """,
    author='Theo Naunheim',
    author_email='theonaunheim@gmail.com',
    packages=[
        'surgeo',
        'surgeo.app',
        'surgeo.models',
        'surgeo.utility',
    ],
    license='MIT',
    url='https://github.com/theonaunheim/surgeo',
    keywords=[
        'bisg',
        'disparate',
        'race'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
    ],
    requires=[
        'pandas',
        'numpy',
        'xlrd',
    ],
    package_dir={'surgeo': './surgeo'},
    package_data={'surgeo': ['./data/*', './static/*']},
)
