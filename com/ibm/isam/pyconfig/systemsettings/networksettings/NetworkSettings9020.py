"""
Created on Nov 23, 2016

@copyright: IBM
"""
from com.ibm.isam.util.Logger import Logger
from .NetworkSettings import NetworkSettings
import logging

class NetworkSettings9020(NetworkSettings):

    logger = Logger("NetworkSettings9020")

    def __init__(self, baseUrl, username, password, logLevel=logging.NOTSET):
        super(NetworkSettings9020, self).__init__(baseUrl, username, password, logLevel)
        NetworkSettings9020.logger.setLevel(logLevel)

    def getIsamVersion(self):
        return "9020"
