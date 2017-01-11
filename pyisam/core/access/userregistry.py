"""
@copyright: IBM
"""

import logging

from pyisam.util.restclient import RestClient
import pyisam.util.common as Utils


USER_REGISTRY = "/mga/user_registry"

logger = logging.getLogger(__name__)


class UserRegistry(RestClient):

    def __init__(self, base_url, username, password):
        super(UserRegistry, self).__init__(base_url, username, password)

    def update_user_password(self, username, password=None):
        #logger.enter()

        data = {}
        Utils.add_value_string(data, "password", password)

        endpoint = "%s/users/%s/v1" % (USER_REGISTRY, username)
        status_code, content = self.http_put_json(endpoint, data)

        result = (status_code == 204, status_code, content)

        #logger.exit(result)
        return result
