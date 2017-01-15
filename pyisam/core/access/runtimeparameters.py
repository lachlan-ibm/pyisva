"""
@copyright: IBM
"""

import logging

from pyisam.util.model import DataObject
from pyisam.util.restclient import RESTClient


RUNTIME_TUNING = "/mga/runtime_tuning"

logger = logging.getLogger(__name__)


class RuntimeParameters(object):

    def __init__(self, base_url, username, password):
        super(RuntimeParameters, self).__init__()
        self.client = RESTClient(base_url, username, password)

    def update(self, parameter, value=None):
        data = DataObject()
        data.add_value("value", value)

        endpoint = "%s/%s/v1" % (RUNTIME_TUNING, parameter)

        response = self.client.put_json(endpoint, data.data)
        response.success = response.status_code == 200

        return response
