.. image::http://i.imgur.com/pe0GZMP.jpg

Surgeo
==============

Surgeo is a hackish attempt to reverse engineer the Consumer Financial 
Protection Bureau's (CFPB) Bayesian Improved Surname Geocode Analysis (BISG).

Python code by Theo Naunheim. Model created by Mark N. Elliot et al. For 
details, please see BACKGROUND.txt.

Created as a trial run so that when the CFPB releases its whitepaper on proxy 
analysis Summer 2014, the model can be quickly adapted to conform to it. I am
not a developer nor a statistician, so please use at your own risk.

Installing
--------------

Unix/Linux ('--user' option for unprivileged)

::
    python3 /path_to_surgeo/surgeo/setup.py install

Windows ('--user' option for unprivileged)

::
    \path_to_surgeo\surgeo\setup.py install

If using as a Python module in your program
--------------

::
    import surgeo
    # Download data and create tables
    surgeo.data_setup(verbose=True)
    # Create model object
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
    python3 /path_here/executeable.pyw --file /path/input.csv /path/output.csv

--simple takes zip and surname (returns string)
::
    python3 /path_here/executeable.pyw --simple 63110 Naunheim

--complex takes zip and surname (returns detailed string)
::
    python3 /path_here/executeable.pyw --complex 63110 Naunheim

--pipe takes comma separated zip and surname
::
    echo "63110,Naunheim" | python3 /path_here/executeable.pyw --pipe | cat

--setup takes no arguments
::
    python3 /path_here/executeable.pyw --setup

No arguments at all starts GUI
::
    python3 /path_here/executeable.pyw

Prefab files for offline use
--------------
Database link:
https://dl.dropboxusercontent.com/u/26853373/census.db

Logo link:
https://dl.dropboxusercontent.com/u/26853373/logo.gif









