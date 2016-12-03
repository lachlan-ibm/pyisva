"""
Created on Nov 23, 2016

@copyright: IBM
"""

import importlib
import logging


class Factory(object):

    VERSIONS = {
        "IBM Security Access Manager 9.0.2.0": "9020"
    }

    def __init__(self):
        self.__version = Factory.VERSIONS.get("IBM Security Access Manager 9.0.2.0")

    def getAccessControl(self, baseUrl, username, password, logLevel=logging.NOTSET):
        className = "AccessControl" + self.__version
        moduleName = "com.ibm.isam.pyconfig.access.accesscontrol"
        return self.__classLoader(moduleName, className)(baseUrl, username, password, logLevel)

    def getFirstSteps(self, baseUrl, username, password, logLevel=logging.NOTSET):
        className = "FirstSteps" + self.__version
        moduleName = "com.ibm.isam.pyconfig.firststeps.firststeps"
        return self.__classLoader(moduleName, className)(baseUrl, username, password, logLevel)

    def getSystemSettings(self, baseUrl, username, password, logLevel=logging.NOTSET):
        className = "SystemSettings" + self.__version
        moduleName = "com.ibm.isam.pyconfig.system.systemsettings"
        return self.__classLoader(moduleName, className)(baseUrl, username, password, logLevel)

    def getWebSettings(self, baseUrl, username, password, logLevel=logging.NOTSET):
        className = "WebSettings" + self.__version
        moduleName = "com.ibm.isam.pyconfig.web.websettings"
        return self.__classLoader(moduleName, className)(baseUrl, username, password, logLevel)

    def __classLoader(self, moduleName, className):
        return getattr(importlib.import_module(moduleName), className)
