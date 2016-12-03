"""
Created on Dec 02, 2016

@copyright: IBM
"""

import logging

from com.ibm.isam.util.logger import Logger

from .configuration import Configuration9020
from .network import NetworkSettings9020
from .secure import SecureSettings9020
from .system import SystemSettings9020 as SysSettings9020
from .updates import UpdatesLicensing9020


class SystemSettings9020(Configuration9020, NetworkSettings9020, SecureSettings9020, SysSettings9020,
                         UpdatesLicensing9020):

    logger = Logger("SystemSettings9020")

    def __init__(self, baseUrl, username, password, logLevel=logging.NOTSET):
        super(SystemSettings9020, self).__init__(baseUrl, username, password, logLevel)
        SystemSettings9020.logger.setLevel(logLevel)
