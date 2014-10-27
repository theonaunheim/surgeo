
import atexit
import ftplib
import os
import sqlite3
import zipfile

import surgeo

from surgeo.models.model_base import BaseModel
from surgeo.utilities.result import Result
from surgeo.utilities.download_bar import PercentageFTP
from surgeo.calculate.weighted_mean import get_weighted_mean


class GeocodeModel(BaseModel):
    '''Contains data references and methods for running a Geocode model.

    Attributes
    ----------
    surgeo_folder_path : string
        Path to a shared sqlite3 database connection.
    temp_folder_path : string
        Path to a folder used as a temporary holding area.
    model_folder_path : string
        Path to folder that contains models.
    logger : logging.Logger or logging.RootLogger
        Logger for the individual model.
    db_path : string
        Path to sqlite3 database.
    census_states : list
        List of states from which to download FTP data.

    Methods
    -------
    build_up()
        setups up data as necessary
    db_check()
        checks db for proper table
    db_create()
        creates db tables if necessary
    db_destroy()
        removes database tables associated with this class.
    get_result_object()
        take parameters return result ProxyResult object.
    csv_summary()
        takes csv, returns summary statistic csv.
    csv_process()
        takes two paths. Reads one, writes to another.
    temp_cleanup()
        this function is used with atexit for cleanup.

    '''

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
        '''Checks db accuracy. Valid returns True, else False.

        Parameters
        ----------
        None

        Returns
        -------
        True: Boolean
            If the database is good, returns True.
        False: Boolean
            If database is deficient, returns False.

        Raises
        ------
        sqlite3.Error
            Can occur for any number of database-related reasons. Upon error,
            automatic rollback occurs, but the error is raised because it's
            probably symptomatic of a bigger problem.

        '''
        PROPER_COUNT = 33223
        try:
            connection = sqlite3.connect(self.db_path)
            cursor = connection.cursor()
            # Use row count to determine db validity.
            cursor.execute('''SELECT COUNT(*) FROM geocode_joint''')
            surname_joint_count = int(cursor.fetchone()[0])
            # If passes assertion, return True
            assert(surname_joint_count == PROPER_COUNT)
            return True
        except (sqlite3.Error,
                AssertionError,
                sqlite3.OperationalError) as e:
            self.logger.exception(''.join([e.__class__.__name__,
                                           ': ',
                                           e.__str__()]))
            # If doesn't pass assertion test, log and return False.
            return False

    def db_create(self):
        '''Creates geocode database based on Census 2010 data.

        Where entries are catagorized as "other race", they are allocated in
        accordance with Jirousek and Preucil's article "On the effective
        implementation of the iterative proportional fitting procedure" in
        Comput. Stat. Data Anal. 19(2), 177–189 (1995). The proportions are:
        70.5% White, 11.1% Hispanic, 11.3% Black, 7.0% API, 0.8% multiracial,
        and 0.9% AI/AN.

        '''

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
                                  zcta TEXT,
                                  num_white REAL,
                                  num_black REAL,
                                  num_ai REAL,
                                  num_api REAL,
                                  num_hispanic REAL,
                                  num_multi REAL)''')
            cursor.execute('''ATTACH ? AS "downloaded_db" ''', (destination,))
            cursor.execute('''INSERT INTO geocode_joint
                              SELECT * FROM downloaded_db.geocode_joint''')
            cursor.execute('''CREATE INDEX IF NOT EXISTS zcta_index
                              ON geocode_joint(zcta)''')
            connection.commit()
            surgeo.adapter.adaprint('Successfully written ...')
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
                                if summary_level == '871':
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
                                num_other = int(table_p5[7])
                                # Other goes into categories in the following
                                # proportions (iternative fitting) white 70.5%
                                # black 11.3%, hispanic 11.1% api 7.0%
                                # multi .8%, ai_an .9%
                                # Note that Asian and pacific islanders are
                                # lumped together also Alaskan Native/Native Am
                                white_partial = num_other * float(.705)
                                black_partial = num_other * float(.113)
                                hispanic_partial = num_other * float(.111)
                                api_partial = num_other * float(.070)
                                multi_partial = num_other * float(.008)
                                ai_an_partial = num_other * float(.009)
                                num_white = (int(table_p5[2]) +
                                             int(white_partial))
                                num_black = (int(table_p5[3]) +
                                             int(black_partial))
                                num_ai = (int(table_p5[4]) +
                                          int(ai_an_partial))
                                num_asian = table_p5[5]
                                num_pacisland = table_p5[6]
                                num_other = table_p5[7]
                                num_api = str((int(num_asian) +
                                               int(num_pacisland) +
                                               int(api_partial)))
                                num_multi = (int(table_p5[8]) +
                                             int(multi_partial))
                                num_hispanic = (int(table_p5[9]) +
                                                int(hispanic_partial))
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
                              ON L.logical_record=R.logical_record
                              WHERE L.state=R.state''')
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
        print(zip_code)
        print(type(zip_code))
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        cursor.execute('''SELECT * FROM geocode_joint
                          WHERE zcta=?''', (zip_code,))
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
        zcta = row[1]
        count_hispanic = row[6]
        count_white = row[2]
        count_black = row[3]
        count_api = row[5]
        count_ai = row[4]
        count_multi = row[7]
        # Float because dividing later
        total = float(count_hispanic +
                      count_white +
                      count_black +
                      count_api +
                      count_ai +
                      count_multi)
        argument_dict = {'zcta': zcta,
                         'hispanic': round((count_hispanic/total), 5),
                         'white': round((count_white/total), 5),
                         'black': round((count_black/total), 5),
                         'api': round((count_api/total), 5),
                         'ai': round((count_ai/total), 5),
                         'multi': round((count_multi/total), 5)}
        result = Result(**argument_dict)
        return result

    def db_destroy(self):
        '''Destroy database.'''
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        cursor.execute('''DROP TABLE IF EXISTS geocode_race''')
        cursor.execute('''DROP TABLE IF EXISTS geocode_logical''')
        cursor.execute('''DROP TABLE IF EXISTS geocode_joint''')
        connection.commit()
        connection.close()

    def csv_summary(self,
                    csv_path_in,
                    summary_path_out):
        '''Wraps get_weighted_mean()'''
        for index, line in enumerate(open(csv_path_in, 'r')):
            if index > 1:
                break
            if index == 0:
                first_line = line.split(',')
            if index == 2:
                second_line = line.split(',')
        # List of lines
        line_list_1 = [item.replace('\"', '').replace('\'', '').strip()
                       for item in first_line]
        line_list_2 = [item.replace('\"', '').replace('\'', '').strip()
                       for item in first_line]
        # Indices to become tuples
        percent_index = []
        subject_index = []
        # Create percent index
        for row_index, row_item in enumerate(line_list_1):
            if any(['hispanic',
                    'white',
                    'black',
                    'api',
                    'ai',
                    'multi']) in row_item:
                percent_index.append(row_index)
        # Create subject index
        for row_index, row_item in enumerate(line_list_2):
            try:
                int(row_item)
                # It's an integer. Add to the index.
                subject_index.append(row_index)
            except ValueError:
                continue
        get_weighted_mean(tuple(percent_index),
                          tuple(subject_index),
                          csv_path_in,
                          summary_path_out)

    def csv_process(self,
                    filepath_in,
                    filepath_out):
        '''Thin wrapper around the BaseModel's csv_process method.

        This looks for the 'zip'-related items.

        Args:
            filepath_in: file path of csv from which data is read
            filepath_out: file path of csv where data is written
        Returns:
            None
        Raises:
            SurgeoError

        '''
        # TODO: Make so all subclassed or all imported as functions.
        for index, line in enumerate(open(filepath_in, 'r')):
            if index > 0:
                break
            first_line = line.split(',')
        # Separate
        line_list = [item.replace('\"', '').replace('\'', '').strip()
                     for item in first_line]
        for index, item in enumerate(line_list):
            if item.lower() in ['zip', 'zcta', 'zip code', 'zip_code']:
                super().csv_process(filepath_in,
                                    filepath_out,
                                    (item,),
                                    ('zip_code',),
                                    continue_on_model_fail=True)
            # Prevent multiple hits
            return

