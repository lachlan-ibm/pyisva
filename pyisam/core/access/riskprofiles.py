"""
@copyright: IBM
"""

import logging

from pyisam.util.restclient import RestClient
import pyisam.util.common as Utils


RISK_PROFILES = "/iam/access/v8/risk/profiles"

logger = logging.getLogger(__name__)


class RiskProfiles(RestClient):

    def __init__(self, base_url, username, password):
        super(RiskProfiles, self).__init__(base_url, username, password)

    def create(self, description=None, name=None, active=None, attributes=None):
        #logger.enter()

        data = {}
        Utils.add_value_string(data, "description", description)
        Utils.add_value_string(data, "name", name)
        Utils.add_value(data, "active", active)
        Utils.add_value(data, "attributes", attributes)
        Utils.add_value(data, "predefined", False)

        status_code, content = self.http_post_json(RISK_PROFILES, data=data)

        result = (status_code == 201, status_code, content)

        #logger.exit(result)
        return result
