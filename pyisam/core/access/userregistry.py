"""
@copyright: IBM
"""

import logging

from pyisam.util.model import DataObject
from pyisam.util.restclient import RESTClient


USER_REGISTRY = "/mga/user_registry"

logger = logging.getLogger(__name__)


class UserRegistry(object):

    def __init__(self, base_url, username, password):
        super(UserRegistry, self).__init__()
        self.client = RESTClient(base_url, username, password)

    def update_user_password(self, username, password=None):
        data = DataObject()
        data.add_value_string("password", password)

        endpoint = "%s/users/%s/v1" % (USER_REGISTRY, username)

        response = self.client.put_json(endpoint, data.data)
        response.success = response.status_code == 204

        return response
