"""
@copyright: IBM
"""

import logging

from pyisam.util.restclient import RestClient
import pyisam.util.common as Utils


CAPABILITIES = "/isam/capabilities"

logger = logging.getLogger(__name__)


class Licensing(RestClient):

    def __init__(self, base_url, username, password):
        super(Licensing, self).__init__(base_url, username, password)

    def activate_module(self, code):
        #logger.enter()

        data = {}
        Utils.add_value_string(data, "code", code)

        endpoint = CAPABILITIES + "/v1"
        status_code, content = self.http_post_json(endpoint, data)

        result = (status_code == 200, status_code, content)

        #logger.exit(result)
        return result

    def get_activated_module(self, id):
        #logger.enter()

        endpoint = "%s/%s/v1" % (CAPABILITIES, id)
        status_code, content = self.http_get_json(endpoint)

        result = (status_code == 200, status_code, content)

        #logger.exit(result)
        return result

    def get_activated_modules(self):
        #logger.enter()

        endpoint = CAPABILITIES + "/v1"
        status_code, content = self.httpGetJson(endpoint)

        result = (status_code == 200, status_code, content)

        #logger.exit(result)
        return result

    def import_activation_code(self, file_path):
        #logger.enter()
        result = (False, None, None)

        try:
            with open(file_path, 'rb') as code:
                data = {}
                Utils.add_value_string(data, "name", "activation")

                files = {"filename": code}

                endpoint = CAPABILITIES + "/v1"
                status_code, content = self.http_post_file(
                    endpoint, data=data, files=files)

                result = (status_code == 200, status_code, content)
        except IOError as e:
            logger.error(e)

        #logger.exit(result)
        return result
