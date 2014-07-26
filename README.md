![alt tag](http://i.imgur.com/pe0GZMP.jpg)

surgeo
========

surgeo is a hackish attempt to reverse engineer the Consumer Financial 
Protection Bureau's (CFPB) Bayesian Improved Surname Geocode Analysis (BISG).

Python code by Theo Naunheim. Model created by Mark N. Elliot et al. For 
details, please see BACKGROUND.txt.

###########################
Installing
###########################

# Unix/Linux ('--user' option for unprivileged)
python3 /path_to_surgeo/surgeo/setup.py install

# Windows ('--user' option for unprivileged)
/path_to_surgeo/surgeo/setup.py install

###########################
If using as a Python Module
###########################

import surgeo

surgeo.data_setup(verbose=True) # Download data and create tables

model = surgeo.SurgeoModel() # Create model object

model.guess_race(12345, 'Naunheim') # Simple version returns 'White'

surgeo_result = model.race_data(63110, 'Naunheim') # race_data() returns object
print(surgeo_result.probable_race) # 'White'
print(surgeo_result.black) # '.0328'
print(surgeo_result.surname) # 'Naunheim'

model.process_csv(csv_path, new_csv_path) # Create new .csv with race data

###########################
If using as a program
###########################

# GUI version if no arguments
python3 /path_here/executeable.pyw

# --file argument takes input and output (no return)
python3 /path_here/executeable.pyw --file /path/input.csv /path/output.csv

# --simple takes zip and surname (returns string)
python3 /path_here/executeable.pyw --simple 63110 Naunheim

# --complex takes zip and surname (returns detailed string)
python3 /path_here/executeable.pyw --complex 63110 Naunheim

# --pipe takes comma separated zip and surname
echo "63110,Naunheim" | python3 /path_here/executeable.pyw --pipe | cat





