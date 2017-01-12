"""
@copyright: IBM
"""

import logging

from pyisam.util.restclient import RestClient
import pyisam.util.common as Utils


SSL_CERTIFICATES = "/isam/ssl_certificates"

logger = logging.getLogger(__name__)


class SSLCertificates(RestClient):

    def __init__(self, base_url, username, password):
        super(SSLCertificates, self).__init__(base_url, username, password)

    def import_personal(self, kdb_id, file_path, password=None):
        #logger.enter()
        result = (False, None, None)

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
            logger.error(e)

        #logger.exit(result)
        return result

    def import_signer(self, kdb_id, file_path, label=None):
        #logger.enter()
        result = (False, None, None)

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
            logger.error(e)

        #logger.exit(result)
        return result

    def load_signer(self, kdb_id, server=None, port=None, label=None):
        #logger.enter()

        data = {}
        Utils.add_value_string(data, "operation", "load")
        Utils.add_value_string(data, "label", label)
        Utils.add_value_string(data, "server", server)
        Utils.add_value(data, "port", port)

        endpoint = ("%s/%s/signer_cert" % (SSL_CERTIFICATES, kdb_id))
        status_code, content = self.http_post_json(endpoint, data)

        result = (status_code == 200, status_code, content)

        #logger.exit(result)
        return result
