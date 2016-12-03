"""
Created on Dec 02, 2016

@copyright: IBM
"""

import logging

from com.ibm.isam.util.logger import Logger

from .manage import Manage9020


class WebSettings9020(Manage9020):

    logger = Logger("WebSettings9020")

    def __init__(self, baseUrl, username, password, logLevel=logging.NOTSET):
        super(WebSettings9020, self).__init__(baseUrl, username, password, logLevel)
        WebSettings9020.logger.setLevel(logLevel)
