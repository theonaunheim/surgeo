import csv
import os
import statistics

import surgeo

def get_weighted_mean(filepath_in, 
                      filepath_out,
                      percentage_index_numbers,
                      analyzed_subject_index_numbers):
    '''Gives the weighted mean of a particular data set.
        
        Args:
            filepath_in: file path of csv from which data is read
            filepath_out: file path of csv where data is written
            percentage_index_numbers: index numbers of %s to analyze.
            analyzed_subject_index_numbers: index numbers to analyze
        Returns:
            None
        Raises:
            None
            
    '''

    with open(filepath_in, 'rU') as input_csv:
        # First pass, get all data and count up
        csv_reader = csv.reader(input_csv)
        row_1 = next(csv_reader)
        # Create number/header index
        
        name_column_index = {item: row_1[item] for item in
                             percentage_index_numbers}
        summed_percentages = {item: float(0) for item in
                              percentage_index_numbers}
        data_rows = []
        # Already did first row. Starting at 1 instead of 0
        for index, entry in enumerate(csv_reader, start=1):
            try:
                float(subject)
            except ValueError:
                continue
            try:
                cursor = db.cursor()
                # Check exist
                cursor.execute('''SELECT state, logical_record FROM
                                  geocode_data WHERE zcta=?''', (zcta,))
                state, logical_record = cursor.fetchone()
                cursor.execute('''SELECT name, rank FROM
                                  surname_data WHERE name=?''', 
                                  (surname.upper(),))
                name, rank = cursor.fetchone()
                # Zip code is in database, so run it.
                result = surgeo.model.model1.run_model(zcta,
                                                       surname.upper(),
                                                       db)
                data_rows.append([float(result.hispanic),
                                  float(result.white),
                                  float(result.black),
                                  float(result.asian_or_pi),
                                  float(result.american_indian),
                                  float(result.multiracial),
                                  float(subject)])
                aggregate_percent_hispanic += float(result.hispanic)
                aggregate_percent_white += float(result.white)
                aggregate_percent_black += float(result.black)
                aggregate_percent_api += float(result.asian_or_pi)
                aggregate_percent_ai += float(result.american_indian)
                aggregate_percent_multi += float(result.multiracial)
            # Not in database. Do not add to analysis
            except TypeError:
                continue
    # Weighted average composite
    with open(filepath_out, 'w+') as input_csv:
        composite_percent_hispanic = 0
        composite_percent_white = 0
        composite_percent_black = 0
        composite_percent_api = 0
        composite_percent_ai = 0
        composite_percent_multi = 0
        subject_list = []
        for row in data_rows:
            hispanic_percent = row[0]
            white_percent = row[1]
            black_percent = row[2]
            api_percent = row[3]
            ai_percent = row[4]
            multi_percent = row[5]
            subject = row[6]
            subject_list.append(subject)
            # Weighted arithmetic mean
            composite_percent_hispanic += (hispanic_percent / 
                                           aggregate_percent_hispanic * 
                                           subject)
            composite_percent_white += (white_percent / 
                                        aggregate_percent_white * 
                                        subject)
            composite_percent_black += (black_percent / 
                                        aggregate_percent_black * 
                                        subject)                                           
            composite_percent_api += (api_percent / 
                                      aggregate_percent_api * 
                                      subject)
            composite_percent_ai += (ai_percent /
                                     aggregate_percent_ai *
                                     subject)                                           
            composite_percent_multi += (multi_percent / 
                                        aggregate_percent_multi * 
                                        subject) 
        sample_mean = statistics.mean(subject_list)
        sample_standard_deviation = statistics.stdev(subject_list)
    #                                     
    with open(filepath_out, 'w+') as f:
        f.write(''.join(["Sample mean: ",
                         str(sample_mean),
                         "\n",
                         "Sample standard deviation: ",
                         str(sample_standard_deviation),
                         "\n",
                         "\n",
                         "Average Hispanic: ",
                         str(composite_percent_hispanic),
                         "\n",
                         "Average White: ",
                         str(composite_percent_white),
                         "\n",
                         "Average Black: ",
                         str(composite_percent_black),
                         "\n",
                         "Average API: ",
                         str(composite_percent_api),
                         "\n",
                         "Average AI: ",
                         str(composite_percent_ai),
                         "\n",
                         "Average Multi: ",
                         str(composite_percent_multi),
                         "\n"]))
        
        
        


