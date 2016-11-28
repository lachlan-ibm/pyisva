"""
Created on Nov 23, 2016

@copyright: IBM
"""
from com.ibm.isam.util.Logger import Logger
from .SecureSettings import SecureSettings
import logging

class SecureSettings9020(SecureSettings):

    logger = Logger("SecureSettings9020")

    def __init__(self, baseUrl, username, password, logLevel=logging.NOTSET):
        super(SecureSettings9020, self).__init__(baseUrl, username, password, logLevel)
        SecureSettings9020.logger.setLevel(logLevel)

    def getIsamVersion(self):
        return "9020"
