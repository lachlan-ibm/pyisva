"""
@copyright: IBM
"""

import logging

from pyisam.util.restclient import RestClient
import pyisam.util.common as Utils


SERVER_CONNECTION_LDAP = "/mga/server_connections/ldap"
SERVER_CONNECTION_WEB_SERVICE = "/mga/server_connections/ws"

logger = logging.getLogger(__name__)


class ServerConnections(RestClient):

    def __init__(self, base_url, username, password):
        super(ServerConnections, self).__init__(base_url, username, password)

    def create_ldap(
            self, name=None, description=None, locked=None,
            connection_host_name=None, connection_bind_dn=None,
            connection_bind_pwd=None, connection_ssl_truststore=None,
            connection_ssl_auth_key=None, connection_host_port=None,
            connection_ssl=None, connect_timeout=None, servers=None):
        #logger.enter()

        connection_data = {}
        Utils.add_value_string(
            connection_data, "hostName", connection_host_name)
        Utils.add_value_string(connection_data, "bindDN", connection_bind_dn)
        Utils.add_value_string(connection_data, "bindPwd", connection_bind_pwd)
        Utils.add_value_string(
            connection_data, "sslTruststore", connection_ssl_truststore)
        Utils.add_value_string(
            connection_data, "sslAuthKey", connection_ssl_auth_key)
        Utils.add_value(connection_data, "hostPort", connection_host_port)
        Utils.add_value(connection_data, "ssl", connection_ssl)

        manager_data = {}
        Utils.add_value(manager_data, "connectTimeout", connect_timeout)

        data = {}
        Utils.add_value_string(data, "name", name)
        Utils.add_value_string(data, "description", description)
        Utils.add_value_string(data, "type", "ldap")
        Utils.add_value(data, "locked", locked)
        Utils.add_value(data, "servers", servers)
        Utils.add_value_not_empty(data, "connection", connection_data)
        Utils.add_value_not_empty(data, "connectionManager", manager_data)

        endpoint = SERVER_CONNECTION_LDAP + "/v1"
        status_code, content = self.http_post_json(endpoint, data=data)

        result = (status_code == 201, status_code, content)

        #logger.exit(result)
        return result

    def delete_ldap(self, uuid):
        #logger.enter()

        endpoint = "%s/%s/v1" % (SERVER_CONNECTION_LDAP, uuid)
        status_code, content = self.http_delete_json(endpoint)

        result = (status_code == 204, status_code, content)

        #logger.exit(result)
        return result

    def list_ldap(self):
        #logger.enter()

        endpoint = SERVER_CONNECTION_LDAP + "/v1"
        status_code, content = self.http_get_json(endpoint)

        result = (status_code == 200, status_code, content)

        #logger.exit(result)
        return result

    def create_web_service(
            self, name=None, description=None, locked=None, connection_url=None,
            connection_user=None, connection_password=None,
            connection_ssl_truststore=None, connection_ssl_auth_key=None,
            connection_ssl=None):
        #logger.enter()

        connection_data = {}
        Utils.add_value_string(connection_data, "url", connection_url)
        Utils.add_value_string(connection_data, "user", connection_user)
        Utils.add_value_string(connection_data, "password", connection_password)
        Utils.add_value_string(
            connection_data, "sslTruststore", connection_ssl_truststore)
        Utils.add_value_string(
            connection_data, "sslAuthKey", connection_ssl_auth_key)
        Utils.add_value(connection_data, "ssl", connection_ssl)

        data = {}
        Utils.add_value_string(data, "name", name)
        Utils.add_value_string(data, "description", description)
        Utils.add_value_string(data, "type", "ws")
        Utils.add_value(data, "locked", locked)
        Utils.add_value_not_empty(data, "connection", connection_data)

        endpoint = SERVER_CONNECTION_WEB_SERVICE + "/v1"
        status_code, content = self.http_post_json(endpoint, data=data)

        result = (status_code == 201, status_code, content)

        #logger.exit(result)
        return result

    def list_web_service(self):
        #logger.enter()

        endpoint = SERVER_CONNECTION_WEB_SERVICE + "/v1"
        status_code, content = self.http_get_json(endpoint)

        result = (status_code == 200, status_code, content)

        #logger.exit(result)
        return result
