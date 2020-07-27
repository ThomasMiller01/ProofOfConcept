from datetime import date
import sqlite3
import os
import pandas as pd


def run(filename):
    # create dir for file
    dir_path_tmp = filename.split('.')
    dir_path_tmp = '.'.join(dir_path_tmp[: -1])
    try:
        os.mkdir('./output/' + str(date.today()) + '/' + dir_path_tmp)
    except FileExistsError:
        pass

    input_file = './data/' + filename
    output_file = './output/' + \
        str(date.today()) + '/' + dir_path_tmp + '/' + filename

    # get new data
    db_connection = sqlite3.connect(input_file)
    db = db_connection.cursor()

    db.execute('SELECT name FROM sqlite_master WHERE type="table"')
    tables = db.fetchall()

    # filter for tables with real data
    tables = [x[0] for x in tables if x[0] not in ['sqlite_sequence']]

    for table in tables:
        results = pd.read_sql_query("SELECT * FROM " + table, db_connection)
        save(output_file, results, table)

    db_connection.close()


def save(output_file, results, table):
    error = True
    num = 0
    while error:
        file_path_tmp = output_file.split('.')
        file_path_tmp = '.'.join(file_path_tmp[: -1]) + '_' + table
        added = '' if num == 0 else ' (' + str(num) + ')'
        file_path_name = file_path_tmp + added + '.csv'
        if os.path.isfile(file_path_name):
            num += 1
        else:
            results.to_csv(file_path_name, index=False)
            print("Saved '" + table + "' to " + file_path_name)
            error = False


if __name__ == '__main__':
    try:
        os.mkdir('./output/' + str(date.today()))
    except FileExistsError:
        pass
    files = os.listdir('./data')
    for f in files:
        run(f)
    print('Saved all files')
