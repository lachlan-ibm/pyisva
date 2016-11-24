"""
Created on Nov 23, 2016

@copyright: IBM
"""
from com.ibm.isam.util.Logger import Logger
from .Manage import Manage
import logging

class Manage9020(Manage):

    logger = Logger("Manage9020")

    def __init__(self, baseUrl, username, password, logLevel=logging.NOTSET):
        super(Manage9020, self).__init__(baseUrl, username, password, logLevel)
        Manage9020.logger.setLevel(logLevel)

    def getIsamVersion(self):
        return "9020"
