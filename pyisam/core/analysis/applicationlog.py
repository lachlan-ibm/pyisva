""""
@copyright: IBM
"""

import logging

from pyisam.util.model import DataObject
from pyisam.util.restclient import RESTClient


logger = logging.getLogger(__name__)


class ApplicationLog(object):

    def __init__(self, base_url, username, password):
        super(ApplicationLog, self).__init__()
        self.client = RESTClient(base_url, username, password)
