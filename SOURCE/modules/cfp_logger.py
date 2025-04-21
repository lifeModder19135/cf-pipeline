import logging
from enum import Flag
from SOURCE.modules.cfp_errors import CfpTypeError, CfpValueError

class Level(Flag):
    """These values represent different logging levels."""

    DEBUG = 1
    INFO = 2
    WARNING = 3
    ERROR = 4
    CRITICAL = 5

class BasicLogger:
    """This is a basic logger. Creating an instance sets the defaults for the logger. After creating an instance, you can log messages with it's `log` method."""

    @property
    def min_level_printed(self) -> Level:
        return self.__level
    
    @min_level_printed.setter
    def min_level_printed(self, lvl: Level) -> None:
        """This is the minimum priority level printed to the console."""
        if type(lvl) == Level:
            self.__level = lvl
        else:
            raise CfpTypeError('The value assigned to min_level_printed must be of type Level')

    @property
    def filename(self) -> str:
        """This is the name of the file to which logs will be written."""
        return self.__filename
    
    @filename.setter
    def filename(self, fname: str) -> None:
        self.__filename = fname

    def log(self, msg: str, level: Level=Level.DEBUG):
        if level == Level.DEBUG:
            logging.debug(msg)
        elif level == Level.INFO:
            logging.info(msg)
        elif level == Level.WARNING:
            logging.warning(msg)
        elif level == Level.ERROR:
            logging.error(msg)
        elif level == Level.CRITICAL:
            logging.critical(msg)
        else:
            raise CfpValueError
    

    def __init__(self, level: Level, logfile: str):
        self.min_level_printed = level
        self.filename = logfile
        if self.min_level_printed == Level.DEBUG:
            logging.basicConfig(level=logging.DEBUG, filename=self.filename, filemode='a', force=True)
        elif self.min_level_printed == Level.INFO:
            logging.basicConfig(level=logging.INFO, filename=self.filename, filemode='a', force=True)
        elif self.min_level_printed == Level.WARNING:
            logging.basicConfig(level=logging.WARNING, filename=self.filename, filemode='a', force=True)
        elif self.min_level_printed == Level.ERROR:
            logging.basicConfig(level=logging.ERROR, filename=self.filename, filemode='a', force=True)
        elif self.min_level_printed == Level.CRITICAL:
            logging.basicConfig(level=logging.CRITICAL, filename=self.filename, filemode='a', force=True)

        