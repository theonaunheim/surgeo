import sqlite3

connection = sqlite3.connect('/path')
cursor = connection.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS
                  merge_data(
                  INTEGER PRIMARY KEY, zip TEXT,
                  num_white REAL, num_black REAL, num_ai REAL,
                  num_api REAL, num_hispanic REAL, num_multi REAL)''')
zip_logical_record_tuples = []
for row in cursor.execute('''SELECT logical_record, zcta FROM geocode_data'''):
    logical_record = row[0]
    zcta = row[1]
    zip_log_tuple = (logical_record, zcta)
    zip_logical_record_tuples.append(zip_log_tuple)

for tuple_ in zip_logical_record_tuples:
    logical_record = tuple_[0]
    zcta = tuple_[1]
    try:
        int(zcta)
    except ValueError:
        continue
    cursor.execute('''SELECT num_white, num_black, num_ai, num_api, num_hispanic,
                      num_multi FROM logical_race_data WHERE
                      logical_record=?''',
                      (logical_record,))
    result = cursor.fetchone()
    white = result[0]
    black = result[1]
    ai = result[2]
    api = result[3]
    hispanic = result[4]
    multi = result[5]
    cursor.execute('''INSERT INTO merge_data VALUES(NULL, ?, ?, ?, ?, ?, ?, ?)''',
                   (zcta, white, black, ai, api, hispanic, multi))
connection.commit()
connection.close()
