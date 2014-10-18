import csv
import math
import itertools
import io


def get_weighted_mean(percentage_index_numbers,
                      analyzed_subject_index_numbers,
                      filepath_in,
                      filepath_out=''):
    '''Gives the weighted mean of a particular data set.

        Args:
            filepath_in: file path of csv from which data is read
            filepath_out: file path of csv where data is written.
                          If blank, return value.
            percentage_index_numbers: tuple of index numbers of %s to use.
            analyzed_subject_index_numbers: tuple of index numbers to analyze
        Returns:
            None, or string depending on filepath_out.
        Raises:
            None

    '''

    with open(filepath_in, 'rU') as input_csv:
        # First pass, get all data and count up
        csv_reader = csv.reader(input_csv)
        row_1 = next(csv_reader)
        # Create number/header index

        name_column_index = {index: header for index, header in
                             enumerate(row_1)}
        summed_percentages = {item: float(0) for item in
                              percentage_index_numbers}
        #TODO better RAM usage
        validated_data_rows = []
######### First filter out bad or incomplete rows
        for index, row in enumerate(csv_reader, start=1):
            try:
                chained_index = itertools.chain(percentage_index_numbers,
                                                analyzed_subject_index_numbers)
                for positional_number in chained_index:
                    row_item = row[positional_number]
                    float(row_item)
                validated_data_rows.append(row)
            except ValueError:
                continue
######### Sum totals
    for row in validated_data_rows:
        for dictionary_key in summed_percentages.keys():
            row_value = row[dictionary_key]
            summed_percentages[dictionary_key] += float(row_value)
######### Calculate weighted mean for each analyzed subject matter
    summary_text = io.StringIO('')
    for subject_index_number in analyzed_subject_index_numbers:
        # Setup numbers
        weighted_mean = {item: float(0) for item in
                         percentage_index_numbers}
        weighted_stdev = {item: float(0) for item in
                          percentage_index_numbers}
        list_of_subject_values = []
        # Accumulate weighted mean
        for row in validated_data_rows:
            for key in weighted_mean.keys():
                # row[key] is percentage
                # summed_percentages[key] is aggregate percentage
                # row[subject_index_number] is subject (e.g. balance, APR)
                weighted_mean[key] += (float(row[key]) /
                                       float(summed_percentages[key]) *
                                       float(row[subject_index_number]))
            list_of_subject_values.append(float(row[subject_index_number]))
        # Accumulate weighted stdev
        for row in validated_data_rows:
            for key in weighted_stdev.keys():
                # row[key] is percentage
                # summed_percentages[key] is aggregate percentage
                # row[subject_index_number] is subject (e.g. balance, APR)
                # Subtract the entry minus weighted mean
                distance = abs(float(row[subject_index_number]) -
                               weighted_mean[key])
                weighted_stdev[key] += (float(row[key]) /
                                        float(summed_percentages[key]) * 
                                        distance)
        sample_mean = sum(list_of_subject_values) / len(list_of_subject_values)
        distance_from_mean = [math.pow((value - sample_mean), 2) for value in
                              list_of_subject_values]
        variance = sum(distance_from_mean) / len(list_of_subject_values)
        sample_std_dev = math.sqrt(variance)
        summary_text.write(''.join(['\n##########\n',
                                    name_column_index[subject_index_number],
                                    '\n##########\n',
                                    'sample mean: ',
                                    str(sample_mean),
                                    '\n',
                                    'sample standard deviation: ',
                                    str(sample_std_dev),
                                    '\n\n']))
        for key in weighted_mean.keys():
            summary_text.write(str(name_column_index[key]))
            summary_text.write(' weighted mean: ')
            summary_text.write(str(weighted_mean[key]))
            summary_text.write(str('\n'))
            summary_text.write(str(name_column_index[key]))
            summary_text.write(' weighted sdev: ')
            summary_text.write(str(weighted_stdev[key]))
            summary_text.write('\n')
    text_output = summary_text.getvalue()
    summary_text.close()
    if filepath_out == '':
        return text_output
    else:
        with open(filepath_out, 'w+') as f:
            f.write(text_output)

