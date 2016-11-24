"""
Created on Nov 23, 2016

@copyright: IBM
"""
from com.ibm.isam.util.Logger import Logger
from .Configuration import Configuration
import logging

class Configuration9020(Configuration):

    logger = Logger("Configuration9020")

    def __init__(self, baseUrl, username, password, logLevel=logging.NOTSET):
        super(Configuration9020, self).__init__(baseUrl, username, password, logLevel)
        Configuration9020.logger.setLevel(logLevel)

    def getIsamVersion(self):
        return "9020"
