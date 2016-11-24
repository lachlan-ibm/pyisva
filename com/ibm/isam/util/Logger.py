"""
Created on Nov 23, 2016

@copyright: IBM
"""
import logging

logging.basicConfig()

class Logger(object):

    def __init__(self, className, level=logging.NOTSET):
        self.logger = logging.getLogger(className)
        self.logger.setLevel(level)

    def getLevel(self):
        return self.logger.getEffectiveLevel()

    def setLevel(self, level):
        self.logger.setLevel(level)

    def enterMethod(self, methodName, args=None):
        if args is None:
            self.logger.debug("%s >" % methodName)
        else:
            self.logger.debug("%s > %s" % (methodName, args))

    def exitMethod(self, methodName, args=None):
        if args is None:
            self.logger.debug("%s <" % methodName)
        else:
            self.logger.debug("%s < %s" % (methodName, args))

    def error(self, methodName, message):
        self.logger.error("%s %s" % (methodName, message))

    def log(self, methodName, message):
        self.logger.info("%s %s" % (methodName, message))

    def trace(self, methodName, message):
        self.logger.debug("%s %s" % (methodName, message))

    def warn(self, methodName, message):
        self.logger.warning("%s %s" % (methodName, message))
