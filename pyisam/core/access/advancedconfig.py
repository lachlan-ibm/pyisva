"""
@copyright: IBM
"""

import logging

from pyisam.util.model import DataObject
from pyisam.util.restclient import RESTClient


OVERRIDE_CONFIGS = "/iam/access/v8/override-configs"

logger = logging.getLogger(__name__)


class AdvancedConfig(object):

    def __init__(self, base_url, username, password):
        super(AdvancedConfig, self).__init__()
        self.client = RESTClient(base_url, username, password)

    def list(self, sortBy=None, count=None, start=None, filter=None):
        parameters = DataObject()
        parameters.add_value_string("sortBy", sortBy)
        parameters.add_value_string("count", count)
        parameters.add_value_string("start", start)
        parameters.add_value_string("filter", filter)

        response = self.client.get_json(OVERRIDE_CONFIGS, parameters.data)
        response.success = response.status_code == 200

        return response

    def update(self, id, value=None, sensitive=None):
        data = DataObject()
        data.add_value_string("value", value)
        data.add_value("sensitive", sensitive)

        endpoint = "%s/%s" % (OVERRIDE_CONFIGS, id)

        response = self.client.put_json(endpoint, data.data)
        response.success = response.status_code == 204

        return response
