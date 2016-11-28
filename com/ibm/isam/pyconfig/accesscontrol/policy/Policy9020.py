"""
Created on Nov 23, 2016

@copyright: IBM
"""
from com.ibm.isam.util.Logger import Logger
from .Policy import Policy
import logging

class Policy9020(Policy):

    logger = Logger("Policy9020")

    def __init__(self, baseUrl, username, password, logLevel=logging.NOTSET):
        super(Policy9020, self).__init__(baseUrl, username, password, logLevel)
        Policy9020.logger.setLevel(logLevel)

    def getIsamVersion(self):
        return "9020"
