'''This loads the database to ram for quick access.'''

import io
import os
import sqlite3
import sys
import traceback

def db_to_ram(verbose):
    '''This function loads the database to ram and returns a database object.'''
    db_path = os.path.join(os.path.expanduser('~'),
                           '.surgeo',
                           'census.db')
    if verbose == True:
        sys.stdout.write('Populating ram db ... \n')
    # Create temporary file and write all rows to file.
    temporary_file = io.StringIO()
    try:
        connection = sqlite3.connect(db_path)
        for index, row in enumerate(connection.iterdump()):
            temporary_file.write('{}'.format(row))
            if verbose == True:
                if index % 10000 == 0:
                    sys.stdout.write('\rPreparing rows: {}'.format(index))
        connection.close()  
    except sqlite3.Error as e:
        traceback.print_exc()
        connection.close()
        raise e
    # Create new sqlite3 database in ram and write tempfile.
    if verbose == True:
        sys.stdout.write('\n')
    temporary_file.seek(0)
    temporary_file_items = temporary_file.getvalue().count(';')
    try:
        ram_db = sqlite3.connect(':memory:')
        ram_cursor = ram_db.cursor()
        # Last rows have commit items.
        for index, line in enumerate(temporary_file.getvalue().split(';')[:-2]):
            ram_cursor.execute(''.join([line,';']))
            if verbose == True:
                try:
                    last_write
                except NameError:
                    last_write = 1
                if index > last_write:
                    if index % 10000 == 0:
                        sys.stdout.write('\rDumping db to ram: {} of {}'
                                         .format(index,
                                                 temporary_file_items)) 
                        last_write = index 
        if verbose == True:                                           
            sys.stdout.write('\rDumping db to ram: {} of {}\n'
                              .format(temporary_file_items,
                                      temporary_file_items))  
            sys.stdout.write('Committing ...')
            sys.stdout.flush()
        ram_db.commit()
    except sqlite3.Error as e:
        traceback.print_exc()
        ram_db.rollback()
        ram_db.commit()
        ram_db.close()
        raise e
    if verbose == True:
        sys.stdout.write('\t\t\t\t{}OK{}\n'.format('\033[92m','\033[0m'))
    return ram_db
        
        
        
                   

            
        
