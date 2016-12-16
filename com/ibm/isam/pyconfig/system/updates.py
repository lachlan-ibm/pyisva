"""
@copyright: IBM
"""

import logging

from com.ibm.isam.util.logger import Logger
from com.ibm.isam.util.restclient import RestClient
import com.ibm.isam.util.utils as Utils


CAPABILITIES = "/isam/capabilities"


class UpdatesLicensing(RestClient):

    logger = Logger("UpdatesLicensing")

    def __init__(self, base_url, username, password, log_level=logging.NOTSET):
        super(UpdatesLicensing, self).__init__(
            base_url, username, password, log_level)
        UpdatesLicensing.logger.set_level(log_level)

    #
    # Licensing and Activation
    #

    def activate_module(self, code):
        UpdatesLicensing.logger.enter()
        result = None

        data = {}
        Utils.add_value_string(data, "code", code)

        endpoint = CAPABILITIES + "/v1"
        status_code, content = self.http_post_json(endpoint, data)

        result = (status_code == 200, status_code, content)

        UpdatesLicensing.logger.exit(result)
        return result

    def get_activated_module(self, id):
        UpdatesLicensing.logger.enter()
        result = None

        endpoint = "%s/%s/v1" % (CAPABILITIES, id)
        status_code, content = self.http_get_json(endpoint)

        result = (status_code == 200, status_code, content)

        UpdatesLicensing.logger.exit(result)
        return result

    def get_activated_modules(self):
        UpdatesLicensing.logger.enter()
        result = None

        endpoint = CAPABILITIES + "/v1"
        status_code, content = self.httpGetJson(endpoint)

        result = (status_code == 200, status_code, content)

        UpdatesLicensing.logger.exit(result)
        return result

    def import_activation_code(self, file_path):
        UpdatesLicensing.logger.enter()
        result = None

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
            UpdatesLicensing.logger.error(e)
            result = (False, None, None)

        UpdatesLicensing.logger.exit(result)
        return result
