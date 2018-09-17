"""
@copyright: IBM
"""

import logging

from pyisam.util.model import DataObject
from pyisam.util.restclient import RESTClient


MMFA_CONFIG = "/iam/access/v8/mmfa-config"

logger = logging.getLogger(__name__)


class MMFAConfig(object):

    def __init__(self, base_url, username, password):
        super(MMFAConfig, self).__init__()
        self.client = RESTClient(base_url, username, password)

    def update(
            self, client_id=None, hostname=None, junction=None, options=None,
            port=None):
        data = DataObject()
        data.add_value_string("client_id", client_id)
        data.add_value_string("hostname", hostname)
        data.add_value_string("junction", junction)
        data.add_value_string("options", options)
        data.add_value("port", port)

        response = self.client.post_json(MMFA_CONFIG, data.data)
        response.success = response.status_code == 204

        return response


class MMFAConfig9021(MMFAConfig):

    def __init__(self, base_url, username, password):
        super(MMFAConfig9021, self).__init__(base_url, username, password)

    def update(
            self, client_id=None, hostname=None, junction=None, port=None,
            details_url=None, enrollment_endpoint=None,
            hotp_shared_secret_endpoint=None, totp_shared_secret_endpoint=None,
            token_endpoint=None, authntrxn_endpoint=None,
            mobile_endpoint_prefix=None, qrlogin_endpoint=None,
            discovery_mechanisms=None, options=None):
        endpoints = DataObject()
        endpoints.add_value_string("details_url", details_url)
        endpoints.add_value_string("enrollment_endpoint", enrollment_endpoint)
        endpoints.add_value_string(
            "hotp_shared_secret_endpoint",hotp_shared_secret_endpoint)
        endpoints.add_value_string(
            "totp_shared_secret_endpoint",totp_shared_secret_endpoint)
        endpoints.add_value_string("token_endpoint", token_endpoint)
        endpoints.add_value_string("authntrxn_endpoint", authntrxn_endpoint)
        endpoints.add_value_string(
            "mobile_endpoint_prefix", mobile_endpoint_prefix)
        endpoints.add_value_not_empty("qrlogin_endpoint", qrlogin_endpoint)

        data = DataObject()
        data.add_value_string("client_id", client_id)
        data.add_value_string("hostname", hostname)
        data.add_value_string("junction", junction)
        data.add_value_string("options", options)
        data.add_value("port", port)
        data.add_value_not_empty("endpoints", endpoints.data)
        data.add_value_not_empty("discovery_mechanisms", discovery_mechanisms)

        response = self.client.post_json(MMFA_CONFIG, data.data)
        response.success = response.status_code == 204

        return response
