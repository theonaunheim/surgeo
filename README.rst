.. image:: logo.gif

Surgeo
==============

**Link to Windows installer at bottom.**

Surgeo is a hackish attempt to reverse engineer the Consumer Financial 
Protection Bureau's (CFPB) Bayesian Improved Surname Geocode Analysis (BISG).

Python code by Theo Naunheim. Model created by Mark N. Elliot et al. For 
details, please see BACKGROUND.txt.

Created as a trial run so that when the CFPB releases its whitepaper on proxy 
analysis Summer 2014, the model can be quickly adapted to conform to it. I am
not a developer nor a statistician, so please use at your own risk.

Please note that your shortcut to Python may be 'python' or 'python3' depending 
on how it is installed. Additionally, this guide presumes you are working on
a Unix-like system. If running Windows, you will need to substitute backslashes 
instead of the slashes used in the paths below.

Command line utility only as of August 2014. GUI to follow.

Installing
--------------

::

    <Download installer at link below. Run. Type 'surgeo' into cmd.exe>
    
    or
    
    pip3 install surgeo
    
    or
    
    python3 <path_to_setup.py> install


If using as a Python module in your program
--------------

::

    import surgeo
    
    # Download data and create tables (takes some time)
    surgeo.data_setup(verbose=True)
    
    # Create model object (SurModel and GeoModel also exist)
    model = surgeo.SurgeoModel() 
    
    # Simple version returns 'White'
    model.guess_race(63110, 'Naunheim') 
    
    # race_data() returns object
    surgeo_result = model.race_data(63110, 'Naunheim')
    
    # 'White'
    print(surgeo_result.probable_race) 
    
    # '.0328'
    print(surgeo_result.black) 
    
    # 'Naunheim'
    print(surgeo_result.surname) 
    
    # Create new .csv with race data
    model.process_csv(csv_path, new_csv_path) 

If using as a program (if installed can also 'python3 -m surgeo')
--------------

--file argument takes input and output (no return)
::

    surgeo --file /path/input.csv /path/output.csv

--simple takes zip and surname (returns string)
::

    surgeo --simple 63110 Naunheim

    White
    
--complex takes zip and surname (returns detailed string)
::

    surgeo /path_here/executeable.py --complex 63110 Naunheim
    
    probable_race=White
    probable_race_percent=0.817650
    surname=NAUNHEIM
    zip=63110
    hispanic=0.007056
    white=0.817650
    black=0.172591
    asian=0.002249
    indian=0.000077
    multiracial=0.000377

--pipe takes zip and surname arguments
::

    cat | surgeo --pipe

--setup takes no arguments
::

    surgeo --setup


Prefab files
--------------
Windows installer:
https://dl.dropboxusercontent.com/u/26853373/surgeo-0.6.7-amd64.msi

Database link:
https://dl.dropboxusercontent.com/u/26853373/census.db

Database dump:
https://dl.dropboxusercontent.com/u/26853373/sql_dump.txt
