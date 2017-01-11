"""
@copyright: IBM
"""

import logging

from pyisam.util.restclient import RestClient
import pyisam.util.common as Utils


RUNTIME_TUNING = "/mga/runtime_tuning"

logger = logging.getLogger(__name__)


class RuntimeParameters(RestClient):

    def __init__(self, base_url, username, password):
        super(RuntimeParameters, self).__init__(base_url, username, password)

    def update(self, parameter, value=None):
        #logger.enter()

        data = {}
        Utils.add_value(data, "value", value)

        endpoint = "%s/%s/v1" % (RUNTIME_TUNING, parameter)
        status_code, content = self.http_put_json(endpoint, data=data)

        result = (status_code == 200, status_code, content)

        #logger.exit(result)
        return result
