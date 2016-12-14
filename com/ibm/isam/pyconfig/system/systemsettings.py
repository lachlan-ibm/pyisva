"""
@copyright: IBM
"""

import logging

from com.ibm.isam.util.logger import Logger

from .configuration import Configuration
from .network import NetworkSettings
from .secure import SecureSettings
from .system import SystemSettings as SysSettings
from .updates import UpdatesLicensing


class SystemSettings9020(
        Configuration, NetworkSettings, SecureSettings, SysSettings,
        UpdatesLicensing):

    logger = Logger("SystemSettings9020")

    def __init__(self, base_url, username, password, log_level=logging.NOTSET):
        super(SystemSettings9020, self).__init__(
            base_url, username, password, log_level)
        SystemSettings9020.logger.set_level(log_level)


class SystemSettings9021(
        Configuration, NetworkSettings, SecureSettings, SysSettings,
        UpdatesLicensing):

    logger = Logger("SystemSettings9021")

    def __init__(self, base_url, username, password, log_level=logging.NOTSET):
        super(SystemSettings9021, self).__init__(
            base_url, username, password, log_level)
        SystemSettings9021.logger.set_level(log_level)
