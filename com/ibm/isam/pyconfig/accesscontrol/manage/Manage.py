"""
Created on Nov 22, 2016

@copyright: IBM
"""
from com.ibm.isam.pyconfig.Factory import Factory
from com.ibm.isam.util.RestClient import RestClient
from com.ibm.isam.util.Logger import Logger
import com.ibm.isam.util.Utils as Utils
import abc, logging

class Manage(RestClient):
    __metaclass__ = abc.ABCMeta

    MMFA_CONFIG = "/iam/access/v8/mmfa-config"
    OVERRIDE_CONFIGS = "/iam/access/v8/override-configs"
    RUNTIME_TUNING = "/mga/runtime_tuning"
    SCIM_CONFIGURATION = "/mga/scim/configuration"
    SCIM_CONFIGURATION_ISAM = "/mga/scim/configuration/urn:ietf:params:scim:schemas:extension:isam:1.0:User"
    SERVER_CONNECTION_LDAP = "/mga/server_connections/ldap/v1"
    SERVER_CONNECTION_WEB_SERVICE = "/mga/server_connections/ws/v1"
    TEMPLATE_FILES = "/mga/template_files"

    logger = Logger("Manage")

    def __init__(self, baseUrl, username, password, logLevel=logging.NOTSET):
        super(Manage, self).__init__(baseUrl, username, password, logLevel)
        Manage.logger.setLevel(logLevel)

    @abc.abstractmethod
    def getIsamVersion(self):
        pass

    #
    # Advanced Configuration
    #

    # Configuration

    def getAdvancedConfigurationByKey(self, key):
        methodName = "getAdvancedConfigurationByKey()"
        Manage.logger.enterMethod(methodName)
        result = None

        keyEquals = "key equals %s" % str(key)
        configurations = self.getAdvancedConfigurations(filter=keyEquals)

        if configurations is not None and len(configurations) > 0:
            result = configurations[0]

        Manage.logger.exitMethod(methodName, str(result))
        return result

    def getAdvancedConfigurations(self, sortBy=None, count=None, start=None, filter=None):
        methodName = "getAdvancedConfigurations()"
        Manage.logger.enterMethod(methodName)
        result = None

        parameters = {}
        Utils.addOnStringValue(parameters, "sortBy", sortBy)
        Utils.addOnStringValue(parameters, "count", count)
        Utils.addOnStringValue(parameters, "start", start)
        Utils.addOnStringValue(parameters, "filter", filter)

        statusCode, content = self.httpGetJson(Manage.OVERRIDE_CONFIGS, parameters=parameters)

        if statusCode == 200 and content is not None:
            result = content

        Manage.logger.exitMethod(methodName, result)
        return result

    def updateAdvancedConfiguration(self, id, value, sensitive):
        methodName = "updateAdvancedConfiguration()"
        Manage.logger.enterMethod(methodName)
        result = None

        jsonObj = {}
        Utils.addOnStringValue(jsonObj, "value", value)
        Utils.addOnValue(jsonObj, "sensitive", sensitive)

        endpoint = "%s/%s" % (Manage.OVERRIDE_CONFIGS, str(id))
        statusCode, content = self.httpPutJson(endpoint, jsonObj)

        if statusCode == 204:
            result = True if content is None else content

        Manage.logger.exitMethod(methodName, str(result))
        return result

    def updateAdvancedConfigurationByKey(self, key, value, sensitive):
        methodName = "updateAdvancedConfigurationByKey()"
        Manage.logger.enterMethod(methodName)
        result = None

        configuration = self.getAdvancedConfigurationByKey(key)

        if configuration is not None:
            id = configuration.get("id", None)

            result = self.updateAdvancedConfiguration(id, value, sensitive)

        Manage.logger.exitMethod(methodName, str(result))
        return result

    #
    # Configure SCIM
    #

    def getScimConfiguration(self):
        methodName = "getScimConfiguration()"
        Manage.logger.enterMethod(methodName)
        result = None

        statusCode, content = self.httpGetJson(Manage.SCIM_CONFIGURATION)

        if statusCode == 200 and content is not None:
            result = content

        Manage.logger.exitMethod(methodName, str(result))
        return result

    def updateScimConfiguration(self, jsonObj):
        methodName = "updateScimConfiguration()"
        Manage.logger.enterMethod(methodName)
        result = None

        statusCode, content = self.httpPutJson(Manage.SCIM_CONFIGURATION, jsonObj)

        if statusCode == 200:
            result = True if content is None else content

        Manage.logger.exitMethod(methodName, str(result))
        return result

    def updateScimConfigurationUserIsam(self, ldapConnection=None, isamDomain=None, updateNativeUsers=None):
        methodName = "updateScimConfigurationUserIsam()"
        Manage.logger.enterMethod(methodName)
        result = None

        jsonObj = {}
        Utils.addOnStringValue(jsonObj, "ldap_connection", ldapConnection)
        Utils.addOnStringValue(jsonObj, "isam_domain", isamDomain)
        Utils.addOnValue(jsonObj, "update_native_users", updateNativeUsers)

        statusCode, content = self.httpPutJson(Manage.SCIM_CONFIGURATION_ISAM, jsonObj)

        if statusCode == 200:
            result = True if content is None else content

        Manage.logger.exitMethod(methodName, str(result))
        return result

    #
    # Mobile Multi Factor Authentication
    #

    # Endpoint Configuration

    def configureMmfaEndpoints(self, clientId=None, hostname=None, junction=None, options=None, port=None):
        methodName = "configureMmfaEndpoints()"
        Manage.logger.enterMethod(methodName)
        result = None

        jsonObj = {}
        Utils.addOnStringValue(jsonObj, "client_id", clientId)
        Utils.addOnStringValue(jsonObj, "hostname", hostname)
        Utils.addOnStringValue(jsonObj, "junction", junction)
        Utils.addOnStringValue(jsonObj, "options", options)
        Utils.addOnValue(jsonObj, "port", port)

        statusCode, content = self.httpPostJson(Manage.MMFA_CONFIG, jsonObj)

        if statusCode == 204:
            result = True if content is None else content

        Manage.logger.exitMethod(methodName, str(result))
        return result

    #
    # Runtime Parameters
    #

    def updateTuningParameter(self, parameter, value):
        methodName = "updateTuningParameter()"
        Manage.logger.enterMethod(methodName)
        result = None

        jsonObj = {}
        Utils.addOnValue(jsonObj, "value", value)

        endpoint = "%s/%s/v1" % (Manage.RUNTIME_TUNING, str(parameter))
        statusCode, content = self.httpPutJson(endpoint, jsonObj)

        if statusCode == 200:
            result = True if content is None else content

        Manage.logger.exitMethod(methodName, str(result))
        return result

    #
    # Runtime Template Files
    #

    # Directories

    def createTemplateFileDirectory(self, path, dirName):
        methodName = "createTemplateFileDirectory()"
        Manage.logger.enterMethod(methodName)
        result = None

        jsonObj = {}
        Utils.addOnStringValue(jsonObj, "dir_name", dirName)
        Utils.addOnStringValue(jsonObj, "type", "dir")

        endpoint = "%s/%s" % (Manage.TEMPLATE_FILES, str(path))
        statusCode, content = self.httpPostJson(endpoint, jsonObj)

        if statusCode == 200:
            result = True if content is None else content

        Manage.logger.exitMethod(methodName, str(result))
        return result

    def getTemplateFileDirectory(self, path, recursive=None):
        methodName = "getTemplateFileDirectory()"
        Manage.logger.enterMethod(methodName)
        result = None

        parameters = {}
        Utils.addOnValue(parameters, "recursive", recursive)

        endpoint = "%s/%s" % (Manage.TEMPLATE_FILES, str(path))
        statusCode, content = self.httpGetJson(endpoint, parameters=parameters)

        if statusCode == 200 and content is not None:
            result = content if isinstance(content, list) else content.get("contents")

        Manage.logger.exitMethod(methodName, str(result))
        return result

    # Files

    def createTemplateFile(self, path, fileName, content):
        methodName = "createTemplateFile()"
        Manage.logger.enterMethod(methodName)
        result = None

        jsonObj = {}
        Utils.addOnStringValue(jsonObj, "file_name", fileName)
        Utils.addOnStringValue(jsonObj, "content", content)
        Utils.addOnStringValue(jsonObj, "type", "file")

        endpoint = "%s/%s" % (Manage.TEMPLATE_FILES, str(path))
        statusCode, content = self.httpPostJson(endpoint, jsonObj)

        if statusCode == 200:
            result = True if content is None else content

        Manage.logger.exitMethod(methodName, str(result))
        return result

    def deleteTemplateFile(self, path, fileName):
        methodName = "getTemplateFile()"
        Manage.logger.enterMethod(methodName)
        result = None

        endpoint = "%s/%s/%s" % (Manage.TEMPLATE_FILES, str(path), str(fileName))
        statusCode, content = self.httpDeleteJson(endpoint)

        if statusCode == 200:
            result = True if content is None else content

        Manage.logger.exitMethod(methodName, str(result))
        return result

    def getTemplateFile(self, path, fileName):
        methodName = "getTemplateFile()"
        Manage.logger.enterMethod(methodName)
        result = None

        endpoint = "%s/%s/%s" % (Manage.TEMPLATE_FILES, str(path), str(fileName))
        statusCode, content = self.httpGetJson(endpoint)

        if statusCode == 200 and content is not None:
            result = content

        Manage.logger.exitMethod(methodName, str(result))
        return result

    def importTemplateFile(self, path, fileName, filePath):
        methodName = "updateTemplateFile()"
        Manage.logger.enterMethod(methodName)
        result = None

        try:
            with open(filePath, 'rb') as template:
                files = {"file": template}

                endpoint = "%s/%s/%s" % (Manage.TEMPLATE_FILES, str(path), str(fileName))
                statusCode, content = self.httpPostFile(endpoint, files=files)

                if statusCode == 200:
                    result = True if content is None else content
        except IOError, e:
            Manage.logger.error(methodName, str(e))

        Manage.logger.exitMethod(methodName, str(result))
        return result

    def updateTemplateFile(self, path, fileName, content=""):
        methodName = "updateTemplateFile()"
        Manage.logger.enterMethod(methodName)
        result = None

        jsonObj = {}
        Utils.addOnStringValue(jsonObj, "content", content)
        Utils.addOnStringValue(jsonObj, "type", "file")

        endpoint = "%s/%s/%s" % (Manage.TEMPLATE_FILES, str(path), str(fileName))
        statusCode, content = self.httpPutJson(endpoint, jsonObj)

        if statusCode == 200:
            result = True if content is None else content

        Manage.logger.exitMethod(methodName, str(result))
        return result

    #
    # Server Connections
    #

    # LDAP

    def createLdapServerConnection(self, name=None, description=None, locked=None, connectionHostName=None, \
            connectionBindDN=None, connectionBindPwd=None, connectionSslTruststore=None, connectionSslAuthKey=None, \
            connectionHostPort=None, connectionSsl=None, connectTimeout=None, servers=None):
        methodName = "createLdapServerConnection()"
        Manage.logger.enterMethod(methodName)
        result = None

        connectionObj = {}
        Utils.addOnStringValue(connectionObj, "hostName", connectionHostName)
        Utils.addOnStringValue(connectionObj, "bindDN", connectionBindDN)
        Utils.addOnStringValue(connectionObj, "bindPwd", connectionBindPwd)
        Utils.addOnStringValue(connectionObj, "sslTruststore", connectionSslTruststore)
        Utils.addOnStringValue(connectionObj, "sslAuthKey", connectionSslAuthKey)
        Utils.addOnValue(connectionObj, "hostPort", connectionHostPort)
        Utils.addOnValue(connectionObj, "ssl", connectionSsl)

        connectionManagerObj = None
        if connectTimeout is not None:
            connectionManagerObj = {"connectTimeout": connectTimeout}

        jsonObj = {}
        Utils.addOnStringValue(jsonObj, "name", name)
        Utils.addOnStringValue(jsonObj, "description", description)
        Utils.addOnStringValue(jsonObj, "type", "ldap")
        Utils.addOnValue(jsonObj, "locked", locked)
        Utils.addOnValue(jsonObj, "connection", connectionObj)
        Utils.addOnValue(jsonObj, "connectionManager", connectionManagerObj)
        Utils.addOnValue(jsonObj, "servers", servers)

        statusCode, content = self.httpPostJson(Manage.SERVER_CONNECTION_LDAP, jsonObj)

        if statusCode == 201:
            result = True if content is None else content

        Manage.logger.exitMethod(methodName, str(result))
        return result

    # Web Service

    def createWebServiceServerConnection(self, name=None, description=None, locked=None, connectionUrl=None, \
            connectionUser=None, connectionPassword=None, connectionSslTruststore=None, connectionSslAuthKey=None, \
            connectionSsl=None):
        methodName = "createWebServiceServerConnection()"
        Manage.logger.enterMethod(methodName)
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

        statusCode, content = self.httpPostJson(Manage.SERVER_CONNECTION_WEB_SERVICE, jsonObj)

        if statusCode == 201:
            result = True if content is None else content

        Manage.logger.exitMethod(methodName, str(result))
        return result

    def getWebServiceServerConnectionByName(self, name):
        methodName = "getWebServiceServerConnectionByName()"
        Manage.logger.enterMethod(methodName)
        result = None

        connections = self.getWebServiceServerConnections()

        if connections is not None:
            for index in range(len(connections)):
                if connections[index].get("name", "") == name:
                    result = connections[index]

        Manage.logger.exitMethod(methodName, str(result))
        return result

    def getWebServiceServerConnections(self):
        methodName = "getWebServiceServerConnections()"
        Manage.logger.enterMethod(methodName)
        result = None

        statusCode, content = self.httpGetJson(Manage.SERVER_CONNECTION_WEB_SERVICE)

        if statusCode == 200 and content is not None:
            result = content

        Manage.logger.exitMethod(methodName, str(result))
        return result
