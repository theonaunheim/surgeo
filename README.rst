.. image:: logo.gif

Surgeo
==============

**Link to Windows installer at bottom.**

Surgeo is an attempt to reverse engineer the Consumer Financial Protection 
Bureau's (CFPB) Bayesian Improved Surname Geocode Analysis (BISG). Python code 
by Theo Naunheim. Model created by Mark N. Elliot et al. For details, please 
see BACKGROUND.txt.

Please note that your shortcut to Python may be 'python' or 'python3' 
depending on how it is installed. Command line utility only as of August 2014 
(run through cmd.exe). GUI later.

Version v0.6.8:

1) more closely mimics the CFPB model by only providing valid results where 
both name and zip are availible.
2) fixes a misapplication of iterative proportional fitting.
3) Still uses 2000 census data (see 'dev' branch for rewrite)


Installing
--------------

::

    # to install as program
    
    <Download installer at link below. Run. Don't forget to --setup!>
    
    
    # or to install as module

    pip3 install surgeo
    
    
    # or (less preferred option)
    
    python3 <path_to_setup.py> install
    
    
If using as a program (Windows Installer)
--------------

On Windows, open the 'cmd.exe' program and type the commands below.

--setup needs to be run before program will work. Requires internet access.
::

    surgeo --setup

--file argument takes input and output (no return)
::

    surgeo --file /path/input.csv /path/output.csv

--simple takes zip and surname (returns string)
::

    surgeo --simple 63110 Jones

    'White'
    
--complex takes zip and surname (returns detailed string)
::

    surgeo --complex 63110 Jones
    
   "probable_race=White
    probable_race_percent=0.817650
    surname=JONES
    zip=63110
    hispanic=0.007056
    white=0.817650
    black=0.172591
    asian=0.002249
    indian=0.000077
    multiracial=0.000377"

--pipe takes zip and surname arguments
::

    cat | surgeo --pipe


If running program as a module
--------------

Much like the above, but instead of 'surgeo' you will type 'python3 -m surgeo'

::

    python3 -m surgeo --simple 63110 Jones
    
    'White'
    

If using as a Python module in your program
--------------

::

    import surgeo
    
    # Download data and create tables (takes some time)
    surgeo.data_setup(verbose=True)
    
    # Create model object (SurModel and GeoModel also exist)
    model = surgeo.SurgeoModel() 
    
    # Simple version returns 'White'
    model.guess_race(63110, 'Jones') 
    
    # race_data() returns object
    surgeo_result = model.race_data(63110, 'Jones')
    
    # 'White'
    print(surgeo_result.probable_race) 
    
    # '.0328'
    print(surgeo_result.black) 
    
    # 'JONES'
    print(surgeo_result.surname) 
    
    # Create new .csv with race data
    model.process_csv(csv_path, new_csv_path) 
    

Prefab files
--------------
Windows installer:
https://dl.dropboxusercontent.com/u/26853373/surgeo-0.6.7-amd64.msi

