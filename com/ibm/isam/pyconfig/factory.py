"""
Created on Nov 23, 2016

@copyright: IBM
"""

import importlib
import logging

from com.ibm.isam.util.restclient import RestClient


class Factory(object):

    VERSIONS = {
        "IBM Security Access Manager 9.0.2.0": "9020"
    }

    def __init__(self, baseUrl, username, password, logLevel=logging.NOTSET):
        self.__baseUrl = baseUrl
        self.__username = username
        self.__password = password
        self.__logLevel = logLevel
        self.__version = None

        self.__discoverVersion()
        self.__getVersion()

    def getAccessControl(self):
        className = "AccessControl" + self.__getVersion()
        moduleName = "com.ibm.isam.pyconfig.access.accesscontrol"
        return self.__classLoader(moduleName, className)(self.__baseUrl, self.__username,
                                                         self.__password, self.__logLevel)

    def getFirstSteps(self):
        className = "FirstSteps" + self.__getVersion()
        moduleName = "com.ibm.isam.pyconfig.firststeps.firststeps"
        return self.__classLoader(moduleName, className)(self.__baseUrl, self.__username,
                                                         self.__password, self.__logLevel)

    def getSystemSettings(self):
        className = "SystemSettings" + self.__getVersion()
        moduleName = "com.ibm.isam.pyconfig.system.systemsettings"
        return self.__classLoader(moduleName, className)(self.__baseUrl, self.__username,
                                                         self.__password, self.__logLevel)

    def getWebSettings(self):
        className = "WebSettings" + self.__getVersion()
        moduleName = "com.ibm.isam.pyconfig.web.websettings"
        return self.__classLoader(moduleName, className)(self.__baseUrl, self.__username,
                                                         self.__password, self.__logLevel)

    def setPassword(self, password):
        self.__password = password

    def __classLoader(self, moduleName, className):
        return getattr(importlib.import_module(moduleName), className)

    def __discoverVersion(self):
        client = RestClient(self.__baseUrl, self.__username, self.__password, self.__logLevel)
        statusCode, content = client.httpGetJson("/firmware_settings")

        if statusCode == 200:
            for index in range(len(content)):
                if content[index].get("active", False):
                    self.__version = content[index].get("firmware_version")
        elif statusCode == 403:
            raise AuthenticationError("Authentication failed. Check administrator credentials.")

        if self.__version is None:
            raise Exception("Failed to retrieve the ISAM firmware version.")

    def __getVersion(self):
        if self.__version in Factory.VERSIONS:
            return Factory.VERSIONS.get(self.__version)
        else:
            raise Exception(self.__version + " is not supported.")


class AuthenticationError(Exception):
    pass
