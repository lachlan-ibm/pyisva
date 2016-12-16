"""
@copyright: IBM
"""

import logging

from com.ibm.isam.util.logger import Logger

from .manage import Manage, Manage9021
from .policy import Policy, Policy9021
from .settings import GlobalSettings


class AccessControl9020(GlobalSettings, Manage, Policy):

    logger = Logger("AccessControl9020")

    def __init__(self, base_url, username, password, log_level=logging.NOTSET):
        super(AccessControl9020, self).__init__(
            base_url, username, password, log_level)
        AccessControl9020.logger.set_level(log_level)


class AccessControl9021(GlobalSettings, Manage9021, Policy9021):

    logger = Logger("AccessControl9021")

    def __init__(self, base_url, username, password, log_level=logging.NOTSET):
        super(AccessControl9021, self).__init__(
            base_url, username, password, log_level)
        AccessControl9021.logger.set_level(log_level)
