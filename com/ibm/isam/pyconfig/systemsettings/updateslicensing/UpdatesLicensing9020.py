"""
Created on Nov 23, 2016

@copyright: IBM
"""
from com.ibm.isam.util.Logger import Logger
from .UpdatesLicensing import UpdatesLicensing
import logging

class UpdatesLicensing9020(UpdatesLicensing):

    logger = Logger("UpdatesLicensing9020")

    def __init__(self, baseUrl, username, password, logLevel=logging.NOTSET):
        super(UpdatesLicensing9020, self).__init__(baseUrl, username, password, logLevel)
        UpdatesLicensing9020.logger.setLevel(logLevel)

    def getIsamVersion(self):
        return "9020"
