import atexit
import ftplib
import os
import sqlite3
import zipfile

import surgeo

from surgeo.models.model_base import BaseModel
from surgeo.utilities.result import Result
from surgeo.utilities.download_bar import PercentageFTP
from surgeo.utilities.download_bar import PercentageHTTP
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
        '''Uses the base class __init__. build_up() runs at conclusion.

        Parameters
        ----------
        None

        Returns
        -------
        None

        Raises
        ------
        None

        '''
        super().__init__()

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
        PROPER_COUNT = 151671
        try:
            connection = sqlite3.connect(self.db_path)
            cursor = connection.cursor()
            # Use row count to determine db validity.
            cursor.execute('''SELECT COUNT(*) FROM surname_joint''')
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
        '''Creates surname database based on Census 2000 data.

        This downloads a single census data file which gives the relative
        ethnic makeup for each individual name. It only includes names with
        over 100 instances. Certain elements are scrubbed for anonymity's sake
        from the original database. The anonymized entries are summed and
        divided among the applicable entries.

        Parameters
        ----------
        None

        Returns
        -------
        None

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
            # Custom function for graphical ftp
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
                              pct_white REAL,
                              pct_black REAL,
                              pct_api REAL,
                              pct_ai_an REAL,
                              pct_2_or_more REAL,
                              pct_hispanic REAL)''')
            # Copy foreign db into local db
            cursor.execute('''ATTACH ? AS "downloaded_db" ''', (destination,))
            cursor.execute('''INSERT INTO surname_joint
                              SELECT * FROM downloaded_db.surname_joint''')
            cursor.execute('''CREATE INDEX IF NOT EXISTS surname_index
                              ON surname_joint(name)''')
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
        url = 'http://www2.census.gov/topics/genealogy/2000surnames/names.zip'
        title = 'names.zip'
        destination_path = os.path.join(self.temp_folder_path,
                                        title)
        PercentageHTTP(url,
                       destination_path,
                       title).start()
######## Unzip files
        surgeo.adapter.adaprint('Unzipping files ...')
        with zipfile.ZipFile(destination_path) as zip_file:
            data = zip_file.read('app_c.csv')
        new_csv_path = os.path.join(self.temp_folder_path,
                                    'app_c.csv')
        with open(new_csv_path, 'wb+') as f:
            f.write(data)
######## Write to db
        surgeo.adapter.adaprint('Writing to database ...')
        try:
            connection = sqlite3.connect(self.db_path)
            cursor = connection.cursor()
            cursor.execute('''DROP TABLE IF EXISTS surname_joint''')
            cursor.execute('''CREATE TABLE IF NOT EXISTS surname_joint(
                              id INTEGER PRIMARY KEY,
                              name TEXT,
                              pct_white REAL,
                              pct_black REAL,
                              pct_api REAL,
                              pct_ai_an REAL,
                              pct_2_or_more REAL,
                              pct_hispanic REAL)''')
            # Open csv file.
            with open(new_csv_path, 'Ur', encoding='latin-1') as csv:
                for index, line in enumerate(csv):
                    # Skip row 0
                    if index == 0:
                        continue
                    line = line.split(',')
                    name = line[0]
                    rank = line[1]
                    count = line[2]
                    prop1000k = line[3]
                    cum_prop1000k = line[4]
                    pct_white = line[5]
                    pct_black = line[6]
                    pct_api = line[7]
                    pct_ai_an = line[8]
                    pct_2_or_more = line[9]
                    pct_hispanic = line[10].replace('\n', '')
                    # Reconstitute data (missing represented by '(S)')
                    if '(S)' in line:
                        percentage_dict = {'pct_white': pct_white,
                                           'pct_black': pct_black,
                                           'pct_api': pct_api,
                                           'pct_ai_an': pct_ai_an,
                                           'pct_2_or_more': pct_2_or_more,
                                           'pct_hispanic': pct_hispanic}
                        redacted_pers = {key: value
                                         for key, value in
                                         percentage_dict.items()
                                         if value == '(S)'}
                        non_redacted_pers = {key: float(value)
                                             for key, value in
                                             percentage_dict.items()
                                             if value != '(S)'}
                        # Sum non redacted (should be floats). dict_values
                        # requires a list wrapper.
                        values = list(non_redacted_pers.values())
                        non_redacted_sum = sum(values)
                        redacted_sum = float(100 - non_redacted_sum)
                        len_redacted_per = len(redacted_pers)
                        average_redacted_percentage = (redacted_sum /
                                                       len_redacted_per)
                        percentage_dict = {key:
                                           (average_redacted_percentage if
                                            value == '(S)' else value)
                                           for key, value
                                           in percentage_dict.items()}
                    # If no reconstitution required
                    else:
                        percentage_dict = {'pct_white': float(pct_white),
                                           'pct_black': float(pct_black),
                                           'pct_api': float(pct_api),
                                           'pct_ai_an': float(pct_ai_an),
                                           'pct_2_or_more':
                                           float(pct_2_or_more),
                                           'pct_hispanic': float(pct_hispanic)}
                    # Create tuple for insertion
                    formatted_dict = {key: round(float(value)/100, 5)
                                      for key, value
                                      in percentage_dict.items()}
                    insertion_tuple = (name,
                                       formatted_dict['pct_white'],
                                       formatted_dict['pct_black'],
                                       formatted_dict['pct_api'],
                                       formatted_dict['pct_ai_an'],
                                       formatted_dict['pct_2_or_more'],
                                       formatted_dict['pct_hispanic'])
                    cursor.execute('''INSERT INTO surname_joint
                                      VALUES(NULL, ?, ?, ?, ?, ?, ?, ?)''',
                                   insertion_tuple)
                surgeo.adapter.adaprint('Creating index ...')
                cursor.execute('''CREATE INDEX IF NOT EXISTS surname_index
                                  ON surname_joint(name)''')
                connection.commit()
                connection.close()
        except sqlite3.Error as e:
            connection.rollback()
            connection.commit()
            raise e

    def get_result_object(self, surname):
        '''Takes last name, returns race object.

        Parameters
        ----------
        surname : string
            This is the name for which you are getting data.

        Returns
        -------
        result : surgeo.Result
            The return is not an error result, it is a custom object which
            contains attributes:
                *surname : string
                *hispanic : string
                *white : string
                *black : string
                *api : string
                *ai : string
                *multi : string

        Raises
        ------
        sqlite3.Error
            Can occur for any number of database-related reasons. Upon error,
            automatic rollback occurs, but the error is raised because it's
            probably symptomatic of a bigger problem.

        '''
        upper_surname = surname.upper()
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        cursor.execute('''SELECT * FROM surname_joint
                          WHERE name=?''', (upper_surname,))
        row = cursor.fetchone()
######## Error result. Terminates with returning error result
        if row is None:
            error_result = Result(**{'name': 0,
                                     'hispanic': 0,
                                     'white': 0,
                                     'black': 0,
                                     'api': 0,
                                     'ai': 0,
                                     'multi': 0}).errorify()
            return error_result
        name = row[1]
        count_hispanic = row[7]
        count_white = row[2]
        count_black = row[3]
        count_api = row[4]
        count_ai = row[5]
        count_multi = row[6]
        # Float because dividing later
        total = float(count_hispanic +
                      count_white +
                      count_black +
                      count_api +
                      count_ai +
                      count_multi)
        argument_dict = {'surname': name,
                         'hispanic': round((count_hispanic/total), 5),
                         'white': round((count_white/total), 5),
                         'black': round((count_black/total), 5),
                         'api': round((count_api/total), 5),
                         'ai': round((count_ai/total), 5),
                         'multi': round((count_multi/total), 5)}
        result = Result(**argument_dict)
        return result

    def db_destroy(self):
        '''Destroy database.

        Parameters
        ----------
        None

        Returns
        -------
        None

        Raises
        ------
        sqlite3.Error
            Can occur if you have not yet created a database.

        '''
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        cursor.execute('''DROP TABLE IF EXISTS surname_joint''')
        connection.commit()
        connection.close()

    def csv_summary(self,
                    csv_path_in,
                    summary_path_out=''):
        '''Wraps get_weighted_mean().

        Parameters
        ----------
        csv_path_in : string
            The csv from which you are gathering your data.
        summary_path_out : string
            The location to which you are sending the summary data.

        Returns
        -------
        None

        Raises
        ------
        sqlite3.Error
            Can occur for any number of database-related reasons. Upon error,
            automatic rollback occurs, but the error is raised because it's
            probably symptomatic of a bigger problem.

        '''
        HEADER_LIST = ['hispanic',
                       'white',
                       'black',
                       'api',
                       'ai',
                       'multi']
        for index, line in enumerate(open(csv_path_in, 'r')):
            if index > 1:
                break
            if index == 0:
                first_line = line.split(',')
            if index == 1:
                second_line = line.split(',')
        # List of lines
        line_list_1 = [item.replace('\"', '').replace('\'', '').strip()
                       for item in first_line]
        line_list_2 = [item.replace('\"', '').replace('\'', '').strip()
                       for item in second_line]
        # Indices to become tuples
        percent_index = []
        subject_index = []
        # Create percent index
        for row_index, row_item in enumerate(line_list_1):
            for header_item in HEADER_LIST:
                if header_item in row_item:
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

        Parameters
        ----------
        filepath_in : string
            File path of csv from which data is read
        filepath_out : string
            File path of csv where data is written

        Returns
        -------
        None

        Raises
        ------
        None

        '''
        HEADER_LIST = ['name', 'surname', 'last_name', 'last name']
        # TODO: Make so all subclassed or all imported as functions.
        for index, line in enumerate(open(filepath_in, 'r')):
            if index > 0:
                break
            first_line = line.split(',')
        # Separate
        line_list = [item.replace('\"', '').replace('\'', '').strip()
                     for item in first_line]
        for item in line_list:
            if item.lower() in HEADER_LIST:
                super().csv_process(filepath_in,
                                    filepath_out,
                                    (item,),
                                    ('surname',),  # TODO
                                    continue_on_model_fail=True)
            # Prevent multiple hits
            return

