"""
@copyright: IBM
"""

import logging

from pyisam.util.logger import Logger
from pyisam.util.restclient import RestClient
import pyisam.util.common as Utils


SSL_CERTIFICATES = "/isam/ssl_certificates"


class SecureSettings(RestClient):

    logger = Logger("SecureSettings")

    def __init__(self, base_url, username, password, log_level=logging.NOTSET):
        super(SecureSettings, self).__init__(
            base_url, username, password, log_level)
        SecureSettings.logger.set_level(log_level)

    #
    # SSL Certificates
    #

    # Personal

    def import_ssl_certificate_personal(self, kdb_id, file_path, password=None):
        SecureSettings.logger.enter()
        result = None

        try:
            with open(file_path, 'rb') as certificate:
                data = {}
                Utils.add_value_string(data, "operation", "import")
                Utils.add_value_string(data, "password", password)

                files = {"cert": certificate}

                endpoint = ("%s/%s/personal_cert" % (SSL_CERTIFICATES, kdb_id))
                status_code, content = self.http_post_file(
                    endpoint, data=data, files=files)

                result = (status_code == 200, status_code, content)
        except IOError as e:
            SecureSettings.logger.error(e)
            result = (False, None, None)

        SecureSettings.logger.exit(result)
        return result

    # Signer

    def import_ssl_certificate_signer(self, kdb_id, file_path, label=None):
        SecureSettings.logger.enter()
        result = None

        try:
            with open(file_path, 'rb') as certificate:
                data = {}
                Utils.add_value_string(data, "label", label)

                files = {"cert": certificate}

                endpoint = ("%s/%s/signer_cert" % (SSL_CERTIFICATES, kdb_id))
                status_code, content = self.http_post_file(
                    endpoint, data=data, files=files)

                result = (status_code == 200, status_code, content)
        except IOError as e:
            SecureSettings.logger.error(e)
            result = (False, None, None)

        SecureSettings.logger.exit(result)
        return result

    def load_ssl_certificate_signer(
            self, kdb_id, server=None, port=None, label=None):
        SecureSettings.logger.enter()
        result = None

        data = {}
        Utils.add_value_string(data, "operation", "load")
        Utils.add_value_string(data, "label", label)
        Utils.add_value_string(data, "server", server)
        Utils.add_value(data, "port", port)

        endpoint = ("%s/%s/signer_cert" % (SSL_CERTIFICATES, kdb_id))
        status_code, content = self.http_post_json(endpoint, data)

        result = (status_code == 200, status_code, content)

        SecureSettings.logger.exit(result)
        return result
