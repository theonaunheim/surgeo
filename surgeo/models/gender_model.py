import atexit
import collections
import itertools
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


class GenderNameModel(BaseModel):
    '''Contains data references and methods for running a Gender/Name model.

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
        self._author = 'Theo Naunheim'
        self._version = '2013.1'

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
        PROPER_COUNT = 33072
        try:
            connection = sqlite3.connect(self.db_path)
            cursor = connection.cursor()
            # Use row count to determine db validity.
            cursor.execute('''SELECT COUNT(*) FROM gendername_joint''')
            count = int(cursor.fetchone()[0])
            # If passes assertion, return True
            assert(count == PROPER_COUNT)
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
        '''Creates gender/name database based on 2013 SSA data.

        This downloads data from the Social Security Administration which
        contains the most popular surnames, along with their associated
        genders.

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
                                       'gender.sqlite')
            ftp_for_prefab = ftplib.FTP('ftp.theonaunheim.com')
            ftp_for_prefab.login()
            # Custom function for graphical ftp
            PercentageFTP('gender.sqlite',
                          destination,
                          ftp_for_prefab).start()
            surgeo.adapter.adaprint('Copying data to local table ...')
            connection = sqlite3.connect(self.db_path)
            cursor = connection.cursor()
            cursor.execute('''DROP TABLE IF EXISTS gendername_joint''')
            cursor.execute('''CREATE TABLE IF NOT EXISTS gendername_joint(
                              id INTEGER PRIMARY KEY,
                              first_name TEXT,
                              female_prob REAL,
                              male_prob REAL)''')
            # Copy foreign db into local db
            cursor.execute('''ATTACH ? AS "downloaded_db" ''', (destination,))
            cursor.execute('''INSERT INTO gendername_joint
                              SELECT * FROM downloaded_db.gendername_joint''')
            cursor.execute('''CREATE INDEX IF NOT EXISTS first_name_index
                              ON gendername_joint(first_name)''')
            connection.commit()
            surgeo.adapter.adaprint('Successfully written ...')
            return
        # Fix naked except.
        except:
            surgeo.adapter.adaprint('Unable to find prefab database ...')
            surgeo.adapter.adaprint('Time-consuming rebuild starting ...')
######## Downloads
        surgeo.adapter.adaprint('Creating GenderModel database manually ...')
        # Remove downloaded files in event of a hangup.
        atexit.register(self.temp_cleanup)
        surgeo.adapter.adaprint('Downloading files ...')
        url = 'http://www.ssa.gov/oact/babynames/names.zip'
        title = 'names.zip'
        destination_path = os.path.join(self.temp_folder_path,
                                        title)
        PercentageHTTP(url,
                       destination_path,
                       title).start()
######## Unzip files
        FILE_LIST = ['yob1989.txt', 'yob1990.txt', 'yob1991.txt',
                     'yob1992.txt', 'yob1993.txt', 'yob1994.txt',
                     'yob1995.txt', 'yob1996.txt', 'yob1997.txt',
                     'yob1998.txt', 'yob1999.txt', 'yob2000.txt',
                     'yob2001.txt', 'yob2002.txt', 'yob2003.txt',
                     'yob2004.txt', 'yob2005.txt', 'yob2006.txt',
                     'yob2007.txt', 'yob2008.txt', 'yob2009.txt',
                     'yob2010.txt', 'yob2011.txt', 'yob2012.txt',
                     'yob2013.txt']
        # Set up counter to start tabulating names and counts.
        female_counter = collections.Counter()
        male_counter = collections.Counter()
        surgeo.adapter.adaprint('Unzipping files ...')
        with zipfile.ZipFile(destination_path) as zip_file:
            for item in FILE_LIST:
                data = zip_file.read(item)
                new_file_path = os.path.join(self.temp_folder_path,
                                             item)
                # TODO Roundabout way or getting file data.
                with open(new_file_path, 'wb+') as destination_file:
                    destination_file.write(data)
                with open(destination_file, 'r') as opened_file:
                    for line in opened_file:
                        split_line = line.split(',')
                        name = split_line[0].strip()
                        gender = split_line[1].strip()
                        count = split_line[2].strip()
                        # Add to counts
                        if gender == 'F':
                            female_counter.update({name: int(count)})
                        if gender == 'M':
                            male_counter.update({name: int(count)})
        # Create name set.
        name_set = set(itertools.chain(female_counter.keys(),
                                       male_counter.keys()))
        # Prep names for db entry
        list_of_entry_tuples = []
        for name in name_set:
            female_count = female_counter[name]
            male_count = male_counter[name]
            total = female_count + male_count
            female_percentage = float(female_count) / float(total)
            male_percentage = float(male_count) / float(total)
            list_of_entry_tuples.append(tuple(name,
                                              female_percentage,
                                              male_percentage))
######## Write to db
        surgeo.adapter.adaprint('Writing to database ...')
        try:
            connection = sqlite3.connect(self.db_path)
            cursor = connection.cursor()
            cursor.execute('''DROP TABLE IF EXISTS gendername_joint''')
            cursor.execute('''CREATE TABLE IF NOT EXISTS gendername_joint(
                              id INTEGER PRIMARY KEY,
                              first_name TEXT,
                              female_prob REAL,
                              male_prob REAL)''')
            for item_tuple in list_of_entry_tuples:
                cursor.execute('''INSERT INTO gendername_joint
                                  VALUES(NULL, ?, ?, ?)''',
                               item_tuple)
                surgeo.adapter.adaprint('Creating index ...')
                cursor.execute('''CREATE INDEX IF NOT EXISTS first_name_index
                                  ON gender_joint(first_name)''')
                connection.commit()
                connection.close()
        except sqlite3.Error as e:
            connection.rollback()
            connection.commit()
            raise e

    def get_result_object(self, first_name):
        '''Takes last name, returns race object.

        Parameters
        ----------
        first_name : string
            This is the name for which you are getting data.

        Returns
        -------
        result : surgeo.Result
            The return is not an error result, it is a custom object which
            contains attributes:
                *first_name : string
                *gender : string

        Raises
        ------
        sqlite3.Error
            Can occur for any number of database-related reasons. Upon error,
            automatic rollback occurs, but the error is raised because it's
            probably symptomatic of a bigger problem.

        '''
        # No removal of jr, sr, II, etc. Clean your data accordingly.
        title_first_name = first_name.title()
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        cursor.execute('''SELECT * FROM gender_joint
                          WHERE first_name=?''', (title_first_name,))
        row = cursor.fetchone()
######## Error result. Terminates with returning error result
        if row is None:
            error_result = Result(**{'first_name': 0,
                                     'gender': 0}).errorify()
            return error_result
        first_name = row[1]
        gender = row[2]
        argument_dict = {'first_name': first_name,
                         'gender': gender}
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
        cursor.execute('''DROP TABLE IF EXISTS gender_joint''')
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
        HEADER_LIST = ['name',
                       'first_name',
                       'first',
                       'gender',
                       'sex']
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
        subject_index = []
        # Create percent index
        for row_index, row_item in enumerate(line_list_1):
            for header_item in HEADER_LIST:
                if header_item in row_item:
                    gender_index = row_index
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

