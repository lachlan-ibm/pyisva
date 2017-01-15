"""
@copyright: IBM
"""

import logging

from pyisam.util.model import DataObject
from pyisam.util.restclient import RESTClient


SCHEMA_ISAM_USER = "urn:ietf:params:scim:schemas:extension:isam:1.0:User"
SCIM_CONFIGURATION = "/mga/scim/configuration"

logger = logging.getLogger(__name__)


class SCIMConfig(object):

    def __init__(self, base_url, username, password):
        super(SCIMConfig, self).__init__()
        self.client = RESTClient(base_url, username, password)

    def get(self):
        response = self.client.get_json(SCIM_CONFIGURATION)
        response.success = response.status_code == 200

        return response

    def update(self, data):
        response = self.client.put_json(SCIM_CONFIGURATION, data=data)
        response.success = response.status_code == 200

        return response

    def update_isam_user(
            self, ldap_connection=None, isam_domain=None,
            update_native_users=None):
        data = DataObject()
        data.add_value_string("ldap_connection", ldap_connection)
        data.add_value_string("isam_domain", isam_domain)
        data.add_value("update_native_users", update_native_users)

        endpoint = ("%s/%s" % (SCIM_CONFIGURATION, SCHEMA_ISAM_USER))

        response = self.client.put_json(endpoint, data.data)
        response.success = response.status_code == 200

        return response
