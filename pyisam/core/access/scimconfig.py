"""
@copyright: IBM
"""

import logging

from pyisam.util.restclient import RestClient
import pyisam.util.common as Utils


SCHEMA_ISAM_USER = "urn:ietf:params:scim:schemas:extension:isam:1.0:User"
SCIM_CONFIGURATION = "/mga/scim/configuration"

logger = logging.getLogger(__name__)


class SCIMConfig(RestClient):

    def __init__(self, base_url, username, password):
        super(SCIMConfig, self).__init__(base_url, username, password)

    def get(self):
        #logger.enter()

        status_code, content = self.http_get_json(SCIM_CONFIGURATION)

        result = (status_code == 200, status_code, content)

        #logger.exit(result)
        return result

    def update(self, data):
        #logger.enter()

        status_code, content = self.http_put_json(SCIM_CONFIGURATION, data=data)

        result = (status_code == 200, status_code, content)

        #logger.exit(result)
        return result

    def update_isam_user(
            self, ldap_connection=None, isam_domain=None,
            update_native_users=None):
        #logger.enter()

        data = {}
        Utils.add_value_string(data, "ldap_connection", ldap_connection)
        Utils.add_value_string(data, "isam_domain", isam_domain)
        Utils.add_value(data, "update_native_users", update_native_users)

        endpoint = ("%s/%s" % (SCIM_CONFIGURATION, SCHEMA_ISAM_USER))
        status_code, content = self.http_put_json(endpoint, data=data)

        result = (status_code == 200, status_code, content)

        #logger.exit(result)
        return result
