""""
@copyright: IBM
"""

import logging

from pyisam.util.restclient import RestClient
import pyisam.util.common as Utils


ADVANCED_PARAMETERS = "/core/adv_params"

logger = logging.getLogger(__name__)


class AdvancedTuning(RestClient):

    def __init__(self, base_url, username, password):
        super(AdvancedTuning, self).__init__(base_url, username, password)

    def create_parameter(self, key=None, value=None, comment=None):
        #logger.enter()

        data = {}
        Utils.add_value_string(data, "key", key)
        Utils.add_value_string(data, "value", value)
        Utils.add_value_string(data, "comment", comment)
        Utils.add_value(data, "_isNew", True)

        status_code, content = self.http_post_json(ADVANCED_PARAMETERS, data)

        result = (status_code == 201, status_code, content)

        #logger.exit(result)
        return result

    def get_parameters(self):
        #logger.enter()

        status_code, content = self.http_get_json(ADVANCED_PARAMETERS)

        if status_code == 200:
            result = (True, status_code, content.get("tuningParameters", []))
        else:
            result = (False, status_code, content)

        #logger.exit(result)
        return result
