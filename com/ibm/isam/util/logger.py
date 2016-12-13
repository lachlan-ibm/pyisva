"""
@copyright: IBM
"""

import logging

logging.basicConfig()

class Logger(object):

    def __init__(self, class_name, level=logging.NOTSET):
        self._logger = logging.getLogger(class_name)
        self._logger.setLevel(level)

    def get_level(self):
        return self._logger.getEffectiveLevel()

    def set_level(self, level):
        self._logger.setLevel(level)

    def enter_method(self, method_name, args=None):
        if args is None:
            self._logger.debug("%s >" % method_name)
        else:
            self._logger.debug("%s > %s" % (method_name, args))

    def exit_method(self, method_name, args=None):
        if args is None:
            self._logger.debug("%s <" % method_name)
        else:
            self._logger.debug("%s < %s" % (method_name, args))

    def error(self, method_name, message):
        self._logger.error("%s %s" % (method_name, message))

    def log(self, method_name, message):
        self._logger.info("%s %s" % (method_name, message))

    def trace(self, method_name, message):
        self._logger.debug("%s %s" % (method_name, message))

    def warn(self, method_name, message):
        self._logger.warning("%s %s" % (method_name, message))
