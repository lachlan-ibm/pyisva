"""
@copyright: IBM
"""

import logging

from pyisam.util.model import DataObject, Response
from pyisam.util.restclient import RESTClient


SSL_CERTIFICATES = "/isam/ssl_certificates"

logger = logging.getLogger(__name__)


class SSLCertificates(object):

    def __init__(self, base_url, username, password):
        super(SSLCertificates, self).__init__()
        self.client = RESTClient(base_url, username, password)

    def import_personal(self, kdb_id, file_path, password=None):
        response = Response()

        try:
            with open(file_path, 'rb') as certificate:
                data = DataObject()
                data.add_value_string("operation", "import")
                data.add_value_string("password", password)

                files = {"cert": certificate}

                endpoint = ("%s/%s/personal_cert" % (SSL_CERTIFICATES, kdb_id))

                response = self.client.post_file(
                    endpoint, data=data.data, files=files)
                response.success = response.status_code == 200
        except IOError as e:
            logger.error(e)
            response.success = False

        return response

    def import_signer(self, kdb_id, file_path, label=None):
        response = Response()

        try:
            with open(file_path, 'rb') as certificate:
                data = DataObject()
                data.add_value_string("label", label)

                files = {"cert": certificate}

                endpoint = ("%s/%s/signer_cert" % (SSL_CERTIFICATES, kdb_id))

                response = self.client.post_file(
                    endpoint, data=data.data, files=files)
                response.success = response.status_code == 200
        except IOError as e:
            logger.error(e)
            response.success = False

        return response

    def load_signer(self, kdb_id, server=None, port=None, label=None):
        data = DataObject()
        data.add_value_string("operation", "load")
        data.add_value_string("label", label)
        data.add_value_string("server", server)
        data.add_value("port", port)

        endpoint = ("%s/%s/signer_cert" % (SSL_CERTIFICATES, kdb_id))

        response = self.client.post_json(endpoint, data.data)
        response.success = response.status_code == 200

        return response
