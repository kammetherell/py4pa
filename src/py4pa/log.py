from datetime import datetime as datetime
import logging
import os
import sys

class Log_File:
    """Python class to enable logging of key events to a file of your choosing, 
    as well as the console if you wish

    Parameters
    ----------
    directory : str
        The file location where you want the log file saved, 
        excluding the file name

    fName : str (optional)
        The filename, including extension that you want to use as your output.
        If this isn't specified, the file will be called 'progress_log - YYYY-MM-DD HH:MM:SS.txt', 
        where the date & time stamp will be the time when the log is first initiated.
    
    log_level : str (optional)
        Defaults to 'INFO'. Valid options are NOTSET, DEBUG, INFO, WARN, ERROR, CRITICAL
    
    log_fmt : str (optional)
        See https://docs.python.org/3/library/logging.html#logging.LogRecord for definitions 
        of attributes. Defaults to '%(asctime)s: %(levelname)s %(message)s' e.g. 
        '2024-03-14 10:56:54,329: INFO test info message'

    print_to_console : bool (optional)
        Defaults to True. If set to true, will print messages to both the log file, 
        and the console. If False, will only output to the log file    
    """


    def __init__(self, 
                 directory, 
                 fName=None, 
                 log_level = 'INFO', 
                 log_fmt='%(asctime)s: %(levelname)s %(message)s',
                 print_to_console=False):

        self.run_date_time = datetime.now().strftime('%Y-%m-%d T%H-%M-%S')
        self.fName = f'progress_log-{self.run_date_time}.log'

        if fName is not None:
            self.fName = fName
        self.directory = directory
        self.fPath = r'{0}/{1}'.format(directory, self.fName)
        print(self.fPath)

        self.log_level = logging.getLevelName(log_level)
        self.log_fmt = log_fmt
        self.print_to_console = print_to_console

        if not os.path.exists(self.directory):
            os.makedirs(self.directory)
        
        # if not os.path.exists(self.fPath):
        #     with open(self.fPath, 'w'): pass

        self.__create_logger()

    def __create_logger(self):

        #Set Up Logger and level
        log = logging.getLogger()
        log.setLevel(self.log_level)

        #Set log message format
        format=logging.Formatter(self.log_fmt)

        #Set Up log file handler
        file_handler = logging.FileHandler(self.fPath)
        file_handler.setLevel(self.log_level)
        file_handler.setFormatter(format)
        log.addHandler(file_handler)

        #Set up Print to console if set in Class
        if self.print_to_console:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(self.log_level)
            console_handler.setFormatter(format)
            log.addHandler(console_handler)
            
        self.logger = log
    
    def debug(self, msg):
        self.logger.debug(msg)
    def info(self, msg):
        self.logger.info(msg)
    def warning(self, msg):
        self.logger.warning(msg)
    def error(self, msg):
        self.logger.error(msg)
    def critical(self, msg):
        self.logger.critical(msg)