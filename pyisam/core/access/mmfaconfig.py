"""
@copyright: IBM
"""

import logging

from pyisam.util.restclient import RestClient
import pyisam.util.common as Utils


MMFA_CONFIG = "/iam/access/v8/mmfa-config"

logger = logging.getLogger(__name__)


class MMFAConfig(RestClient):

    def __init__(self, base_url, username, password):
        super(MMFAConfig, self).__init__(base_url, username, password)

    def update(
            self, client_id=None, hostname=None, junction=None, options=None,
            port=None):
        #logger.enter()

        data = {}
        Utils.add_value_string(data, "client_id", client_id)
        Utils.add_value_string(data, "hostname", hostname)
        Utils.add_value_string(data, "junction", junction)
        Utils.add_value_string(data, "options", options)
        Utils.add_value(data, "port", port)

        status_code, content = self.http_post_json(MMFA_CONFIG, data=data)

        result = (status_code == 204, status_code, content)

        #logger.exit(result)
        return result


class MMFAConfig9021(MMFAConfig):

    def __init__(self, base_url, username, password):
        super(MMFAConfig9021, self).__init__(base_url, username, password)

    def update(
            self, client_id=None, hostname=None, junction=None, port=None,
            details_url=None, enrollment_endpoint=None,
            hotp_shared_secret_endpoint=None, totp_shared_secret_endpoint=None,
            token_endpoint=None, authntrxn_endpoint=None,
            mobile_endpoint_prefix=None, discovery_mechanisms=None, 
            options=None):
        #logger.enter()

        endpoints = {}
        Utils.add_value_string(endpoints, "details_url", details_url)
        Utils.add_value_string(
            endpoints, "enrollment_endpoint", enrollment_endpoint)
        Utils.add_value_string(
            endpoints, "hotp_shared_secret_endpoint",
            hotp_shared_secret_endpoint)
        Utils.add_value_string(
            endpoints, "totp_shared_secret_endpoint",
            totp_shared_secret_endpoint)
        Utils.add_value_string(endpoints, "token_endpoint", token_endpoint)
        Utils.add_value_string(
            endpoints, "authntrxn_endpoint", authntrxn_endpoint)
        Utils.add_value_string(
            endpoints, "mobile_endpoint_prefix", mobile_endpoint_prefix)

        data = {}
        Utils.add_value_string(data, "client_id", client_id)
        Utils.add_value_string(data, "hostname", hostname)
        Utils.add_value_string(data, "junction", junction)
        Utils.add_value_string(data, "options", options)
        Utils.add_value(data, "port", port)
        Utils.add_value_not_empty(data, "endpoints", endpoints)
        Utils.add_value_not_empty(
            data, "discovery_mechanisms", discovery_mechanisms)

        status_code, content = self.http_post_json(MMFA_CONFIG, data=data)

        result = (status_code == 204, status_code, content)

        #logger.exit(result)
        return result
