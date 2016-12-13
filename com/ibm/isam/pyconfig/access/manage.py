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


class _Manage(RestClient):

    logger = Logger("Manage")

    def __init__(self, base_url, username, password, log_level=logging.NOTSET):
        super(_Manage, self).__init__(base_url, username, password, log_level)
        _Manage.logger.set_level(log_level)

    #
    # SCIM Configuration
    #

    # General

    def get_scim_configuration(self):
        method_name = "get_scim_configuration()"
        _Manage.logger.enter_method(method_name)
        result = None

        status_code, content = self.http_get_json(SCIM_CONFIGURATION)

        result = (status_code == 200, status_code, content)

        _Manage.logger.exit_method(method_name, result)
        return result

    def update_scim_configuration(self, data):
        method_name = "update_scim_configuration()"
        _Manage.logger.enter_method(method_name)
        result = None

        status_code, content = self.http_put_json(SCIM_CONFIGURATION, data=data)

        result = (status_code == 200, status_code, content)

        _Manage.logger.exit_method(method_name, result)
        return result

    # ISAM User

    def update_scim_configuration_isam_user(
            self, ldap_connection=None, isam_domain=None,
            update_native_users=None):
        method_name = "update_scim_configuration_isam_user()"
        _Manage.logger.enter_method(method_name)
        result = None

        data = {}
        Utils.add_string_value(data, "ldap_connection", ldap_connection)
        Utils.add_string_value(data, "isam_domain", isam_domain)
        Utils.add_value(data, "update_native_users", update_native_users)

        endpoint = ("%s/%s" % (SCIM_CONFIGURATION, SCHEMA_ISAM_USER))
        status_code, content = self.http_put_json(endpoint, data=data)

        result = (status_code == 200, status_code, content)

        _Manage.logger.exit_method(method_name, result)
        return result

    #
    # MMFA Configuration
    #

    def update_mmfa_configuration(
            self, client_id=None, hostname=None, junction=None, options=None,
            port=None):
        method_name = "update_mmfa_configuration()"
        _Manage.logger.enter_method(method_name)
        result = None

        data = {}
        Utils.add_string_value(data, "client_id", client_id)
        Utils.add_string_value(data, "hostname", hostname)
        Utils.add_string_value(data, "junction", junction)
        Utils.add_string_value(data, "options", options)
        Utils.add_value(data, "port", port)

        status_code, content = self.http_post_json(MMFA_CONFIG, data=data)

        result = (status_code == 204, status_code, content)

        _Manage.logger.exit_method(method_name, result)
        return result


class Manage9020(_Manage):

    logger = Logger("Manage9020")

    def __init__(self, base_url, username, password, log_level=logging.NOTSET):
        super(Manage9020, self).__init__(
            base_url, username, password, log_level)
        Manage9020.logger.set_level(log_level)
