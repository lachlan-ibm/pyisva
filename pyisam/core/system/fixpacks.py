"""
@copyright: IBM
"""

import logging

from pyisam.util.model import DataObject, Response
from pyisam.util.restclient import RESTClient


FIXPACKS = "/fixpacks"

logger = logging.getLogger(__name__)


class Fixpacks(object):

    def __init__(self, base_url, username, password):
        super(Fixpacks, self).__init__()
        self.client = RESTClient(base_url, username, password)

    def install_fixpack(self, file_path):
        response = Response()

        try:
            with open(file_path, 'rb') as fixpack:
                data = DataObject()
                data.add_value_string("type", "application/octect-stream")

                files = {"file": fixpack}

                endpoint = FIXPACKS

                response = self.client.post_file(
                    endpoint, data=data.data, files=files)
                response.success = response.status_code == 200
        except IOError as e:
            logger.error(e)
            response.success = False

        return response

    def list_fixpacks(self):
        endpoint = FIXPACKS

        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200

        return response

    def get_fips_mode(self):
        endpoint = FIXPACKS + "/fipsmode"

        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200

        return response

    def rollback_fixpack(self):
        endpoint = FIXPACKS

        response = self.client.delete_json(endpoint)
        response.success = response.status_code == 204

        return response
