"""
@copyright: IBM
"""

import inspect
import logging


CALLER = 1
METHOD = 3
FORMAT = "[%(asctime)-15s] %(name)-20.20s %(level).1s %(method)s() %(message)s"

logging.basicConfig(format=FORMAT)


class Logger(object):

    def __init__(self, class_name, level=logging.NOTSET):
        self._logger = logging.getLogger(class_name)
        self._logger.setLevel(level)

    def get_level(self):
        return self._logger.getEffectiveLevel()

    def set_level(self, level):
        self._logger.setLevel(level)

    def enter(self, *args):
        extras = {"level": ">", "method": inspect.stack()[CALLER][METHOD]}
        if not args:
            self._logger.debug("ENTRY", extra=extras)
        elif len(args) == 1:
            self._logger.debug("ENTRY %s", *args, extra=extras)
        else:
            self._logger.debug("ENTRY %s", args, extra=extras)

    def exit(self, *args):
        extras = {"level": "<", "method": inspect.stack()[CALLER][METHOD]}
        if not args:
            self._logger.debug("RETURN", extra=extras)
        elif len(args) == 1:
            self._logger.debug("RETURN %s", *args, extra=extras)
        else:
            self._logger.debug("RETURN %s", args, extra=extras)

    def critical(self, message, *args):
        extras = {"level": "C", "method": inspect.stack()[CALLER][METHOD]}
        self._logger.critical(message, *args, extra=extras)

    def debug(self, message, *args):
        extras = {"level": "D", "method": inspect.stack()[CALLER][METHOD]}
        self._logger.debug(message, *args, extra=extras)

    def error(self, message, *args):
        extras = {"level": "E", "method": inspect.stack()[CALLER][METHOD]}
        self._logger.error(message, *args, extra=extras)

    def info(self, message, *args):
        extras = {"level": "I", "method": inspect.stack()[CALLER][METHOD]}
        self._logger.info(message, *args, extra=extras)

    def warning(self, message, *args):
        extras = {"level": "W", "method": inspect.stack()[CALLER][METHOD]}
        self._logger.warning(message, *args, extra=extras)
