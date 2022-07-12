import logging
import logging.handlers
import datetime
import os


class Logger:
    def __init__(self, handler: str = None, debug_level: str = None):
        td = datetime.datetime.now().today()
        project_name = os.getenv('PROJECT_NAME', 'Project')
        config = {
            'filename': f'log/{project_name}-{td.year}-{td.month}-{td.day}.log',
            'encoding': 'UTF-8'
        }

        if handler == 'syslog':
            del config
            self.__handler = logging.handlers.SysLogHandler()
        elif handler == 'rotate':
            self.__handler = logging.handlers.RotatingFileHandler(**config)
        else:
            self.__handler = logging.FileHandler(**config)

        if not debug_level:
            debug_level = os.getenv('DEBUG_LEVEL', 'NOTSET')

        self.__debug_level = debug_level
        self.__handler.setFormatter(logging.Formatter('%(asctime)s: %(levelname)s - %(message)s'))
        self.__logger = logging.getLogger(project_name)
        self.__logger.addHandler(self.__handler)
        self.__logger.setLevel(self.__debug_level)

    def getDebugLevel(self):
        return self.__debug_level

    def info(self, message, *args, **kwargs):
        self.__logger.info(message, *args, **kwargs)

    def warning(self, message, *args, **kwargs):
        self.__logger.warning(message, *args, **kwargs)

    def critical(self, message, *args, **kwargs):
        self.__logger.critical(message, *args, **kwargs)

    def debug(self, message, *args, **kwargs):
        self.__logger.debug(message, *args, **kwargs)

    def error(self, message, *args, **kwargs):
        self.__logger.error(message, *args, **kwargs)
