
import decimal
import os
import sqlite3
import sys
import time
import traceback


def reconstitute_data():
    '''Go through each row. Fill in estimates for redacted items.

    Args:
        None
    Returns:
        None
    Raises:
        None

    It is a simple function that transforms the database. For confidentiality
    purposes, the Census Bureau scrubs certain data on race. This function
    reconstitutes that data. We take the total number of scrubbed items, and
    then divide it equally between the scrubbed categories. This yields an
    approximation.

    '''

    db_path = os.path.join(os.path.expanduser('~'),
                           '.surgeo',
                           'census.db')
    redacted_db = sqlite3.connect(db_path)
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
