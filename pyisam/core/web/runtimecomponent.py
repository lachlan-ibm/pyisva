"""
@copyright: IBM
"""

import logging

from pyisam.util.common import add_value, add_value_not_empty, add_value_string
from pyisam.util.restclient import RestClient


EMBEDDED_LDAP_PASSWORD = "/isam/embedded_ldap/change_pwd/v1"
RUNTIME_COMPONENT = "/isam/runtime_components"


logger = logging.getLogger(__name__)


class RuntimeComponent(RestClient):

    def __init__(self, base_url, username, password):
        super(RuntimeComponent, self).__init__(base_url, username, password)

    def configure(
            self, ps_mode=None, user_registry=None, admin_password=None,
            ldap_password=None, admin_cert_lifetime=None, ssl_compliance=None,
            ldap_host=None, ldap_port=None, isam_domain=None, ldap_dn=None,
            ldap_suffix=None, ldap_ssl_db=None, ldap_ssl_label=None,
            isam_host=None, isam_port=None):
        #logger.enter()
        result = None

        data = {}
        add_value_string(data, "ps_mode", ps_mode)
        add_value_string(data, "user_registry", user_registry)
        add_value_string(data, "admin_cert_lifetime", admin_cert_lifetime)
        add_value_string(data, "ssl_compliance", ssl_compliance)
        add_value_string(data, "admin_pwd", admin_password)
        add_value_string(data, "ldap_pwd", ldap_password)
        add_value_string(data, "ldap_host", ldap_host)
        add_value_string(data, "domain", isam_domain)
        add_value_string(data, "ldap_dn", ldap_dn)
        add_value_string(data, "ldap_suffix", ldap_suffix)
        add_value_string(data, "ldap_ssl_db", ldap_ssl_db)
        add_value_string(data, "ldap_ssl_label", ldap_ssl_label)
        add_value_string(data, "isam_host", isam_host)
        add_value(data, "ldap_port", ldap_port)
        add_value(data, "isam_port", isam_port)

        status_code, content = self.http_post_json(RUNTIME_COMPONENT, data)

        result = (status_code == 200, status_code, content)

        #logger.exit(result)
        return result

    def update_embedded_ldap_password(self, password):
        #logger.enter()
        result = None

        data = {}
        add_value_string(data, "password", password)

        status_code, content = self.http_post_json(EMBEDDED_LDAP_PASSWORD, data)

        result = (status_code == 200, status_code, content)

        #logger.exit(result)
        return result
