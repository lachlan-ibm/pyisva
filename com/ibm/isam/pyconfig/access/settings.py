"""
@copyright: IBM
"""

import logging

from com.ibm.isam.util.logger import Logger
from com.ibm.isam.util.restclient import RestClient
import com.ibm.isam.util.utils as Utils


OVERRIDE_CONFIGS = "/iam/access/v8/override-configs"
RUNTIME_TUNING = "/mga/runtime_tuning"
SERVER_CONNECTION_LDAP = "/mga/server_connections/ldap"
SERVER_CONNECTION_WEB_SERVICE = "/mga/server_connections/ws"
TEMPLATE_FILES = "/mga/template_files"
USER_REGISTRY = "/mga/user_registry"


class GlobalSettings(RestClient):

    logger = Logger("GlobalSettings")

    def __init__(self, base_url, username, password, log_level=logging.NOTSET):
        super(GlobalSettings, self).__init__(
            base_url, username, password, log_level)
        GlobalSettings.logger.set_level(log_level)

    #
    # Advanced Configuration
    #

    def get_advanced_configuration_by_key(self, key):
        GlobalSettings.logger.enter()
        result = None

        filter = "key equals " + str(key)
        success, status_code, content = self.get_advanced_configurations(
            filter=filter)

        if success and content:
            result = (success, status_code, content[0])
        else:
            result = (success, status_code, content)

        GlobalSettings.logger.exit(result)
        return result

    def get_advanced_configurations(
            self, sortBy=None, count=None, start=None, filter=None):
        GlobalSettings.logger.enter()
        result = None

        parameters = {}
        Utils.add_value_string(parameters, "sortBy", sortBy)
        Utils.add_value_string(parameters, "count", count)
        Utils.add_value_string(parameters, "start", start)
        Utils.add_value_string(parameters, "filter", filter)

        status_code, content = self.http_get_json(
            OVERRIDE_CONFIGS, parameters=parameters)

        result = (status_code == 200, status_code, content)

        GlobalSettings.logger.exit(result)
        return result

    def update_advanced_configuration(self, id, value=None, sensitive=None):
        GlobalSettings.logger.enter()
        result = None

        data = {}
        Utils.add_value_string(data, "value", value)
        Utils.add_value(data, "sensitive", sensitive)

        endpoint = "%s/%s" % (OVERRIDE_CONFIGS, id)
        status_code, content = self.http_put_json(endpoint, data=data)

        result = (status_code == 204, status_code, content)

        GlobalSettings.logger.exit(result)
        return result

    def update_advanced_configuration_by_key(
            self, key, value=None, sensitive=None):
        GlobalSettings.logger.enter()
        result = None

        success, status_code, content = self.get_advanced_configuration_by_key(
            key)

        if success:
            id = content.get("id", None)
            result = self.update_advanced_configuration(id, value, sensitive)
        else:
            result = (success, status_code, content)

        GlobalSettings.logger.exit(result)
        return result

    #
    # Runtime Parameters
    #

    def update_runtime_tuning_parameter(self, parameter, value=None):
        GlobalSettings.logger.enter()
        result = None

        data = {}
        Utils.add_value(data, "value", value)

        endpoint = "%s/%s/v1" % (RUNTIME_TUNING, parameter)
        status_code, content = self.http_put_json(endpoint, data=data)

        result = (status_code == 200, status_code, content)

        GlobalSettings.logger.exit(result)
        return result

    #
    # Server Connections
    #

    # LDAP

    def create_server_connection_ldap(
            self, name=None, description=None, locked=None,
            connection_host_name=None, connection_bind_dn=None,
            connection_bind_pwd=None, connection_ssl_truststore=None,
            connection_ssl_auth_key=None, connection_host_port=None,
            connection_ssl=None, connect_timeout=None, servers=None):
        GlobalSettings.logger.enter()
        result = None

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

        GlobalSettings.logger.exit(result)
        return result

    def delete_server_connection_ldap(self, uuid):
        GlobalSettings.logger.enter()
        result = None

        endpoint = "%s/%s/v1" % (SERVER_CONNECTION_LDAP, uuid)
        status_code, content = self.http_delete_json(endpoint)

        result = (status_code == 204, status_code, content)

        GlobalSettings.logger.exit(result)
        return result

    def get_server_connection_ldap_by_name(self, name):
        GlobalSettings.logger.enter()
        result = None

        success, status_code, content = self.get_server_connections_ldap()

        if success:
            for entry in content:
                if entry.get("name", "") == name:
                    result = (success, status_code, entry)

            if not result:
                result = (False, 404, content)
        else:
            result = (success, status_code, content)

        GlobalSettings.logger.exit(result)
        return result

    def get_server_connections_ldap(self):
        GlobalSettings.logger.enter()
        result = None

        endpoint = SERVER_CONNECTION_LDAP + "/v1"
        status_code, content = self.http_get_json(endpoint)

        result = (status_code == 200, status_code, content)

        GlobalSettings.logger.exit(result)
        return result

    # Web Service

    def create_server_connection_web_service(
            self, name=None, description=None, locked=None, connection_url=None,
            connection_user=None, connection_password=None,
            connection_ssl_truststore=None, connection_ssl_auth_key=None,
            connection_ssl=None):
        GlobalSettings.logger.enter()
        result = None

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

        GlobalSettings.logger.exit(result)
        return result

    def get_server_connection_web_service_by_name(self, name):
        GlobalSettings.logger.enter()
        result = None

        success, status_code, content = self.get_server_connections_web_service()

        if success:
            for entry in content:
                if entry.get("name", "") == name:
                    result = (success, status_code, entry)

            if not result:
                result = (False, 404, content)
        else:
            result = (success, status_code, content)

        GlobalSettings.logger.exit(result)
        return result

    def get_server_connections_web_service(self):
        GlobalSettings.logger.enter()
        result = None

        endpoint = SERVER_CONNECTION_WEB_SERVICE + "/v1"
        status_code, content = self.http_get_json(endpoint)

        result = (status_code == 200, status_code, content)

        GlobalSettings.logger.exit(result)
        return result

    #
    # Template Files
    #

    # Directories

    def create_template_file_directory(self, path, dir_name=None):
        GlobalSettings.logger.enter()
        result = None

        data = {}
        Utils.add_value_string(data, "dir_name", dir_name)
        Utils.add_value_string(data, "type", "dir")

        endpoint = "%s/%s" % (TEMPLATE_FILES, path)
        status_code, content = self.http_post_json(endpoint, data=data)

        result = (status_code == 200, status_code, content)

        GlobalSettings.logger.exit(result)
        return result

    def get_template_file_directory(self, path, recursive=None):
        GlobalSettings.logger.enter()
        result = None

        parameters = {}
        Utils.add_value(parameters, "recursive", recursive)

        endpoint = "%s/%s" % (TEMPLATE_FILES, path)
        status_code, content = self.http_get_json(
            endpoint, parameters=parameters)

        if status_code == 200:
            if isinstance(content, list):
                result = (True, status_code, content)
            else:
                result = (True, status_code, content.get("contents"))
        else:
            result = (False, status_code, content)

        GlobalSettings.logger.exit(result)
        return result

    # Files

    def create_template_file(self, path, file_name=None, content=None):
        GlobalSettings.logger.enter()
        result = None

        data = {}
        Utils.add_value_string(data, "file_name", file_name)
        Utils.add_value_string(data, "content", content)
        Utils.add_value_string(data, "type", "file")

        endpoint = "%s/%s" % (TEMPLATE_FILES, path)
        status_code, content = self.http_post_json(endpoint, data=data)

        result = (status_code == 200, status_code, content)

        GlobalSettings.logger.exit(result)
        return result

    def delete_template_file(self, path, file_name):
        GlobalSettings.logger.enter()
        result = None

        endpoint = ("%s/%s/%s" % (TEMPLATE_FILES, path, file_name))
        status_code, content = self.http_delete_json(endpoint)

        result = (status_code == 200, status_code, content)

        GlobalSettings.logger.exit(result)
        return result

    def get_template_file(self, path, file_name):
        GlobalSettings.logger.enter()
        result = None

        endpoint = ("%s/%s/%s" % (TEMPLATE_FILES, path, file_name))
        status_code, content = self.http_get_json(endpoint)

        result = (status_code == 200, status_code, content)

        GlobalSettings.logger.exit(result)
        return result

    def import_template_file(self, path, file_name, file_path):
        GlobalSettings.logger.enter()
        result = None

        try:
            with open(file_path, 'rb') as template:
                files = {"file": template}

                endpoint = ("%s/%s/%s" % (TEMPLATE_FILES, path, file_name))
                status_code, content = self.http_post_file(
                    endpoint, files=files)

                result = (status_code == 200, status_code, content)
        except IOError as e:
            GlobalSettings.logger.error(e)
            result = (False, None, None)

        GlobalSettings.logger.exit(result)
        return result

    def update_template_file(self, path, file_name, content=None):
        GlobalSettings.logger.enter()
        result = None

        data = {}
        Utils.add_value_string(data, "content", content)
        Utils.add_value_string(data, "type", "file")

        endpoint = ("%s/%s/%s" % (TEMPLATE_FILES, path, file_name))
        status_code, content = self.http_put_json(endpoint, data=data)

        result = (status_code == 200, status_code, content)

        GlobalSettings.logger.exit(result)
        return result

    #
    # User Registry
    #

    # Users

    def update_user_registry_user_password(self, username, password=None):
        GlobalSettings.logger.enter()
        result = None

        data = {}
        Utils.add_value_string(data, "password", password)

        endpoint = "%s/users/%s/v1" % (USER_REGISTRY, username)
        status_code, content = self.http_put_json(endpoint, data)

        result = (status_code == 204, status_code, content)

        GlobalSettings.logger.exit(result)
        return result
