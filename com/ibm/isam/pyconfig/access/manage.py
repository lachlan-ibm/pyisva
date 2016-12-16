"""
@copyright: IBM
"""

import logging

from com.ibm.isam.util.logger import Logger
from com.ibm.isam.util.restclient import RestClient
import com.ibm.isam.util.utils as Utils


MMFA_CONFIG = "/iam/access/v8/mmfa-config"
SCHEMA_ISAM_USER = "urn:ietf:params:scim:schemas:extension:isam:1.0:User"
SCIM_CONFIGURATION = "/mga/scim/configuration"


class Manage(RestClient):

    logger = Logger("Manage")

    def __init__(self, base_url, username, password, log_level=logging.NOTSET):
        super(Manage, self).__init__(base_url, username, password, log_level)
        Manage.logger.set_level(log_level)

    #
    # SCIM Configuration
    #

    # General

    def get_scim_configuration(self):
        Manage.logger.enter()
        result = None

        status_code, content = self.http_get_json(SCIM_CONFIGURATION)

        result = (status_code == 200, status_code, content)

        Manage.logger.exit(result)
        return result

    def update_scim_configuration(self, data):
        Manage.logger.enter()
        result = None

        status_code, content = self.http_put_json(SCIM_CONFIGURATION, data=data)

        result = (status_code == 200, status_code, content)

        Manage.logger.exit(result)
        return result

    # ISAM User

    def update_scim_configuration_isam_user(
            self, ldap_connection=None, isam_domain=None,
            update_native_users=None):
        Manage.logger.enter()
        result = None

        data = {}
        Utils.add_value_string(data, "ldap_connection", ldap_connection)
        Utils.add_value_string(data, "isam_domain", isam_domain)
        Utils.add_value(data, "update_native_users", update_native_users)

        endpoint = ("%s/%s" % (SCIM_CONFIGURATION, SCHEMA_ISAM_USER))
        status_code, content = self.http_put_json(endpoint, data=data)

        result = (status_code == 200, status_code, content)

        Manage.logger.exit(result)
        return result

    #
    # MMFA Configuration
    #

    def update_mmfa_configuration(
            self, client_id=None, hostname=None, junction=None, options=None,
            port=None):
        Manage.logger.enter()
        result = None

        data = {}
        Utils.add_value_string(data, "client_id", client_id)
        Utils.add_value_string(data, "hostname", hostname)
        Utils.add_value_string(data, "junction", junction)
        Utils.add_value_string(data, "options", options)
        Utils.add_value(data, "port", port)

        status_code, content = self.http_post_json(MMFA_CONFIG, data=data)

        result = (status_code == 204, status_code, content)

        Manage.logger.exit(result)
        return result


class Manage9021(Manage):

    logger = Logger("Manage9021")

    def __init__(self, base_url, username, password, log_level=logging.NOTSET):
        super(Manage9021, self).__init__(
            base_url, username, password, log_level)
        Manage9021.logger.set_level(log_level)

    def update_mmfa_configuration(
            self, client_id=None, hostname=None, junction=None, port=None,
            details_url=None, enrollment_endpoint=None,
            hotp_shared_secret_endpoint=None, totp_shared_secret_endpoint=None,
            token_endpoint=None, authntrxn_endpoint=None,
            discovery_mechanisms=None, options=None):
        Manage.logger.enter()
        result = None

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

        Manage.logger.exit(result)
        return result
