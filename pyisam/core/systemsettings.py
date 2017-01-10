"""
@copyright: IBM
"""

import logging

from .system.firststeps import FirstSteps


logger = logging.getLogger(__name__)


class SystemSettings9020(object):

    def __init__(self, base_url, username, password):
        self.first_steps = FirstSteps(base_url, username, password)


class SystemSettings9021(SystemSettings9020):

    def __init__(self, base_url, username, password):
        super(SystemSettings9021, self).__init__(base_url, username, password)
