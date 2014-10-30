from surgeo.models.geocode_model import GeocodeModel
from surgeo.models.surname_model import SurnameModel
from surgeo.models.model_base import BaseModel
from surgeo.utilities.result import Result
from surgeo.calculate.weighted_mean import get_weighted_mean


class SurgeoModel(BaseModel):
    '''Contains data and methods for Bayesian Improved Surname Geocoding model.

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
    geocode_model : GeocodeModel
        This is a Geocode model object to use.
    surname_model : SurnameModel
        Thie is a Surname model object to use.

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
        self._version = '2000.2010.1'
        self.geocode_model = GeocodeModel()
        self.surname_model = SurnameModel()

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
            Ifu database is deficient, returns False.

        Raises
        ------
        None

        '''
        if self.geocode_model.db_check() is False:
            return False
        if self.surname_model.db_check() is False:
            return False
        return True

    def db_create(self):
        '''Creates Surname and Geocode database tables.

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
        # Try geocode and create if necessary
        if self.geocode_model.db_check() is False:
            self.geocode_model.db_create()
        if self.surname_model.db_check() is False:
            self.surname_model.db_create()

    def get_result_object(self,
                          zcta,
                          surname,
                          zcta_weight=1.00,
                          surname_weight=1.00):
        '''Takes last name, returns race object.

        Parameters
        ----------
        zcta : string
            This is the zip code for which you are getting data.
        surname : string
            This is the name for which you are getting data.
        zcta_weight : float
            Weight given to zcta.
        surname_weight : float
            Weight given to surname.

        Returns
        -------
        result : surgeo.Result
            The return is not an error result, it is a custom object which
            contains attributes:
                *surname : string
                *zip : string
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

        Where k is census block
        Where j is surname
        Where i is race (1 = Hispanic,
                         2 = White,
                         3 = Black,
                         4 = Asian or Pacific Islander,
                         5 = American Indian / Alaska Native,
                         6 = Multiracial)

        Where u(i,j,k) = p(i|j) * r(k|i):

                                          u(i,j,k)
        q(i|j,k) = ------------------------------------------------------------
                u(1,j,k) + u(2,j,k) + u(3,j,k) + u(4,j,k) + u(5,j,k) + u(6,j,k)

        See BACKGROUND.txt file for detail.

        For each (zcta, surname) pair, we must first get the probability for a
        specific race is based on surname. We must then get get the probability
        for a specific race based on location. We then take prob_surname for
        that race and multiply it by prob_location. We multiply these together
        to get a unified surname/geocode probability. We divide this
        probability by the probability of all the races together to give us our
        final probability.

        '''
        geocode_result = self.geocode_model.get_result_object(zcta)
        surname_result = self.surname_model.get_result_object(surname)
        # Filter out erroneous results
        if any([geocode_result._error_result,
                surname_result._error_result]) is True:
            error_result = Result(**{'zcta': 0,
                                     'surname': 0,
                                     'hispanic': 0,
                                     'white': 0,
                                     'black': 0,
                                     'api': 0,
                                     'ai': 0,
                                     'multi': 0}).errorify()
            return error_result
        # Hispanic joint u(1,j,k)
        hispanic_prob = (float(surname_result.hispanic) *
                         surname_weight *
                         float(geocode_result.hispanic) *
                         zcta_weight)
        # White joint u(2,j,k)
        white_prob = (float(surname_result.white) *
                      surname_weight *
                      float(geocode_result.white) *
                      zcta_weight)
        # Black joint u(3,j,k)
        black_prob = (float(surname_result.black) *
                      surname_weight *
                      float(geocode_result.black) *
                      zcta_weight)
        # API joint u(4,j,k)
        api_prob = (float(surname_result.api) *
                    surname_weight *
                    float(geocode_result.api) *
                    zcta_weight)
        # AI_AN joint u(5,j,k)
        ai_prob = (float(surname_result.ai) *
                   surname_weight *
                   float(geocode_result.ai) *
                   zcta_weight)
        # Multi joint u(6,j,k)
        multi_prob = (float(surname_result.multi) *
                      surname_weight *
                      float(geocode_result.multi) *
                      zcta_weight)
        # Denom=u(1,j,k) + u(2,j,k) + u(3,j,k) + u(4,j,k) + u(5,j,k) + u(6,j,k)
        denominator = (hispanic_prob +
                       white_prob +
                       black_prob +
                       api_prob +
                       ai_prob +
                       multi_prob)
        argument_dict = {'surname': surname,
                         'zcta': zcta,
                         'hispanic': round(hispanic_prob / denominator, 5),
                         'white': round(white_prob / denominator, 5),
                         'black': round(black_prob / denominator, 5),
                         'api': round(api_prob / denominator, 5),
                         'ai': round(ai_prob / denominator, 5),
                         'multi': round(multi_prob / denominator, 5)}
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
        None

        '''
        self.geocode_model.db_destroy()
        self.surname_model.db_destroy()

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
                    file_path_in,
                    file_path_out):
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
        SURNAME_HEADERS = ['name', 'surname', 'last_name', 'last name']
        ZCTA_HEADERS = ['zcta', 'zip', 'zip_code', 'zip_code']
        # TODO: Make so all subclassed or all imported as functions.
        surname_index = None
        zcta_index = None
        for index, line in enumerate(open(file_path_in, 'r')):
            if index > 0:
                break
            first_line = line.split(',')
        # Separate
        line_list = [item.replace('\"', '').replace('\'', '').strip()
                     for item in first_line]
        for index, item in enumerate(line_list):
            if item.lower() in SURNAME_HEADERS:
                surname_index = index
            if item.lower() in ZCTA_HEADERS:
                zcta_index = index
        super().csv_process(file_path_in,
                            file_path_out,
                            (line_list[zcta_index], line_list[surname_index]),
                            ('zcta', 'surname'),
                            continue_on_model_fail=True)

