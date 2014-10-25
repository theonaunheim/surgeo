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


class SurnameModel(BaseModel):
    '''Contains data references and methods for running a Surname model.

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
        '''Uses the base class __init__. build_up() runs at conclusion.'''
        super().__init__()

    def db_check(self):
        '''Checks db accuracy. Valid returns True, else False.

        Returns
        -------
        Boolean
            If the database is good, returns True. Otherwise returns false.

        '''

        try:
            connection = sqlite3.connect(self.db_path)
            cursor = connection.cursor()
            # Use row count to determine db validity.
            cursor.execute('''SELECT COUNT(*) FROM surname_main''')
            surname_main_count = int(cursor.fetchone()[0])
            # If passes assertion, return True
            assert(surname_main == XXXXX)
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
        '''Creates surname database based on Census 2000 data.

        This downloads a single census data file which gives the relative
        ethnic makeup for each individual name. It only includes names with
        over 100 instances. Certain elements are scrubbed for anonymity's sake
        from the original database. The anonymized entries are summed and
        divided among the applicable entries.

        Where entries are catagorized as "other race", they are allocated in
        accordance with Jirousek and Preucil's article "On the effective
        implementation of the iterative proportional fitting procedure" in
        Comput. Stat. Data Anal. 19(2), 177–189 (1995). The proportions are:
        70.5% White, 11.1% Hispanic, 11.3% Black, 7.0% API, 0.8% multiracial,
        and 0.9% AI/AN.

        Raises
        ------
        sqlite3.Error
            Can occur for any number of database-related reasons. Upon error,
            automatic rollback occurs, but the error is raised because it's
            probably symptomatic of a bigger problem.

        '''

######## First try prefab database
        surgeo.adapter.adaprint('Trying to download prefabricated db ...')
        try:
            destination = os.path.join(self.temp_folder_path,
                                       'surname.sqlite')
            ftp_for_prefab = ftplib.FTP('ftp.theonaunheim.com')
            ftp_for_prefab.login()
            PercentageFTP('surname.sqlite',
                          destination,
                          ftp_for_prefab).start()
            surgeo.adapter.adaprint('Copying data to local table ...')
            connection = sqlite3.connect(self.db_path)
            cursor = connection.cursor()
            cursor.execute('''DROP TABLE IF EXISTS surname_joint''')
            cursor.execute('''CREATE TABLE IF NOT EXISTS surname_joint(
                              id INTEGER PRIMARY KEY,
                              name TEXT,
                              pctwhite REAL,
                              pctblack REAL,
                              pctapi REAL,
                              pctaian REAL,
                              pct2prace REAL,
                              pcthispanic REAL)''')
            cursor.execute('''ATTACH ? AS "downloaded_db" ''', (destination,))
            cursor.execute('''INSERT INTO surname_joint
                              SELECT * FROM downloaded_db.surname_joint''')
            connection.commit()
            surgeo.adapter.adaprint('Successfully written ...')
            return
        # Fix naked except.
        except:
            surgeo.adapter.adaprint('Unable to find prefab database ...')
            surgeo.adapter.adaprint('Time-consuming rebuild starting ...')
######## Downloads
        surgeo.adapter.adaprint('Creating SurnameModel database manually ...')
        # Remove downloaded files in event of a hangup.
        atexit.register(self.temp_cleanup)
        surgeo.adapter.adaprint('Downloading files ...')
        url = 'http://www.census.gov/genealogy/www/data/2000surnames/names.zip'
        title = 'names.zip'
        destination_path = ''.join([self.temp_folder_path,
                                    title])
        PercentageHTTP(url,
                       destination_path,
                       title).start()
######## Unzip files
        surgeo.adapter.adaprint('Unzipping files ...')
        with zipfile.ZipFile(destination_path) as zip_file:
            data = f.read('app_c.csv')
        new_csv_path = ''.join([self.temp_folder_path,
                                'app_c.csv'])
        with open(new_csv_path, 'wb+') as f:
            f.write(data)
        
# TODO


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
                if verbose is True:
                    try:
                        last_written_percent
                    except NameError:
                        last_written_percent = 0
                    # Prevent flicker. Only update when percentage changes
                    if percent > last_written_percent:
                        sys.stdout.write('\rItems written: {}%'.
                                         format(percent))
                        last_written_percent = percent
            if verbose is True:
                sys.stdout.write('\rItems written: 100%')
                sys.stdout.write('\n')
                sys.stdout.write('Db write cleanup ... \t\t\t\t')
            connection.commit()
            connection.close()
            if verbose is True:
                sys.stdout.write('OK\n')
        except sqlite3.Error as e:
            traceback.print_exc()
            connection.rollback()
            connection.close()
            raise e
            
    try:
        cursor = redacted_db.cursor()
        altered_rows = []
        for row in cursor.execute('''SELECT * FROM surname_data'''):
            time.sleep(0)
            primary_key = row[0]
            surname = row[1]
            rank = row[2]
            count = row[3]
            prop1000k = row[4]
            cum_prop1000k = row[5]
            pctwhite = row[6]
            pctblack = row[7]
            pctapi = row[8]
            pctaian = row[9]
            pct2prace = row[10]
            # For some reason the last elemet often has a newline
            if type(row[11]) is str:
                pcthispanic = row[11].replace('\n', '')
            else:
                pcthispanic = row[11]
            # Per the study, the total number of redacted names is divided
            # by the number of redacted entries yielding an approximation.
            percentages = [pctwhite,
                           pctblack,
                           pctapi,
                           pctaian,
                           pct2prace,
                           pcthispanic]
            # Do not alter row unless it contains '(S)', which denotes redacted
            if not '(S)' in row:
                continue
            non_redacted = [x for x in percentages if not x == '(S)']
            redacted = [x for x in percentages if x == '(S)']
            non_redacted_percentage = sum(non_redacted)
            redacted_percentage = float(100) - (non_redacted_percentage)
            count_redacted_total = float(count) * redacted_percentage / 100
            count_per_redacted_item = round(count_redacted_total /
                                            len(redacted))
            # All redacted items set the same and added to list of altered rows
            for redacted_item in redacted:
                redacted_item = count_per_redacted_item
            # Add altered row to altered_rows
            altered_rows.append(row)
        for row in altered_rows:
            time.sleep(0)
            primary_key = row[0]
            cursor.execute('''DELETE FROM surname_data WHERE id=?''',
                           (primary_key,))
            cursor.execute('''INSERT INTO surname_data VALUES
                              (?,?,?,?,?,?,?,?,?,?,?,?)''', row)
        # Index via name to speed up searches
    except sqlite3.Error as e:
        traceback.print_exc()
        redacted_db.rollback()
        redacted_db.commit()
        raise e














##############################################
               




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
        cursor.execute('''DROP TABLE IF EXISTS geocode_logical''')
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
        for item in line_list:
            if item.lower() in ['zip', 'zcta', 'zip code', 'zip_code']:
                super().csv_process(filepath_in,
                                    filepath_out,
                                    (item,),
                                    (zip_code,),
                                    continue_on_model_fail=True)
            # Prevent multiple hits
            return

