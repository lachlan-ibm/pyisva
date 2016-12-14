"""
@copyright: IBM
"""

import logging

from com.ibm.isam.util.logger import Logger

from .manage import Manage


class WebSettings9020(Manage):

    logger = Logger("WebSettings9020")

    def __init__(self, base_url, username, password, log_level=logging.NOTSET):
        super(WebSettings9020, self).__init__(
            base_url, username, password, log_level)
        WebSettings9020.logger.set_level(log_level)


class WebSettings9021(Manage):

    logger = Logger("WebSettings9021")

    def __init__(self, base_url, username, password, log_level=logging.NOTSET):
        super(WebSettings9021, self).__init__(
            base_url, username, password, log_level)
        WebSettings9021.logger.set_level(log_level)
