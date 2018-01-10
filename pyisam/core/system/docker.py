"""
@copyright: IBM
"""

import logging

from pyisam.util.model import DataObject, Response
from pyisam.util.restclient import RESTClient


DOCKER = "/docker"

logger = logging.getLogger(__name__)


class Docker(object):

    def __init__(self, base_url, username, password):
        super(Docker, self).__init__()
        self.client = RESTClient(base_url, username, password)


    def publish(self, db_type=None, port=None, host=None, secure=True, user=None,passwd=None, db_name=None):

        endpoint = DOCKER + "/publish"

        response = self.client.put_json(endpoint)
        response.success = response.status_code == 201

        return response
