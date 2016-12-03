"""
Created on Nov 22, 2016

@copyright: IBM
"""

import logging

from com.ibm.isam.util.logger import Logger
from com.ibm.isam.util.restclient import RestClient
import com.ibm.isam.util.utils as Utils


class _Manage(RestClient):

    MMFA_CONFIG = "/iam/access/v8/mmfa-config"
    SCIM_CONFIGURATION = "/mga/scim/configuration"
    SCIM_CONFIGURATION_ISAM = "/mga/scim/configuration/urn:ietf:params:scim:schemas:extension:isam:1.0:User"

    logger = Logger("Manage")

    def __init__(self, baseUrl, username, password, logLevel=logging.NOTSET):
        super(_Manage, self).__init__(baseUrl, username, password, logLevel)
        _Manage.logger.setLevel(logLevel)

    #
    # SCIM Configuration
    #

    # General

    def getScimConfiguration(self):
        methodName = "getScimConfiguration()"
        _Manage.logger.enterMethod(methodName)
        result = None

        statusCode, content = self.httpGetJson(_Manage.SCIM_CONFIGURATION)

        if statusCode == 200 and content is not None:
            result = content

        _Manage.logger.exitMethod(methodName, str(result))
        return result

    def updateScimConfiguration(self, jsonObj):
        methodName = "updateScimConfiguration()"
        _Manage.logger.enterMethod(methodName)
        result = None

        statusCode, content = self.httpPutJson(_Manage.SCIM_CONFIGURATION, data=jsonObj)

        if statusCode == 200:
            result = True if content is None else content

        _Manage.logger.exitMethod(methodName, str(result))
        return result

    # ISAM User

    def updateScimConfigurationIsamUser(self, ldapConnection=None, isamDomain=None, updateNativeUsers=None):
        methodName = "updateScimConfigurationIsamUser()"
        _Manage.logger.enterMethod(methodName)
        result = None

        jsonObj = {}
        Utils.addOnStringValue(jsonObj, "ldap_connection", ldapConnection)
        Utils.addOnStringValue(jsonObj, "isam_domain", isamDomain)
        Utils.addOnValue(jsonObj, "update_native_users", updateNativeUsers)

        statusCode, content = self.httpPutJson(_Manage.SCIM_CONFIGURATION_ISAM, data=jsonObj)

        if statusCode == 200:
            result = True if content is None else content

        _Manage.logger.exitMethod(methodName, str(result))
        return result

    #
    # MMFA Configuration
    #

    def updateMmfaConfiguration(self, clientId=None, hostname=None, junction=None, options=None, port=None):
        methodName = "updateMmfaConfiguration()"
        _Manage.logger.enterMethod(methodName)
        result = None

        jsonObj = {}
        Utils.addOnStringValue(jsonObj, "client_id", clientId)
        Utils.addOnStringValue(jsonObj, "hostname", hostname)
        Utils.addOnStringValue(jsonObj, "junction", junction)
        Utils.addOnStringValue(jsonObj, "options", options)
        Utils.addOnValue(jsonObj, "port", port)

        statusCode, content = self.httpPostJson(_Manage.MMFA_CONFIG, data=jsonObj)

        if statusCode == 204:
            result = True

        _Manage.logger.exitMethod(methodName, str(result))
        return result


class Manage9020(_Manage):

    logger = Logger("Manage9020")

    def __init__(self, baseUrl, username, password, logLevel=logging.NOTSET):
        super(Manage9020, self).__init__(baseUrl, username, password, logLevel)
        Manage9020.logger.setLevel(logLevel)
