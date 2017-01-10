"""
@copyright: IBM
"""

import inspect
import logging


DETAILED = "[%(asctime)-15s] %(name)-20.20s %(levelname).1s %(message)s"


class Logger(object):

    def __init__(self, class_name, level=logging.NOTSET):
        self._logger = logging.getLogger(class_name)
        self._logger.addHandler(logging.NullHandler())
        self._logger.setLevel(level)

    def get_level(self):
        return self._logger.getEffectiveLevel()

    def set_level(self, level):
        self._logger.setLevel(level)

    def enter(self, *args):
        if not args:
            self._logger.debug("ENTRY")
        elif len(args) == 1:
            self._logger.debug("ENTRY %s", *args)
        else:
            self._logger.debug("ENTRY %s", args)

    def exit(self, *args):
        if not args:
            self._logger.debug("RETURN")
        elif len(args) == 1:
            self._logger.debug("RETURN %s", *args)
        else:
            self._logger.debug("RETURN %s", args)

    def critical(self, message, *args):
        self._logger.critical(message, *args)

    def debug(self, message, *args):
        self._logger.debug(message, *args)

    def error(self, message, *args):
        self._logger.error(message, *args)

    def info(self, message, *args):
        self._logger.info(message, *args)

    def warning(self, message, *args):
        self._logger.warning(message, *args)
