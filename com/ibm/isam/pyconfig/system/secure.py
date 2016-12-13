"""
@copyright: IBM
"""

import logging

from com.ibm.isam.util.logger import Logger
from com.ibm.isam.util.restclient import RestClient
import com.ibm.isam.util.utils as Utils


SSL_CERTIFICATES = "/isam/ssl_certificates"


class _SecureSettings(RestClient):

    logger = Logger("SecureSettings")

    def __init__(self, base_url, username, password, log_level=logging.NOTSET):
        super(_SecureSettings, self).__init__(
            base_url, username, password, log_level)
        _SecureSettings.logger.set_level(log_level)

    #
    # SSL Certificates
    #

    # Personal

    def import_ssl_certificate_personal(self, kdb_id, file_path, password=None):
        method_name = "import_ssl_certificate_personal()"
        _SecureSettings.logger.enter_method(method_name)
        result = None

        try:
            with open(file_path, 'rb') as certificate:
                data = {}
                Utils.add_string_value(data, "operation", "import")
                Utils.add_string_value(data, "password", password)

                files = {"cert": certificate}

                endpoint = ("%s/%s/personal_cert" % (SSL_CERTIFICATES, kdb_id))
                status_code, content = self.http_post_file(
                    endpoint, data=data, files=files)

                result = (status_code == 200, status_code, content)
        except IOError as e:
            _SecureSettings.logger.error(method_name, e)
            result = (False, None, None)

        _SecureSettings.logger.exit_method(method_name, result)
        return result

    # Signer

    def import_ssl_certificate_signer(self, kdb_id, file_path, label=None):
        method_name = "import_ssl_certificate_signer()"
        _SecureSettings.logger.enter_method(method_name)
        result = None

        try:
            with open(file_path, 'rb') as certificate:
                data = {}
                Utils.add_string_value(data, "label", label)

                files = {"cert": certificate}

                endpoint = ("%s/%s/signer_cert" % (SSL_CERTIFICATES, kdb_id))
                status_code, content = self.http_post_file(
                    endpoint, data=data, files=files)

                result = (status_code == 200, status_code, content)
        except IOError as e:
            _SecureSettings.logger.error(method_name, e)
            result = (False, None, None)

        _SecureSettings.logger.exit_method(method_name, result)
        return result

    def load_ssl_certificate_signer(
            self, kdb_id, server=None, port=None, label=None):
        method_name = "load_ssl_certificate_signer()"
        _SecureSettings.logger.enter_method(method_name)
        result = None

        data = {}
        Utils.add_string_value(data, "operation", "load")
        Utils.add_string_value(data, "label", label)
        Utils.add_string_value(data, "server", server)
        Utils.add_value(data, "port", port)

        endpoint = ("%s/%s/signer_cert" % (SSL_CERTIFICATES, kdb_id))
        status_code, content = self.http_post_json(endpoint, data)

        result = (status_code == 200, status_code, content)

        _SecureSettings.logger.exit_method(method_name, result)
        return result


class SecureSettings9020(_SecureSettings):

    logger = Logger("SecureSettings9020")

    def __init__(self, base_url, username, password, log_level=logging.NOTSET):
        super(SecureSettings9020, self).__init__(
            base_url, username, password, log_level)
        SecureSettings9020.logger.set_level(log_level)
