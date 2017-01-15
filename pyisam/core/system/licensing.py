"""
@copyright: IBM
"""

import logging

from pyisam.util.model import DataObject, Response
from pyisam.util.restclient import RESTClient


CAPABILITIES = "/isam/capabilities"

logger = logging.getLogger(__name__)


class Licensing(object):

    def __init__(self, base_url, username, password):
        super(Licensing, self).__init__()
        self.client = RESTClient(base_url, username, password)

    def activate_module(self, code):
        data = DataObject()
        data.add_value_string("code", code)

        endpoint = CAPABILITIES + "/v1"

        response = self.client.post_json(endpoint, data.data)
        response.success = response.status_code == 200

        return response

    def get_activated_module(self, id):
        endpoint = "%s/%s/v1" % (CAPABILITIES, id)

        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200

        return response

    def get_activated_modules(self):
        endpoint = CAPABILITIES + "/v1"

        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200

        return response

    def import_activation_code(self, file_path):
        response = Response()

        try:
            with open(file_path, 'rb') as code:
                data = DataObject()
                data.add_value_string("name", "activation")

                files = {"filename": code}

                endpoint = CAPABILITIES + "/v1"

                response = self.client.post_file(
                    endpoint, data=data.data, files=files)
                response.success = response.status_code == 200
        except IOError as e:
            logger.error(e)
            response.success = False

        return response
