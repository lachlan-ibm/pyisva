"""
@copyright: IBM
"""

import logging

from pyisam.util.model import DataObject
from pyisam.util.restclient import RESTClient


RISK_PROFILES = "/iam/access/v8/risk/profiles"

logger = logging.getLogger(__name__)


class RiskProfiles(object):

    def __init__(self, base_url, username, password):
        super(RiskProfiles, self).__init__()
        self.client = RESTClient(base_url, username, password)

    def create(self, description=None, name=None, active=None, attributes=None):
        data = DataObject()
        data.add_value_string("description", description)
        data.add_value_string("name", name)
        data.add_value("active", active)
        data.add_value("attributes", attributes)
        data.add_value("predefined", False)

        response = self.client.post_json(RISK_PROFILES, data.data)
        response.success = response.status_code == 201

        return response
