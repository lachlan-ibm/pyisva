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


class _GlobalSettings(RestClient):

    logger = Logger("GlobalSettings")

    def __init__(self, base_url, username, password, log_level=logging.NOTSET):
        super(_GlobalSettings, self).__init__(
            base_url, username, password, log_level)
        _GlobalSettings.logger.set_level(log_level)

    #
    # Advanced Configuration
    #

    def get_advanced_configuration_by_key(self, key):
        method_name = "get_advanced_configuration_by_key()"
        _GlobalSettings.logger.enter_method(method_name)
        result = None

        filter = "key equals " + str(key)
        success, status_code, content = self.get_advanced_configurations(
            filter=filter)

        if success and content:
            result = (success, status_code, content[0])
        else:
            result = (success, status_code, content)

        _GlobalSettings.logger.exit_method(method_name, result)
        return result

    def get_advanced_configurations(
            self, sortBy=None, count=None, start=None, filter=None):
        method_name = "get_advanced_configurations()"
        _GlobalSettings.logger.enter_method(method_name)
        result = None

        parameters = {}
        Utils.add_string_value(parameters, "sortBy", sortBy)
        Utils.add_string_value(parameters, "count", count)
        Utils.add_string_value(parameters, "start", start)
        Utils.add_string_value(parameters, "filter", filter)

        status_code, content = self.http_get_json(
            OVERRIDE_CONFIGS, parameters=parameters)

        result = (status_code == 200, status_code, content)

        _GlobalSettings.logger.exit_method(method_name, result)
        return result

    def update_advanced_configuration(self, id, value=None, sensitive=None):
        method_name = "update_advanced_configuration()"
        _GlobalSettings.logger.enter_method(method_name)
        result = None

        data = {}
        Utils.add_string_value(data, "value", value)
        Utils.add_value(data, "sensitive", sensitive)

        endpoint = "%s/%s" % (OVERRIDE_CONFIGS, id)
        status_code, content = self.http_put_json(endpoint, data=data)

        result = (status_code == 204, status_code, content)

        _GlobalSettings.logger.exit_method(method_name, result)
        return result

    def update_advanced_configuration_by_key(
            self, key, value=None, sensitive=None):
        method_name = "update_advanced_configuration_by_key()"
        _GlobalSettings.logger.enter_method(method_name)
        result = None

        success, status_code, content = self.get_advanced_configuration_by_key(
            key)

        if success:
            id = content.get("id", None)
            result = self.update_advanced_configuration(id, value, sensitive)
        else:
            result = (success, status_code, content)

        _GlobalSettings.logger.exit_method(method_name, result)
        return result

    #
    # Runtime Parameters
    #

    def update_runtime_tuning_parameter(self, parameter, value=None):
        method_name = "update_runtime_tuning_parameter()"
        _GlobalSettings.logger.enter_method(method_name)
        result = None

        data = {}
        Utils.add_value(data, "value", value)

        endpoint = "%s/%s/v1" % (RUNTIME_TUNING, parameter)
        status_code, content = self.http_put_json(endpoint, data=data)

        result = (status_code == 200, status_code, content)

        _GlobalSettings.logger.exit_method(method_name, result)
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
        method_name = "create_server_connection_ldap()"
        _GlobalSettings.logger.enter_method(method_name)
        result = None

        connection_data = {}
        Utils.add_string_value(
            connection_data, "hostName", connection_host_name)
        Utils.add_string_value(connection_data, "bindDN", connection_bind_dn)
        Utils.add_string_value(connection_data, "bindPwd", connection_bind_pwd)
        Utils.add_string_value(
            connection_data, "sslTruststore", connection_ssl_truststore)
        Utils.add_string_value(
            connection_data, "sslAuthKey", connection_ssl_auth_key)
        Utils.add_value(connection_data, "hostPort", connection_host_port)
        Utils.add_value(connection_data, "ssl", connection_ssl)

        manager_data = None
        if connect_timeout:
            manager_data = {"connectTimeout": connectTimeout}

        data = {}
        Utils.add_string_value(data, "name", name)
        Utils.add_string_value(data, "description", description)
        Utils.add_string_value(data, "type", "ldap")
        Utils.add_value(data, "locked", locked)
        Utils.add_value(data, "connection", connection_data)
        Utils.add_value(data, "connectionManager", manager_data)
        Utils.add_value(data, "servers", servers)

        endpoint = SERVER_CONNECTION_LDAP + "/v1"
        status_code, content = self.http_post_json(endpoint, data=data)

        result = (status_code == 201, status_code, content)

        _GlobalSettings.logger.exit_method(method_name, result)
        return result

    def delete_server_connection_ldap(self, uuid):
        method_name = "delete_server_connection_ldap()"
        _GlobalSettings.logger.enter_method(method_name)
        result = None

        endpoint = "%s/%s/v1" % (SERVER_CONNECTION_LDAP, uuid)
        status_code, content = self.http_delete_json(endpoint)

        result = (status_code == 204, status_code, content)

        _GlobalSettings.logger.exit_method(method_name, result)
        return result

    def get_server_connection_ldap_by_name(self, name):
        method_name = "get_server_connection_ldap_by_name()"
        _GlobalSettings.logger.enter_method(method_name)
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

        _GlobalSettings.logger.exit_method(method_name, result)
        return result

    def get_server_connections_ldap(self):
        method_name = "get_server_connections_ldap()"
        _GlobalSettings.logger.enter_method(method_name)
        result = None

        endpoint = SERVER_CONNECTION_LDAP + "/v1"
        status_code, content = self.http_get_json(endpoint)

        result = (status_code == 200, status_code, content)

        _GlobalSettings.logger.exit_method(method_name, result)
        return result

    # Web Service

    def create_server_connection_web_service(
            self, name=None, description=None, locked=None, connection_url=None,
            connection_user=None, connection_password=None,
            connection_ssl_truststore=None, connection_ssl_auth_key=None,
            connection_ssl=None):
        method_name = "create_server_connection_web_service()"
        _GlobalSettings.logger.enter_method(method_name)
        result = None

        connection_data = {}
        Utils.add_string_value(connection_data, "url", connection_url)
        Utils.add_string_value(connection_data, "user", connection_user)
        Utils.add_string_value(connection_data, "password", connection_password)
        Utils.add_string_value(
            connection_data, "sslTruststore", connection_ssl_truststore)
        Utils.add_string_value(
            connection_data, "sslAuthKey", connection_ssl_auth_key)
        Utils.add_value(connection_data, "ssl", connection_ssl)

        data = {}
        Utils.add_string_value(data, "name", name)
        Utils.add_string_value(data, "description", description)
        Utils.add_string_value(data, "type", "ws")
        Utils.add_value(data, "locked", locked)
        Utils.add_value(data, "connection", connection_data)

        endpoint = SERVER_CONNECTION_WEB_SERVICE + "/v1"
        status_code, content = self.http_post_json(endpoint, data=data)

        result = (status_code == 201, status_code, content)

        _GlobalSettings.logger.exit_method(method_name, result)
        return result

    def get_server_connection_web_service_by_name(self, name):
        method_name = "get_server_connection_web_service_by_name()"
        _GlobalSettings.logger.enter_method(method_name)
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

        _GlobalSettings.logger.exit_method(method_name, result)
        return result

    def get_server_connections_web_service(self):
        method_name = "get_server_connections_web_service()"
        _GlobalSettings.logger.enter_method(method_name)
        result = None

        endpoint = SERVER_CONNECTION_WEB_SERVICE + "/v1"
        status_code, content = self.http_get_json(endpoint)

        result = (status_code == 200, status_code, content)

        _GlobalSettings.logger.exit_method(method_name, result)
        return result

    #
    # Template Files
    #

    # Directories

    def create_template_file_directory(self, path, dir_name=None):
        method_name = "create_template_file_directory()"
        _GlobalSettings.logger.enter_method(method_name)
        result = None

        data = {}
        Utils.add_string_value(data, "dir_name", dir_name)
        Utils.add_string_value(data, "type", "dir")

        endpoint = "%s/%s" % (TEMPLATE_FILES, path)
        status_code, content = self.http_post_json(endpoint, data=data)

        result = (status_code == 200, status_code, content)

        _GlobalSettings.logger.exit_method(method_name, result)
        return result

    def get_template_file_directory(self, path, recursive=None):
        method_name = "get_template_file_directory()"
        _GlobalSettings.logger.enter_method(method_name)
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

        _GlobalSettings.logger.exit_method(method_name, result)
        return result

    # Files

    def create_template_file(self, path, file_name=None, content=None):
        method_name = "create_template_file()"
        _GlobalSettings.logger.enter_method(method_name)
        result = None

        data = {}
        Utils.add_string_value(data, "file_name", file_name)
        Utils.add_string_value(data, "content", content)
        Utils.add_string_value(data, "type", "file")

        endpoint = "%s/%s" % (TEMPLATE_FILES, path)
        status_code, content = self.http_post_json(endpoint, data=data)

        result = (status_code == 200, status_code, content)

        _GlobalSettings.logger.exit_method(method_name, result)
        return result

    def delete_template_file(self, path, file_name):
        method_name = "delete_template_file()"
        _GlobalSettings.logger.enter_method(method_name)
        result = None

        endpoint = ("%s/%s/%s" % (TEMPLATE_FILES, path, file_name))
        status_code, content = self.http_delete_json(endpoint)

        result = (status_code == 200, status_code, content)

        _GlobalSettings.logger.exit_method(method_name, result)
        return result

    def get_template_file(self, path, file_name):
        method_name = "get_template_file()"
        _GlobalSettings.logger.enter_method(method_name)
        result = None

        endpoint = ("%s/%s/%s" % (TEMPLATE_FILES, path, file_name))
        status_code, content = self.http_get_json(endpoint)

        result = (status_code == 200, status_code, content)

        _GlobalSettings.logger.exit_method(method_name, result)
        return result

    def import_template_file(self, path, file_name, file_path):
        method_name = "import_template_file()"
        _GlobalSettings.logger.enter_method(method_name)
        result = None

        try:
            with open(file_path, 'rb') as template:
                files = {"file": template}

                endpoint = ("%s/%s/%s" % (TEMPLATE_FILES, path, file_name))
                status_code, content = self.http_post_file(
                    endpoint, files=files)

                result = (status_code == 200, status_code, content)
        except IOError as e:
            _GlobalSettings.logger.error(method_name, e)
            result = (False, None, None)

        _GlobalSettings.logger.exit_method(method_name, result)
        return result

    def update_template_file(self, path, file_name, content=None):
        method_name = "update_template_file()"
        _GlobalSettings.logger.enter_method(method_name)
        result = None

        data = {}
        Utils.add_string_value(data, "content", content)
        Utils.add_string_value(data, "type", "file")

        endpoint = ("%s/%s/%s" % (TEMPLATE_FILES, path, file_name))
        status_code, content = self.http_put_json(endpoint, data=data)

        result = (status_code == 200, status_code, content)

        _GlobalSettings.logger.exit_method(method_name, result)
        return result

    #
    # User Registry
    #

    # Users

    def update_user_registry_user_password(self, username, password=None):
        method_name = "update_user_registry_user_password()"
        _GlobalSettings.logger.enter_method(method_name)
        result = None

        data = {}
        Utils.add_string_value(data, "password", password)

        endpoint = "%s/users/%s/v1" % (USER_REGISTRY, username)
        status_code, content = self.http_put_json(endpoint, data)

        result = (status_code == 204, status_code, content)

        _GlobalSettings.logger.exit_method(method_name, result)
        return result


class GlobalSettings9020(_GlobalSettings):

    logger = Logger("GlobalSettings9020")

    def __init__(self, base_url, username, password, log_level=logging.NOTSET):
        super(GlobalSettings9020, self).__init__(
            base_url, username, password, log_level)
        GlobalSettings9020.logger.set_level(log_level)
