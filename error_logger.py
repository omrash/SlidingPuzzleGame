'''
Omar Rashwan
CS 5001, Fall 2021
Project - Error Logger
'''

from time import ctime

ERROR_LOG = '5001_puzzle.err'
# the filename of the error log

ERROR_CODES = {1: 'Puz file malformed or does not exist',
               2: 'Could not open leaderboard.txt'}
# a dictionary of error codes

def read_log():
    '''
    Tries to read the log file, ignores an OSError if it is thrown since the
    log file does not exist. Appends any entries in the log file to a list
    that is returned.
    '''
    log = []
    try:
        with open(ERROR_LOG, mode='r') as log_file:
            for entry in log_file:
                log.append(entry.strip())
    except OSError:
        pass
    return log

def write_log(log):
    # Writes a list of error log entries (strings) to a log file.
    
    with open(ERROR_LOG, mode='w') as log_file:
        for entry in log:
            log_file.write(entry + '\n')

def error_handler(code, location):
    '''
    Takes in the error code and location where the error was encountered, then
    formats them into an entry with the time the error occured included. The
    new entry is then appended to the log and passed into the write function.
    '''
    log = read_log()
    entry = f'{ctime()}:Error: {ERROR_CODES[code]} LOCATION: {location}'
    log.append(entry)
    write_log(log)
