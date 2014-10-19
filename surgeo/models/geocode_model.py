
import atexit
import ftplib
import os
import sqlite3
import zipfile

import surgeo

from surgeo.models.model_base import BaseModel
from surgeo.utilities.result import Result
from surgeo.utilities.download_bar import PercentageFTP


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

           Count geocode_data is 581233

        '''

        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        try:
            # geocode_logical
            cursor.execute('''SELECT COUNT(*) FROM geocode_joint''')
            geocode_joint_count = int(cursor.fetchone()[0])
            assert(geocode_joint_count == 581233)
            return True
        except (sqlite3.Error, AssertionError) as e:
            self.logger.exception(''.join([e.__class__.__name__,
                                           ': ',
                                           e.__str__()]))
            return False

    def db_create(self):
        '''Creates geocode database based on Census 2010 data.'''
######## First try prefab database
        surgeo.adapter.adaprint('Trying to download prefabricated db ...')
        try:
            destination = os.path.join(self.temp_folder_path,
                                       'geocode.sqlite')
            ftp_for_prefab = ftplib.FTP('ftp.theonaunheim.com')
            ftp_for_prefab.login()
            PercentageFTP('geocode.sqlite',
                          destination,
                          ftp_for_prefab).start()
            surgeo.adapter.adaprint('Copying data to local table ...')
            connection = sqlite3.connect(self.db_path)
            cursor = connection.cursor()
            cursor.execute('''DROP TABLE IF EXISTS geocode_joint''')
            cursor.execute('''CREATE TABLE IF NOT EXISTS geocode_joint(
                                  id INTEGER PRIMARY KEY,
                                  state TEXT,
                                  summary_level TEXT,
                                  logical_record TEXT,
                                  zcta TEXT)''')
            cursor.execute('''ATTACH ? AS "downloaded_db" ''', (destination,))
            cursor.execute('''INSERT INTO downloaded_db.geocode_joint(*) 
                              SELECT * FROM surgeo.sqlite''')
            connection.commit()
            return
        # Fix naked except.
        except:
            surgeo.adapter.adaprint('Unable to find prefab database ...')
            surgeo.adapter.adaprint('Time-consuming rebuild starting ...')
######## FTP
        surgeo.adapter.adaprint('Creating GeocodeModel database manually ...')
        # Remove downloaded files in event of a hangup.
        atexit.register(self.temp_cleanup)
        surgeo.adapter.adaprint('Signing in to ftp.census.gov ...')
######## Major loop
        for state in self.census_states:
            surgeo.adapter.adaprint('Getting ' + state + ' data' + ' ...')
            ftp = ftplib.FTP('ftp.census.gov')
            ftp.login()
            ftp.cwd('census_2010/04-Summary_File_1')
            ftp.cwd('/')
            ftp.cwd(''.join(['census_2010/04-Summary_File_1', '/', state]))
            callback_pool = []
            ftp.retrlines('NLST', callback=callback_pool.append)
            target_file = [name for name in callback_pool if 'sf1.zip'
                           in name][0]
            destination_zip = os.path.join(self.temp_folder_path,
                                           str(target_file))
            PercentageFTP(target_file,
                          destination_zip,
                          ftp).start()
######## Unzip files
            surgeo.adapter.adaprint('Unzipping files ...')
            with zipfile.ZipFile(destination_zip) as zip_file:
                # __000042010.sf1
                # __geo2010.sf1
                for zip_name in zip_file.namelist():
                    if '032010.sf1' in zip_name or 'geo2010.sf1' in zip_name:
                        with open(os.path.join('/home/theo/.surgeo/temp',
                                               zip_name), 'wb+') as dest_file:
                            zip_data = zip_file.read(zip_name)
                            dest_file.write(zip_data)
######## Commit to db
            try:
                surgeo.adapter.adaprint('Writing to database ...')
                connection = sqlite3.connect(self.db_path)
                cursor = connection.cursor()
                cursor.execute('''DROP TABLE IF EXISTS geocode_joint''')
                cursor.execute('''CREATE TABLE IF NOT EXISTS geocode_logical(
                                  id INTEGER PRIMARY KEY,
                                  state TEXT,
                                  summary_level TEXT,
                                  logical_record TEXT,
                                  zcta TEXT)''')
                cursor.execute('''CREATE TABLE IF NOT EXISTS geocode_race(
                                  id INTEGER PRIMARY KEY,
                                  state TEXT,
                                  logical_record TEXT,
                                  num_white REAL,
                                  num_black REAL,
                                  num_ai REAL,
                                  num_api REAL,
                                  num_hispanic REAL,
                                  num_multi REAL)''')
                cursor.execute('''CREATE TABLE IF NOT EXISTS geocode_joint(
                                  id INTEGER PRIMARY KEY,
                                  zcta TEXT,
                                  num_white REAL,
                                  num_black REAL,
                                  num_ai REAL,
                                  num_api REAL,
                                  num_hispanic REAL,
                                  num_multi REAL)''')
                connection.commit()
                # now start loading to db
                list_of_filenames = os.listdir(self.temp_folder_path)
                for index, filename in enumerate(list_of_filenames):
                    # First the geographic header file
                    if 'geo' in filename:
                        file_path = os.path.join(self.temp_folder_path,
                                                 filename)
                        with open(file_path, 'Ur', encoding='latin-1') as csv1:
                            for line in csv1:
                                state = line[6:8]
                                summary_level = line[8:11]
                                logical_record = line[18:25]
                                zcta = line[171:176]
                                # Only ZCTA wide numbers considered
                                # DESIRED_SUMMARY_LEVEL = '871'
                                if '871' in summary_level:
                                    cursor.execute('''INSERT INTO
                                                      geocode_logical(
                                                      id,
                                                      state,
                                                      summary_level,
                                                      logical_record,
                                                      zcta)
                                                      VALUES(NULL,
                                                             ?,
                                                             ?,
                                                             ?,
                                                             ?)''',
                                                   (state,
                                                    summary_level,
                                                    logical_record,
                                                    zcta))
                for index, filename in enumerate(list_of_filenames):
                    # First the geographic header file
                    if '32010.sf1' in filename:
                        file_path = os.path.join(self.temp_folder_path,
                                                 filename)
                        with open(file_path, 'Ur', encoding='latin-1') as csv2:
                            for line in csv2:
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
                                                  id,
                                                  state,
                                                  logical_record,
                                                  num_white,
                                                  num_black,
                                                  num_ai,
                                                  num_api,
                                                  num_hispanic,
                                                  num_multi)
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
            except sqlite3.Error as e:
                connection.rollback()
                connection.close()
                raise e
            # Delete temp files for this state because DB data gathered.
            surgeo.adapter.adaprint('Cleaning up unused files ...')
            for directory_item in os.listdir(self.temp_folder_path):
                os.remove(os.path.join(self.temp_folder_path, directory_item))
        # Create indicies
        surgeo.adapter.adaprint('Joining tables and indexing ...')
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        try:
            cursor.execute('''INSERT INTO geocode_joint
                              SELECT NULL,
                                     L.zcta,
                                     R.num_white,
                                     R.num_black,
                                     R.num_ai,
                                     R.num_api,
                                     R.num_multi,
                                     R.num_hispanic
                              FROM geocode_logical as L
                              JOIN geocode_race as R
                              ON L.logical_record=R.logical_record''')
            cursor.execute('''DROP TABLE IF EXISTS geocode_race''')
            cursor.execute('''DROP TABLE IF EXISTS geocode_logical''')
            cursor.execute('''CREATE INDEX IF NOT EXISTS zcta_index
                              ON geocode_joint(zcta)''')
            connection.commit()
            connection.close()
        except sqlite3.Error as e:
            connection.rollback()
            connection.close()
            raise e

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

    def get_summary_data(self):
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
        pass

