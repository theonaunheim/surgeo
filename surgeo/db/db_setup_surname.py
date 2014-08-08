
import configparser
import decimal
import os
import sqlite3
import sys
import time
import traceback
import urllib.request
import zipfile

def setup_surname_table(verbose):
    '''This creates the surname database and does housekeeping.
    
    It takes no arguments.
    
    This downloads a single census data file which gives the relative ethnic 
    makeup for each individual name. It only includes names with over 100 
    instances.'''
    if verbose == True:
        sys.stdout.write('Checking db existence ... \t\t\t')
    db_path = os.path.join(os.path.expanduser('~'),
                           '.surgeo',
                           'census.db')    
    zipfile_path = os.path.join(os.path.expanduser('~'),
                                '.surgeo',
                                'data.zip')  
    csv_path = os.path.join(os.path.expanduser('~'),
                            '.surgeo',
                            'census_data.csv')               
    if not os.path.exists(db_path):
        if verbose == True:
            sys.stdout.write('{}FAIL{}\n'.format('\033[91m','\033[0m'))
            sys.stdout.write('Creating db ... \n')
        config_path = os.path.join(os.path.expanduser('~'),
                                   '.surgeo',
                                   'configuration.txt')
        parser_instance = configparser.ConfigParser()
        parser_instance.read(config_path)
        url = 'http://www.census.gov/genealogy/www/data/2000surnames/names.zip'
        # No try block for url. If it fails, no point in continuing.     
        #site = urllib.request.urlopen(url)
        #length_in_bytes = int(site.info()['Content-Length'])
        if verbose == True:
            urllib.request.urlretrieve(url,
                                       zipfile_path,
                                       download_bar)
        else:
            urllib.request.urlretrieve(url,
                                       zipfile_path)
        if verbose == True:
            sys.stdout.write('\n')
        # Done
        if verbose == True:
            sys.stdout.write('Re-checking folder setup ... \t\t\t')
            sys.stdout.write('{}OK{}\n'.format('\033[92m','\033[0m'))
            # Zip file
            sys.stdout.write('Extracting zip file ... \t\t\t')
        time.sleep(0)
        with zipfile.ZipFile(zipfile_path, 'r') as f:
            data = f.read('app_c.csv')
        # Write zip data to csv
        time.sleep(0)
        with open(csv_path, 'wb+') as f:
            f.write(data)
        if verbose == True:
            sys.stdout.write('{}OK{}\n'.format('\033[92m','\033[0m'))
        # Write line by line of csv to db
        csv_lines = open(csv_path, 'r').readlines()
        time.sleep(0)
        csv_length = len(csv_lines)
        line_count = 0
        # Create DB
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
        try:
            cursor.execute('''CREATE TABLE IF NOT EXISTS surname_data (id 
                              INTEGER PRIMARY KEY, name TEXT, rank INTEGER, 
                              count INTEGER, prop1000K REAL, cum_prop100K REAL, 
                              pctwhite REAL, pctblack REAL, pctapi REAL, 
                              pctaian REAL, pct2prace REAL, 
                              pcthispanic REAL)''')
            cursor.execute('''CREATE INDEX IF NOT EXISTS name_index ON 
                              surname_data(name)''')
            # Strip csv header.
            for line in csv_lines[1:]:
                time.sleep(0)
                cursor.execute('''INSERT into surname_data VALUES (NULL, ?, ?,
                                  ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                                  (line.split(',')))
                line_count += 1
                percent = int(decimal.Decimal(line_count) / 
                              decimal.Decimal(csv_length) * 100)
                if verbose == True:
                    try:
                        last_written_percent
                    except NameError:
                        last_written_percent = 0
                    # Prevent flicker. Only update when percentage changes
                    if percent > last_written_percent:
                        sys.stdout.write('\rItems written: {}%'.format(percent))
                        last_written_percent = percent
            if verbose == True:
                sys.stdout.write('\rItems written: 100%')
                sys.stdout.write('\n')
                sys.stdout.write('Db write cleanup ... \t\t\t\t')
            connection.commit()
            connection.close()
            if verbose == True:
                sys.stdout.write('{}OK{}\n'.format('\033[92m','\033[0m'))
        except sqlite3.Error as e:
            traceback.print_exc()
            connection.rollback()
            connection.close()
            raise e
    else:
        if verbose == True:
            sys.stdout.write('{}OK{}\n'.format('\033[92m','\033[0m'))
            
def download_bar(block_count, block_size, total_size):
    '''Report hook for use in db_setup_in_ram function.'''
    percentage = int((decimal.Decimal(block_count) * 
                      decimal.Decimal(block_size) /
                      decimal.Decimal(total_size) * 100))
    sys.stdout.write('\rDownloading surname data: {}%'.format(str(percentage)))
    time.sleep(0)


