"""
Created on Nov 23, 2016

@copyright: IBM
"""

import logging

logging.basicConfig()

class Logger(object):

    def __init__(self, className, level=logging.NOTSET):
        self.__logger = logging.getLogger(className)
        self.__logger.setLevel(level)

    def getLevel(self):
        return self.__logger.getEffectiveLevel()

    def setLevel(self, level):
        self.__logger.setLevel(level)

    def enterMethod(self, methodName, args=None):
        if args is None:
            self.__logger.debug("%s >" % methodName)
        else:
            self.__logger.debug("%s > %s" % (methodName, args))

    def exitMethod(self, methodName, args=None):
        if args is None:
            self.__logger.debug("%s <" % methodName)
        else:
            self.__logger.debug("%s < %s" % (methodName, args))

    def error(self, methodName, message):
        self.__logger.error("%s %s" % (methodName, message))

    def log(self, methodName, message):
        self.__logger.info("%s %s" % (methodName, message))

    def trace(self, methodName, message):
        self.__logger.debug("%s %s" % (methodName, message))

    def warn(self, methodName, message):
        self.__logger.warning("%s %s" % (methodName, message))
