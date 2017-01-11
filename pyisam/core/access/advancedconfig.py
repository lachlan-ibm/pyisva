"""
@copyright: IBM
"""

import logging

from pyisam.util.restclient import RestClient
import pyisam.util.common as Utils


OVERRIDE_CONFIGS = "/iam/access/v8/override-configs"

logger = logging.getLogger(__name__)


class AdvancedConfig(RestClient):

    def __init__(self, base_url, username, password):
        super(AdvancedConfig, self).__init__(base_url, username, password)

    def list(self, sortBy=None, count=None, start=None, filter=None):
        #logger.enter()

        parameters = {}
        Utils.add_value_string(parameters, "sortBy", sortBy)
        Utils.add_value_string(parameters, "count", count)
        Utils.add_value_string(parameters, "start", start)
        Utils.add_value_string(parameters, "filter", filter)

        status_code, content = self.http_get_json(
            OVERRIDE_CONFIGS, parameters=parameters)

        result = (status_code == 200, status_code, content)

        #logger.exit(result)
        return result

    def update(self, id, value=None, sensitive=None):
        #logger.enter()

        data = {}
        Utils.add_value_string(data, "value", value)
        Utils.add_value(data, "sensitive", sensitive)

        endpoint = "%s/%s" % (OVERRIDE_CONFIGS, id)
        status_code, content = self.http_put_json(endpoint, data=data)

        result = (status_code == 204, status_code, content)

        #logger.exit(result)
        return result
