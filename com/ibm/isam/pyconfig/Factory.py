"""
Created on Nov 23, 2016

@copyright: IBM
"""
import importlib, logging

class Factory(object):

    FIRST_STEPS = "com.ibm.isam.pyconfig.firststeps."
    SYSTEM_SETTINGS = "com.ibm.isam.pyconfig.systemsettings."
    WEB_SETTINGS = "com.ibm.isam.pyconfig.websettings."

    VERSIONS = {
        "IBM Security Access Manager 9.0.2.0": "9020"
    }

    def __init__(self, version=None):
        self.version = (version or Factory.VERSIONS.get("IBM Security Access Manager 9.0.2.0"))

    def classLoader(self, moduleName, className):
        return getattr(importlib.import_module(moduleName), className)

    def getFirstSteps(self, baseUrl, username, password, logLevel=logging.NOTSET):
        className = "FirstSteps" + self.version
        moduleName = Factory.FIRST_STEPS + className
        return self.classLoader(moduleName, className)(baseUrl, username, password, logLevel)

    def getSystemConfiguration(self, baseUrl, username, password, logLevel=logging.NOTSET):
        className = "Configuration" + self.version
        moduleName = Factory.SYSTEM_SETTINGS + "configuration." + className
        return self.classLoader(moduleName, className)(baseUrl, username, password, logLevel)

    def getSystemNetworkSettings(self, baseUrl, username, password, logLevel=logging.NOTSET):
        className = "NetworkSettings" + self.version
        moduleName = Factory.SYSTEM_SETTINGS + "networksettings." + className
        return self.classLoader(moduleName, className)(baseUrl, username, password, logLevel)

    def getSystemSecureSettings(self, baseUrl, username, password, logLevel=logging.NOTSET):
        className = "SecureSettings" + self.version
        moduleName = Factory.SYSTEM_SETTINGS + "securesettings." + className
        return self.classLoader(moduleName, className)(baseUrl, username, password, logLevel)

    def getSystemSystemSettings(self, baseUrl, username, password, logLevel=logging.NOTSET):
        className = "SystemSettings" + self.version
        moduleName = Factory.SYSTEM_SETTINGS + "systemsettings." + className
        return self.classLoader(moduleName, className)(baseUrl, username, password, logLevel)

    def getSystemUpdatesLicensing(self, baseUrl, username, password, logLevel=logging.NOTSET):
        className = "UpdatesLicensing" + self.version
        moduleName = Factory.SYSTEM_SETTINGS + "updateslicensing." + className
        return self.classLoader(moduleName, className)(baseUrl, username, password, logLevel)

    def getWebManage(self, baseUrl, username, password, logLevel=logging.NOTSET):
        className = "Manage" + self.version
        moduleName = Factory.WEB_SETTINGS + "manage." + className
        return self.classLoader(moduleName, className)(baseUrl, username, password, logLevel)
