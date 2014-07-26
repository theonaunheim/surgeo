![alt tag](http://i.imgur.com/pe0GZMP.jpg)

<h1>surgeo</h1>

surgeo is a hackish attempt to reverse engineer the Consumer Financial 
Protection Bureau's (CFPB) Bayesian Improved Surname Geocode Analysis (BISG).

Python code by Theo Naunheim. Model created by Mark N. Elliot et al. For 
details, please see BACKGROUND.txt.

<h1>Installing</h1>

<h2>Unix/Linux ('--user' option for unprivileged)</h2>
python3 /path_to_surgeo/surgeo/setup.py install

<h2>Windows ('--user' option for unprivileged)</h2>
/path_to_surgeo/surgeo/setup.py install

<h1>If using as a Python Module</h1>

import surgeo

surgeo.data_setup(verbose=True) # Download data and create tables

model = surgeo.SurgeoModel() # Create model object

model.guess_race(12345, 'Naunheim') # Simple version returns 'White'

surgeo_result = model.race_data(63110, 'Naunheim') # race_data() returns object
print(surgeo_result.probable_race) # 'White'
print(surgeo_result.black) # '.0328'
print(surgeo_result.surname) # 'Naunheim'

model.process_csv(csv_path, new_csv_path) # Create new .csv with race data

<h1>If using as a program</h1>

<h2>GUI version if no arguments</h2>
python3 /path_here/executeable.pyw

<h2>--file argument takes input and output (no return)</h2>
python3 /path_here/executeable.pyw --file /path/input.csv /path/output.csv

<h2>--simple takes zip and surname (returns string)</h2>
python3 /path_here/executeable.pyw --simple 63110 Naunheim

<h2>--complex takes zip and surname (returns detailed string)</h2>
python3 /path_here/executeable.pyw --complex 63110 Naunheim

<h2>--pipe takes comma separated zip and surname</h2>
echo "63110,Naunheim" | python3 /path_here/executeable.pyw --pipe | cat





