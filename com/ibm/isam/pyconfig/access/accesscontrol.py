"""
Created on Dec 02, 2016

@copyright: IBM
"""

import logging

from com.ibm.isam.util.logger import Logger

from .manage import Manage9020
from .policy import Policy9020
from .settings import GlobalSettings9020


class AccessControl9020(GlobalSettings9020, Manage9020, Policy9020):

    logger = Logger("AccessControl9020")

    def __init__(self, baseUrl, username, password, logLevel=logging.NOTSET):
        super(AccessControl9020, self).__init__(baseUrl, username, password, logLevel)
        AccessControl9020.logger.setLevel(logLevel)
