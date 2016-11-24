"""
Created on Nov 23, 2016

@copyright: IBM
"""
from com.ibm.isam.util.Logger import Logger
from .FirstSteps import FirstSteps
import logging

class FirstSteps9020(FirstSteps):

    logger = Logger("FirstSteps9020")

    def __init__(self, baseUrl, username, password, logLevel=logging.NOTSET):
        super(FirstSteps9020, self).__init__(baseUrl, username, password, logLevel)
        FirstSteps9020.logger.setLevel(logLevel)

    def getIsamVersion(self):
        return "9020"
