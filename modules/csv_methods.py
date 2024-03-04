'''This file contains all common .csv methods that will be used all throughout the Longin Searcher.'''
import csv

DELIMITER = ','
QUOTECHAR = '\\'

def read_csv(path):
    '''Returns all rows in the file a tuple of tuples.
    - path: Path of the desired file'''
    alldata = []
    with open(path, newline='') as file:
        csvreader = csv.reader(file, delimiter=DELIMITER, quotechar=QUOTECHAR)
        for row in csvreader:
            alldata.append(tuple(row))
    return tuple(alldata)

def write_csv(path, data, many_rows=True, mode='w'):
    '''Write data to a .csv file.
    - path: Path of the desired file
    - data: Data to be written. A row must be an iterable of columns
    - many_rows: If 'False', data is single row.
        If 'True', data is an iterable of many rows.
    - mode: Mode to use opening the file.
        'w' for overwriting writes, 'a' for appending writes
    '''
    with open(path, 'w', newline='') as csvfile:
        csvreader = csv.writer(csvfile, delimiter=DELIMITER, quotechar=QUOTECHAR, quoting=csv.QUOTE_MINIMAL)
        
        if many_rows:
            csvreader.writerows(data)
        else:
            csvreader.writerow(data)
pass