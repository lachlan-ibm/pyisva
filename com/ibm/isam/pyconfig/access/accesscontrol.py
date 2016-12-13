"""
@copyright: IBM
"""

import logging

from com.ibm.isam.util.logger import Logger

from .manage import Manage9020
from .policy import Policy9020
from .settings import GlobalSettings9020


class AccessControl9020(GlobalSettings9020, Manage9020, Policy9020):

    logger = Logger("AccessControl9020")

    def __init__(self, base_url, username, password, log_level=logging.NOTSET):
        super(AccessControl9020, self).__init__(
            base_url, username, password, log_level)
        AccessControl9020.logger.set_level(log_level)
