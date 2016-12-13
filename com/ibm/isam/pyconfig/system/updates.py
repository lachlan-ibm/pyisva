"""
@copyright: IBM
"""

import logging

from com.ibm.isam.util.logger import Logger
from com.ibm.isam.util.restclient import RestClient
import com.ibm.isam.util.utils as Utils


CAPABILITIES = "/isam/capabilities"


class _UpdatesLicensing(RestClient):

    logger = Logger("UpdatesLicensing")

    def __init__(self, base_url, username, password, log_level=logging.NOTSET):
        super(_UpdatesLicensing, self).__init__(
            base_url, username, password, log_level)
        _UpdatesLicensing.logger.set_level(log_level)

    #
    # Licensing and Activation
    #

    def activate_module(self, code):
        method_name = "activate_module()"
        _UpdatesLicensing.logger.enter_method(method_name)
        result = None

        data = {}
        Utils.add_string_value(data, "code", code)

        endpoint = CAPABILITIES + "/v1"
        status_code, content = self.http_post_json(endpoint, data)

        result = (status_code == 200, status_code, content)

        _UpdatesLicensing.logger.exit_method(method_name, result)
        return result

    def get_activated_module(self, id):
        method_name = "get_activated_module()"
        _UpdatesLicensing.logger.enter_method(method_name)
        result = None

        endpoint = "%s/%s/v1" % (CAPABILITIES, id)
        status_code, content = self.http_get_json(endpoint)

        result = (status_code == 200, status_code, content)

        _UpdatesLicensing.logger.exit_method(method_name, result)
        return result

    def get_activated_modules(self):
        method_name = "get_activated_modules()"
        _UpdatesLicensing.logger.enter_method(method_name)
        result = None

        endpoint = CAPABILITIES + "/v1"
        status_code, content = self.httpGetJson(endpoint)

        result = (status_code == 200, status_code, content)

        _UpdatesLicensing.logger.exit_method(method_name, result)
        return result

    def import_activation_code(self, file_path):
        method_name = "import_activation_code()"
        _UpdatesLicensing.logger.enter_method(method_name)
        result = None

        try:
            with open(file_path, 'rb') as code:
                data = {}
                Utils.add_string_value(data, "name", "activation")

                files = {"filename": code}

                endpoint = CAPABILITIES + "/v1"
                status_code, content = self.http_post_file(
                    endpoint, data=data, files=files)

                result = (status_code == 200, status_code, content)
        except IOError as e:
            _SecureSettings.logger.error(method_name, e)
            result = (False, None, None)

        _UpdatesLicensing.logger.exit_method(method_name, result)
        return result


class UpdatesLicensing9020(_UpdatesLicensing):

    logger = Logger("UpdatesLicensing9020")

    def __init__(self, base_url, username, password, log_level=logging.NOTSET):
        super(UpdatesLicensing9020, self).__init__(
            base_url, username, password, log_level)
        UpdatesLicensing9020.logger.set_level(log_level)
