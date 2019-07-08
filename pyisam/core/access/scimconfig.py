"""
@copyright: IBM
"""

import logging

from pyisam.util.model import DataObject
from pyisam.util.restclient import RESTClient

"""
Test comment by Shane
"""
SCHEMA_ISAM_USER = "urn:ietf:params:scim:schemas:extension:isam:1.0:User"
SCIM_CONFIGURATION = "/mga/scim/configuration"
SCIM_CONFIGURATION_GENERAL = "/mga/scim/configuration/general"

logger = logging.getLogger(__name__)


class SCIMConfig(object):

    def __init__(self, base_url, username, password):
        super(SCIMConfig, self).__init__()
        self.client = RESTClient(base_url, username, password)

    def get(self):
        response = self.client.get_json(SCIM_CONFIGURATION)
        response.success = response.status_code == 200

        return response

    def get_schema(self,schema_name):
        endpoint = "%s/%s" % (SCIM_CONFIGURATION,schema_name)

        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200

        return response

    def update(self, data):
        response = self.client.put_json(SCIM_CONFIGURATION, data)
        response.success = response.status_code == 200

        return response

    def update_schema(self, schema_name, data):
        endpoint = "%s/%s" % (SCIM_CONFIGURATION,schema_name)

        response = self.client.put_json(endpoint, data)
        response.success = response.status_code == 200

        return response

    def update_config(self, admin_group="adminGroup",enable_header_authentication=True, enable_authz_filter=True):

        data = DataObject()
        data.add_value_string("admin_group", admin_group)
        data.add_value_string("enable_header_authentication", enable_header_authentication)
        data.add_value_string("enable_authz_filter", enable_authz_filter)

        response = self.client.put_json(SCIM_CONFIGURATION_GENERAL, data.data)
        response.success = response.status_code == 200

        return response

    def update_attribute_mode(
            self, schema_name, scim_attribute, scim_subattribute=None,
            mode=None):

        data = DataObject()
        data.add_value_string("mode", mode)

        endpoint = "%s/attribute_modes/%s/%s" % (
            SCIM_CONFIGURATION_GENERAL, schema_name, scim_attribute)
        if scim_subattribute:
            endpoint = "%s/%s" % (endpoint, scim_subattribute)

        response = self.client.put_json(endpoint, data.data)
        response.success = response.status_code == 204

        return response

    def update_isam_user(
            self, ldap_connection=None, isam_domain=None, update_native_users=None):
        data = DataObject()
        data.add_value_string("ldap_connection", ldap_connection)
        data.add_value_string("isam_domain", isam_domain)        
        data.add_value("update_native_users", update_native_users)

        endpoint = ("%s/%s" % (SCIM_CONFIGURATION, SCHEMA_ISAM_USER))

        response = self.client.put_json(endpoint, data.data)
        response.success = response.status_code == 200

        return response
        
class SCIMConfig9050(SCIMConfig):
    def __init__(self, base_url, username, password):
        super(SCIMConfig, self).__init__()
        self.client = RESTClient(base_url, username, password)
        
    def update_isam_user(
            self, ldap_connection=None, isam_domain=None, connection_type=None,
            update_native_users=None):
        data = DataObject()
        data.add_value_string("ldap_connection", ldap_connection)
        data.add_value_string("isam_domain", isam_domain)        
        data.add_value_string("connection_type", connection_type)
        data.add_value("update_native_users", update_native_users)

        endpoint = ("%s/%s" % (SCIM_CONFIGURATION, SCHEMA_ISAM_USER))

        response = self.client.put_json(endpoint, data.data)
        response.success = response.status_code == 200
        return response

