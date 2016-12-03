"""
Created on Dec 02, 2016

@copyright: IBM
"""

import logging

from com.ibm.isam.util.logger import Logger
from com.ibm.isam.util.restclient import RestClient
import com.ibm.isam.util.utils as Utils

class _GlobalSettings(RestClient):

    OVERRIDE_CONFIGS = "/iam/access/v8/override-configs"
    RUNTIME_TUNING = "/mga/runtime_tuning"
    SERVER_CONNECTION_LDAP = "/mga/server_connections/ldap/v1"
    SERVER_CONNECTION_WEB_SERVICE = "/mga/server_connections/ws/v1"
    TEMPLATE_FILES = "/mga/template_files"
    USER_REGISTRY = "/mga/user_registry"

    logger = Logger("GlobalSettings")

    def __init__(self, baseUrl, username, password, logLevel=logging.NOTSET):
        super(_GlobalSettings, self).__init__(baseUrl, username, password, logLevel)
        _GlobalSettings.logger.setLevel(logLevel)

    #
    # Advanced Configuration
    #

    def getAdvancedConfigurationByKey(self, key):
        methodName = "getAdvancedConfigurationByKey()"
        _GlobalSettings.logger.enterMethod(methodName)
        result = None

        keyEquals = "key equals " + str(key)
        content = self.getAdvancedConfigurations(filter=keyEquals)

        if content is not None and len(content) > 0:
            result = content[0]

        _GlobalSettings.logger.exitMethod(methodName, str(result))
        return result

    def getAdvancedConfigurations(self, sortBy=None, count=None, start=None, filter=None):
        methodName = "getAdvancedConfigurations()"
        _GlobalSettings.logger.enterMethod(methodName)
        result = None

        parameters = {}
        Utils.addOnStringValue(parameters, "sortBy", sortBy)
        Utils.addOnStringValue(parameters, "count", count)
        Utils.addOnStringValue(parameters, "start", start)
        Utils.addOnStringValue(parameters, "filter", filter)

        statusCode, content = self.httpGetJson(_GlobalSettings.OVERRIDE_CONFIGS, parameters=parameters)

        if statusCode == 200 and content is not None:
            result = content

        _GlobalSettings.logger.exitMethod(methodName, result)
        return result

    def updateAdvancedConfiguration(self, id, value, sensitive):
        methodName = "updateAdvancedConfiguration()"
        _GlobalSettings.logger.enterMethod(methodName)
        result = None

        jsonObj = {}
        Utils.addOnStringValue(jsonObj, "value", value)
        Utils.addOnValue(jsonObj, "sensitive", sensitive)

        endpoint = "%s/%s" % (_GlobalSettings.OVERRIDE_CONFIGS, str(id))
        statusCode, content = self.httpPutJson(endpoint, data=jsonObj)

        if statusCode == 204:
            result = True

        _GlobalSettings.logger.exitMethod(methodName, str(result))
        return result

    def updateAdvancedConfigurationByKey(self, key, value, sensitive):
        methodName = "updateAdvancedConfigurationByKey()"
        _GlobalSettings.logger.enterMethod(methodName)
        result = None

        content = self.getAdvancedConfigurationByKey(key)

        if content is not None:
            id = content.get("id", None)

            result = self.updateAdvancedConfiguration(id, value, sensitive)

        _GlobalSettings.logger.exitMethod(methodName, str(result))
        return result

    #
    # Runtime Parameters
    #

    def updateRuntimeTuningParameter(self, parameter, value):
        methodName = "updateRuntimeTuningParameter()"
        _GlobalSettings.logger.enterMethod(methodName)
        result = None

        jsonObj = {}
        Utils.addOnValue(jsonObj, "value", value)

        endpoint = "%s/%s/v1" % (_GlobalSettings.RUNTIME_TUNING, str(parameter))
        statusCode, content = self.httpPutJson(endpoint, data=jsonObj)

        if statusCode == 200:
            result = True if content is None else content

        _GlobalSettings.logger.exitMethod(methodName, str(result))
        return result

    #
    # Server Connections
    #

    # LDAP

    def createServerConnectionLdap(self, name=None, description=None, locked=None,
                                   connectionHostName=None, connectionBindDN=None,
                                   connectionBindPwd=None, connectionSslTruststore=None,
                                   connectionSslAuthKey=None, connectionHostPort=None,
                                   connectionSsl=None, connectTimeout=None, servers=None):
        methodName = "createServerConnectionLdap()"
        _GlobalSettings.logger.enterMethod(methodName)
        result = None

        connectionObj = {}
        Utils.addOnStringValue(connectionObj, "hostName", connectionHostName)
        Utils.addOnStringValue(connectionObj, "bindDN", connectionBindDN)
        Utils.addOnStringValue(connectionObj, "bindPwd", connectionBindPwd)
        Utils.addOnStringValue(connectionObj, "sslTruststore", connectionSslTruststore)
        Utils.addOnStringValue(connectionObj, "sslAuthKey", connectionSslAuthKey)
        Utils.addOnValue(connectionObj, "hostPort", connectionHostPort)
        Utils.addOnValue(connectionObj, "ssl", connectionSsl)

        connectionGlobalSettingsrObj = None
        if connectTimeout is not None:
            connectionGlobalSettingsrObj = {"connectTimeout": connectTimeout}

        jsonObj = {}
        Utils.addOnStringValue(jsonObj, "name", name)
        Utils.addOnStringValue(jsonObj, "description", description)
        Utils.addOnStringValue(jsonObj, "type", "ldap")
        Utils.addOnValue(jsonObj, "locked", locked)
        Utils.addOnValue(jsonObj, "connection", connectionObj)
        Utils.addOnValue(jsonObj, "connectionGlobalSettingsr", connectionGlobalSettingsrObj)
        Utils.addOnValue(jsonObj, "servers", servers)

        statusCode, content = self.httpPostJson(_GlobalSettings.SERVER_CONNECTION_LDAP, data=jsonObj)

        if statusCode == 201:
            result = True if content is None else content

        _GlobalSettings.logger.exitMethod(methodName, str(result))
        return result

    # Web Service

    def createServerConnectionWebService(self, name=None, description=None, locked=None,
                                         connectionUrl=None, connectionUser=None,
                                         connectionPassword=None, connectionSslTruststore=None,
                                         connectionSslAuthKey=None, connectionSsl=None):
        methodName = "createServerConnectionWebService()"
        _GlobalSettings.logger.enterMethod(methodName)
        result = None

        connectionObj = {}
        Utils.addOnStringValue(connectionObj, "url", connectionUrl)
        Utils.addOnStringValue(connectionObj, "user", connectionUser)
        Utils.addOnStringValue(connectionObj, "password", connectionPassword)
        Utils.addOnStringValue(connectionObj, "sslTruststore", connectionSslTruststore)
        Utils.addOnStringValue(connectionObj, "sslAuthKey", connectionSslAuthKey)
        Utils.addOnValue(connectionObj, "ssl", connectionSsl)

        jsonObj = {}
        Utils.addOnStringValue(jsonObj, "name", name)
        Utils.addOnStringValue(jsonObj, "description", description)
        Utils.addOnStringValue(jsonObj, "type", "ws")
        Utils.addOnValue(jsonObj, "locked", locked)
        Utils.addOnValue(jsonObj, "connection", connectionObj)

        statusCode, content = self.httpPostJson(_GlobalSettings.SERVER_CONNECTION_WEB_SERVICE, data=jsonObj)

        if statusCode == 201:
            result = True if content is None else content

        _GlobalSettings.logger.exitMethod(methodName, str(result))
        return result

    def getServerConnectionWebServiceByName(self, name):
        methodName = "getServerConnectionWebServiceByName()"
        _GlobalSettings.logger.enterMethod(methodName)
        result = None

        content = self.getWebServiceServerConnections()

        if content is not None:
            for index in range(len(content)):
                if content[index].get("name", "") == name:
                    result = content[index]

        _GlobalSettings.logger.exitMethod(methodName, str(result))
        return result

    def getServerConnectionWebServices(self):
        methodName = "getServerConnectionWebServices()"
        _GlobalSettings.logger.enterMethod(methodName)
        result = None

        statusCode, content = self.httpGetJson(_GlobalSettings.SERVER_CONNECTION_WEB_SERVICE)

        if statusCode == 200 and content is not None:
            result = content

        _GlobalSettings.logger.exitMethod(methodName, str(result))
        return result

    #
    # Template Files
    #

    # Directories

    def createTemplateFileDirectory(self, path, dirName):
        methodName = "createTemplateFileDirectory()"
        _GlobalSettings.logger.enterMethod(methodName)
        result = None

        jsonObj = {}
        Utils.addOnStringValue(jsonObj, "dir_name", dirName)
        Utils.addOnStringValue(jsonObj, "type", "dir")

        endpoint = "%s/%s" % (_GlobalSettings.TEMPLATE_FILES, str(path))
        statusCode, content = self.httpPostJson(endpoint, data=jsonObj)

        if statusCode == 200:
            result = True if content is None else content

        _GlobalSettings.logger.exitMethod(methodName, str(result))
        return result

    def getTemplateFileDirectory(self, path, recursive=None):
        methodName = "getTemplateFileDirectory()"
        _GlobalSettings.logger.enterMethod(methodName)
        result = None

        parameters = {}
        Utils.addOnValue(parameters, "recursive", recursive)

        endpoint = "%s/%s" % (_GlobalSettings.TEMPLATE_FILES, str(path))
        statusCode, content = self.httpGetJson(endpoint, parameters=parameters)

        if statusCode == 200 and content is not None:
            result = content if isinstance(content, list) else content.get("contents")

        _GlobalSettings.logger.exitMethod(methodName, str(result))
        return result

    # Files

    def createTemplateFile(self, path, fileName, content):
        methodName = "createTemplateFile()"
        _GlobalSettings.logger.enterMethod(methodName)
        result = None

        jsonObj = {}
        Utils.addOnStringValue(jsonObj, "file_name", fileName)
        Utils.addOnStringValue(jsonObj, "content", content)
        Utils.addOnStringValue(jsonObj, "type", "file")

        endpoint = "%s/%s" % (_GlobalSettings.TEMPLATE_FILES, str(path))
        statusCode, content = self.httpPostJson(endpoint, data=jsonObj)

        if statusCode == 200:
            result = True if content is None else content

        _GlobalSettings.logger.exitMethod(methodName, str(result))
        return result

    def deleteTemplateFile(self, path, fileName):
        methodName = "deleteTemplateFile()"
        _GlobalSettings.logger.enterMethod(methodName)
        result = None

        endpoint = "%s/%s/%s" % (_GlobalSettings.TEMPLATE_FILES, str(path), str(fileName))
        statusCode, content = self.httpDeleteJson(endpoint)

        if statusCode == 200:
            result = True if content is None else content

        _GlobalSettings.logger.exitMethod(methodName, str(result))
        return result

    def getTemplateFile(self, path, fileName):
        methodName = "getTemplateFile()"
        _GlobalSettings.logger.enterMethod(methodName)
        result = None

        endpoint = "%s/%s/%s" % (_GlobalSettings.TEMPLATE_FILES, str(path), str(fileName))
        statusCode, content = self.httpGetJson(endpoint)

        if statusCode == 200 and content is not None:
            result = content

        _GlobalSettings.logger.exitMethod(methodName, str(result))
        return result

    def importTemplateFile(self, path, fileName, filePath):
        methodName = "importTemplateFile()"
        _GlobalSettings.logger.enterMethod(methodName)
        result = None

        try:
            with open(filePath, 'rb') as template:
                files = {"file": template}

                endpoint = "%s/%s/%s" % (_GlobalSettings.TEMPLATE_FILES, str(path), str(fileName))
                statusCode, content = self.httpPostFile(endpoint, files=files)

                if statusCode == 200:
                    result = True if content is None else content
        except IOError as ioe:
            _GlobalSettings.logger.error(methodName, str(ioe))

        _GlobalSettings.logger.exitMethod(methodName, str(result))
        return result

    def updateTemplateFile(self, path, fileName, content=""):
        methodName = "updateTemplateFile()"
        _GlobalSettings.logger.enterMethod(methodName)
        result = None

        jsonObj = {}
        Utils.addOnStringValue(jsonObj, "content", content)
        Utils.addOnStringValue(jsonObj, "type", "file")

        endpoint = "%s/%s/%s" % (_GlobalSettings.TEMPLATE_FILES, str(path), str(fileName))
        statusCode, content = self.httpPutJson(endpoint, data=jsonObj)

        if statusCode == 200:
            result = True if content is None else content

        _GlobalSettings.logger.exitMethod(methodName, str(result))
        return result

    #
    # User Registry
    #

    # Users

    def updateUserRegistryUserPassword(self, username, password):
        methodName = "updateUserRegistryUserPassword()"
        _GlobalSettings.logger.enterMethod(methodName)
        result = None

        jsonObj = {}
        Utils.addOnStringValue(jsonObj, "password", password)

        endpoint = "%s/users/%s/v1" % (_GlobalSettings.USER_REGISTRY, str(username))
        statusCode, content = self.httpPutJson(endpoint, jsonObj)

        if statusCode == 204:
            result = True if content is None else content

        _GlobalSettings.logger.exitMethod(methodName, str(result))
        return result


class GlobalSettings9020(_GlobalSettings):

    logger = Logger("GlobalSettings9020")

    def __init__(self, baseUrl, username, password, logLevel=logging.NOTSET):
        super(GlobalSettings9020, self).__init__(baseUrl, username, password, logLevel)
        GlobalSettings9020.logger.setLevel(logLevel)
