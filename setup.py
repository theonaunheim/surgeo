from distutils.core import setup


setup(
    name='surgeo',
    version='1.1.1',
    description='Bayesian Improved Surname Geocoder model',
    long_description="""
        **Surgeo** is an impelmentation of the Bayesian Improved Surname
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
        'openpyxl',
    ],
    package_dir={'surgeo': './surgeo'},
    package_data={'surgeo': ['./data/*', './static/*']},
)
