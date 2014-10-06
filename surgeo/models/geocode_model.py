
import atexit
import collections
import decimal
import ftplib
import itertools
import os
import sqlite3
import sys
import zipfile

import surgeo

from surgeo.models.model_base import BaseModel
from surgeo.utilities.result import Result
from surgeo.utilities.download_bar import graphical_ftp_download


class GeocodeModel(BaseModel):
    '''Contains data references and methods for running a Geocode model.'''

    def __init__(self):
        super().__init__()
        self.census_states = ['Alabama', 'Alaska', 'Arizona', 'Arkansas',
                              'California', 'Colorado', 'Connecticut',
                              'Delaware', 'District_of_Columbia', 'Florida',
                              'Georgia', 'Hawaii', 'Idaho', 'Illinois',
                              'Indiana', 'Iowa', 'Kansas', 'Kentucky',
                              'Louisiana', 'Maine', 'Maryland',
                              'Massachusetts', 'Michigan', 'Minnesota',
                              'Mississippi', 'Missouri', 'Montana', 'Nebraska',
                              'Nevada', 'New_Hampshire', 'New_Jersey',
                              'New_Mexico', 'New_York', 'North_Carolina',
                              'North_Dakota', 'Ohio', 'Oklahoma', 'Oregon',
                              'Pennsylvania', 'Puerto_Rico', 'Rhode_Island',
                              'South_Carolina', 'South_Dakota', 'Tennessee',
                              'Texas', 'Utah', 'Vermont', 'Virginia',
                              'Washington', 'West_Virginia', 'Wisconsin',
                              'Wyoming']

    def db_check(self):
        '''This checks accuracy of database.

           If valid, returns True.
           If invalid, returns False.

           Count geocode_logical is 33233
           Count geocode_data is 9541315

        '''

        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        try:
            # geocode_logical
            cursor.execute('''SELECT COUNT(*) FROM geocode_logical''')
            geocode_logical_count = int(cursor.fetchone()[0])
            assert(geocode_logical_count == 33233)
            # geocode_data
            cursor.execute('''SELECT COUNT(*) FROM geocode_race''')
            geocode_data_count = int(cursor.fetchone()[0])
            assert(geocode_data_count == 9541315)
            return True
        except (sqlite3.Error, AssertionError) as e:
            self.logger.exception(''.join([e.__class__.__name__,
                                           ': ',
                                           e.__str__()]))
            return False

    def db_create(self):
        '''Creates geocode database based on Census 2010 data.'''
######## FTP
        # Remove downloaded files in event of a hangup.
        atexit.register(self.temp_cleanup)
        ftp = ftplib.FTP('ftp.census.gov')
        ftp.login()
        ftp.cwd('census_2010/04-Summary_File_1')
        # Drop all elements prior to states
        zip_files_downloaded = []
######## Major loop
        for state in self.census_states:
            ftp.cwd('/')
            ftp.cwd(''.join(['census_2010/04-Summary_File_1',
                             '/',
                             state]))
            files_for_individual_state = ftp.nlst()
            for state_item in files_for_individual_state:
                if '2010.sf1.zip' in item:
                    file_path = os.path.join(self.temp_folder_path, state_item)
                    # 'downloaded' is a counter at zero. It is accessed 
                    # via a global in graphical_ftp_download . TODO fix this.
                    downloaded = 0
                    graphical_ftp_download(item,
                                           ftp.size(item),
                                           file_path,
                                           ftp)
######## Unzip files as iterator
                    with zipfile.ZipFile(file_path, 'r') as f:
                        for name_item in f.namelist():
                            # __000042010.sf1
                            # __geo2010.sf1
                            if '32010.sf1' or 'geo2010.sf1' in name_item:
                                with f.open(name_item, 'r') as f2:
                                    with open(os.path.join(
                                              self.temp_folder_path,
                                              name_item),
                                              'w+b') as f3:
                                        for line in f2:
                                            f3.write(line)
######## Commit to db
                try:
                    connection = sqlite3.connect(self.db_path)
                    cursor = connection.cursor()
                    cursor.execute('''CREATE TABLE IF NOT EXISTS
                                      geocode_logical(id INTEGER PRIMARY KEY,
                                      state TEXT, summary_level TEXT,
                                      logical_record TEXT, zcta TEXT)''')
                    cursor.execute('''CREATE TABLE IF NOT EXISTS
                                      geocode_race(id
                                      INTEGER PRIMARY KEY, state TEXT,
                                      logical_record TEXT, num_white REAL,
                                      num_black REAL, num_ai REAL,
                                      num_api REAL,
                                      num_hispanic REAL, num_multi REAL)''')
                    # now start loading to db
                    list_of_filenames = os.listdir(self.temp_folder_path)
                    number_of_filenames = len(list_of_filenames)
                    for index, filename in enumerate(list_of_filenames):
                        # First the geographic header file
                        if 'geo.sf1' in filename:
                        file_path = os.path.join(self.temp_folder_path,
                                                 filename)
                        DESIRED_SUMMARY_LEVEL = '871'
                        with open(file_path, 'r') as f4:
                            for line in f3:
                                state = line[6:8]
                                summary_level = line[8:11]
                                logical_record = line[18:25]
                                zcta = line[171:176]
                                # Only ZCTA wide numbers considered
                                if not summary_level == DESIRED_SUMMARY_LEVEL:
                                    continue
                                # Remove 'XX' large / 'HH' hydrological prefixes
                                if 'XX' or 'HH' in zcta:
                                    continue
                                cursor.execute('''INSERT INTO geocode_logical(
                                               id, state, summary_level,
                                               logical_record, zcta)
                                               VALUES(NULL, ?, ?, ?, ?)''',
                                               (state,
                                                summary_level,
                                                logical_record,
                                                zcta))
                    for index, filename in enumerate(list_of_filenames):
                        # First the geographic header file
                        if '32010.sf1' in filename:
                            file_path = os.path.join(self.temp_folder_path,
                                                     filename)
                            with open(file_path, 'r' as f5:
                                for line in f5:
                                    split_line = line.split(',')
                                    state = split_line[1]
                                    logical_record = split_line[4]
                                    table_p5 = split_line[16:33]
                                    # Breaking up table p10
                                    total_pop = table_p5[0]
                                    total_not_hispanic = table_p5[1]
                                    num_white = table_p5[2]
                                    num_black = table_p5[3]
                                    num_ai = table_p5[4]
                                    num_asian = table_p5[5]
                                    num_pacisland = table_p5[6]
                                    num_other = table_p5[7]
                                    num_api = str((int(num_asian) +
                                                   int(num_pacisland)))
                                    num_multi = table_p5[8]
                                    num_hispanic = table_p5[9]
                                    cursor.execute('''INSERT INTO geocode_race(
                                                      id, state, 
                                                      logical_record,
                                                      num_white, num_black,
                                                      num_ai, num_api,
                                                      num_hispanic, num_multi) 
                                                      VALUES(NULL, ?, ?, ?, ?,
                                                      ?, ?, ?, ?)''',
                                                   (state,
                                                    logical_record,
                                                    num_white,
                                                    num_black,
                                                    num_ai,
                                                    num_api,
                                                    num_multi,
                                                    num_hispanic))
                            # Now commit
                    connection.commit()
                    connection.close()
                except
                    connection.rollback()
                    connection.close()
                    raise e
        # Delete temp files.
        for directory_item in os.listdir(self.temp_folder_path):
            os.remove(os.path.join(self.temp_folder_path, directory_item)
        # Create indicies
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        cursor.execute('''CREATE INDEX IF NOT EXISTS zcta_index ON
                          geocode_logical(zcta)''')
        cursor.execute('''CREATE INDEX IF NOT EXISTS logical_record_index
                          ON geocode_race(logical_record)''')
        connection.commit()
        connection.close()


    def get_result_object(self, zip_code):
        '''Takes zip code, returns race object.

           Args:
            zip_code: 5 digit zip code
        Returns:
            Result object with attributes:
                zcta string
                hispanic float
                white float
                black float
                api float
                ai float
                multi float
        Raises:
            None

        '''
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        cursor.execute('''SELECT state, logical_record FROM geocode_logical
                          WHERE zcta=?''', (zip_code,))
        try:
            state, logical_record = cursor.fetchone()
        except TypeError:
            error_result = Result({'zcta': 0,
                                   'hispanic': 0,
                                   'white': 0,
                                   'black': 0,
                                   'api': 0,
                                   'ai': 0,
                                   'multi': 0}).errorify()
            return error_result
        cursor.execute('''SELECT num_hispanic, num_white, num_black,
                          num_api, num_ai, num_multi FROM geocode_race
                          WHERE logical_record=? AND state=?''',
                       (logical_record, state))
        try:
            row = cursor.fetchone()
        except TypeError:
            error_result = Result({'zcta': 0,
                                   'hispanic': 0,
                                   'white': 0,
                                   'black': 0,
                                   'api': 0,
                                   'ai': 0,
                                   'multi': 0}).errorify()
            return error_result
        count_hispanic = row[0]
        count_white = row[1]
        count_black = row[2]
        count_api = row[3]
        count_ai = row[4]
        count_multi = row[5]
        # Float because dividing later
        total = float(count_hispanic +
                      count_white +
                      count_black +
                      count_api +
                      count_ai +
                      count_multi)
        argument_dict = {'zcta': zip_code,
                         'hispanic': round((count_hispanic/total), 5),
                         'white': round((count_white/total), 5),
                         'black': round((count_black/total), 5),
                         'api': round((count_api/total), 5),
                         'ai': round((count_ai/total), 5),
                         'multi': round((count_multi/total), 5)}
        result = Result(**argument_dict)
        return result

