"""
Created on Nov 23, 2016

@copyright: IBM
"""
from com.ibm.isam.util.Logger import Logger
from .SystemSettings import SystemSettings
import logging

class SystemSettings9020(SystemSettings):

    logger = Logger("SystemSettings9020")

    def __init__(self, baseUrl, username, password, logLevel=logging.NOTSET):
        super(SystemSettings9020, self).__init__(baseUrl, username, password, logLevel)
        SystemSettings9020.logger.setLevel(logLevel)

    def getIsamVersion(self):
        return "9020"
