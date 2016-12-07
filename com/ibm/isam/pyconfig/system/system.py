""""
Created on Nov 22, 2016

@copyright: IBM
"""

import logging
import time

from com.ibm.isam.util.logger import Logger
from com.ibm.isam.util.restclient import RestClient
import com.ibm.isam.util.utils as Utils


class _SystemSettings(RestClient):

    ADMIN_CONFIG = "/core/admin_cfg"
    ADVANCED_PARAMETERS = "/core/adv_params"
    LMI = "/lmi"
    LMI_RESTART = "/restarts/restart_server"
    TIME_CONFIG = "/core/time_cfg"

    logger = Logger("SystemSettings")

    def __init__(self, baseUrl, username, password, logLevel=logging.NOTSET):
        super(_SystemSettings, self).__init__(baseUrl, username, password, logLevel)
        _SystemSettings.logger.setLevel(logLevel)

    #
    # Administrator Settings
    #

    def getAdministratorSettings(self):
        methodName = "getAdministratorSettings()"
        _SystemSettings.logger.enterMethod(methodName)
        result = None

        statusCode, content = self.httpGetJson(_SystemSettings.ADMIN_CONFIG)

        result = (statusCode == 200, statusCode, content)

        _SystemSettings.logger.exitMethod(methodName, str(result))
        return result

    def updateAdministratorSettings(self, oldPassword=None, newPassword=None, confirmPassword=None,
                                    minHeapSize=None, maxHeapSize=None, sessionTimeout=None,
                                    httpPort=None, httpsPort=None, minThreads=None, maxThreads=None,
                                    maxPoolSize=None, lmiDebuggingEnabled=None, consoleLogLevel=None,
                                    acceptClientCerts=None, validateClientCertIdentity=None,
                                    excludeCsrfChecking=None, enableSSLv3=None):
        methodName = "updateAdministratorSettings()"
        _SystemSettings.logger.enterMethod(methodName)
        result = None

        jsonObj = {}
        Utils.addOnStringValue(jsonObj, "oldPassword", oldPassword)
        Utils.addOnStringValue(jsonObj, "newPassword", newPassword)
        Utils.addOnStringValue(jsonObj, "confirmPassword", confirmPassword)
        Utils.addOnStringValue(jsonObj, "consoleLogLevel", consoleLogLevel)
        Utils.addOnStringValue(jsonObj, "excludeCsrfChecking", excludeCsrfChecking)
        Utils.addOnValue(jsonObj, "minHeapSize", minHeapSize)
        Utils.addOnValue(jsonObj, "maxHeapSize", maxHeapSize)
        Utils.addOnValue(jsonObj, "sessionTimeout", sessionTimeout)
        Utils.addOnValue(jsonObj, "httpPort", httpPort)
        Utils.addOnValue(jsonObj, "httpsPort", httpsPort)
        Utils.addOnValue(jsonObj, "minThreads", minThreads)
        Utils.addOnValue(jsonObj, "maxThreads", maxThreads)
        Utils.addOnValue(jsonObj, "maxPoolSize", maxPoolSize)
        Utils.addOnValue(jsonObj, "lmiDebuggingEnabled", lmiDebuggingEnabled)
        Utils.addOnValue(jsonObj, "acceptClientCerts", acceptClientCerts)
        Utils.addOnValue(jsonObj, "validateClientCertIdentity", validateClientCertIdentity)
        Utils.addOnValue(jsonObj, "enableSSLv3", enableSSLv3)

        statusCode, content = self.httpPutJson(_SystemSettings.ADMIN_CONFIG, jsonObj)

        result = (statusCode == 200, statusCode, content)

        _SystemSettings.logger.exitMethod(methodName, str(result))
        return result

    def updateAdministratorPassword(self, password):
        methodName = "updateAdministratorPassword()"
        _SystemSettings.logger.enterMethod(methodName)
        result = None

        success, statusCode, content = self.getAdministratorSettings()

        if success:
            sessionTimeout = content.get("sessionTimeout", -1)

            if sessionTimeout > 0:
                result = self.updateAdministratorSettings(sessionTimeout=sessionTimeout,
                                                          oldPassword=self._password,
                                                          newPassword=password,
                                                          confirmPassword=password)
            else:
                _SystemSettings.logger.error(methodName, "An invalid session timeout was retrieved.")
                result = (False, statusCode, content)
        else:
            result = (success, statusCode, content)

        _SystemSettings.logger.exitMethod(methodName, str(result))
        return result

    #
    # Advanced Tuning Parameters
    #

    def createAdvancedTuningParameter(self, key=None, value=None, comment=None):
        methodName = "createAdvancedTuningParameter()"
        _SystemSettings.logger.enterMethod(methodName)
        result = None

        jsonObj = {}
        Utils.addOnStringValue(jsonObj, "key", key)
        Utils.addOnStringValue(jsonObj, "value", value)
        Utils.addOnStringValue(jsonObj, "comment", comment)
        Utils.addOnValue(jsonObj, "_isNew", True)

        statusCode, content = self.httpPostJson(_SystemSettings.ADVANCED_PARAMETERS, jsonObj)

        result = (statusCode == 201, statusCode, content)

        _SystemSettings.logger.exitMethod(methodName, str(result))
        return result

    def getAdvancedTuningParameters(self):
        methodName = "getAdvancedTuningParameters()"
        _SystemSettings.logger.enterMethod(methodName)
        result = None

        statusCode, content = self.httpGetJson(_SystemSettings.ADVANCED_PARAMETERS)

        if statusCode == 200:
            result = (True, statusCode, content.get("tuningParameters", []))
        else:
            result = (False, statusCode, content)

        _SystemSettings.logger.exitMethod(methodName, str(result))
        return result

    def getAdvancedTuningParameter(self, key):
        methodName = "getAdvancedTuningParameter()"
        _SystemSettings.logger.enterMethod(methodName)
        result = None

        success, statusCode, content = self.getAdvancedTuningParameters()

        if success:
            for index in range(len(content)):
                if content[index].get("key", "") == key:
                    result = (success, statusCode, content[index])

            if result is None:
                result = (False, 404, content)
        else:
            result = (success, statusCode, content)

        _SystemSettings.logger.exitMethod(methodName, str(result))
        return result

    def getAdvancedTuningParameterValue(self, key):
        methodName = "getAdvancedTuningParameterValue()"
        _SystemSettings.logger.enterMethod(methodName)
        result = default

        success, statusCode, content = self.getAdvancedTuningParameter(key)

        if success:
            result = (success, statusCode, content.get("value"))
        else:
            result = (success, statusCode, content)

        _SystemSettings.logger.exitMethod(methodName, str(result))
        return result

    #
    # Date/Time
    #

    def updateDateTime(self, enableNtp=True, ntpServers=None, timeZone=None,
                       dateTime="0000-00-00 00:00:00"):
        methodName = "updateDateTime()"
        _SystemSettings.logger.enterMethod(methodName)
        result = None

        jsonObj = {}
        Utils.addOnStringValue(jsonObj, "dateTime", dateTime)
        Utils.addOnStringValue(jsonObj, "ntpServers", ntpServers)
        Utils.addOnStringValue(jsonObj, "timeZone", timeZone)
        Utils.addOnValue(jsonObj, "enableNtp", enableNtp)

        statusCode, content = self.httpPutJson(_SystemSettings.TIME_CONFIG, jsonObj)

        result = (statusCode == 200, statusCode, content)

        _SystemSettings.logger.exitMethod(methodName, str(result))
        return result

    #
    # Restart or Shutdown
    #

    def getLmiStatus(self):
        methodName = "getLmiStatus()"
        _SystemSettings.logger.enterMethod(methodName)
        result = None

        statusCode, content = self.httpGetJson(_SystemSettings.LMI)

        result = (statusCode == 200, statusCode, content)

        _SystemSettings.logger.exitMethod(methodName, str(result))
        return result

    def restartLmi(self):
        methodName = "restartLmi()"
        _SystemSettings.logger.enterMethod(methodName)
        result = None

        lastStartTime = -1

        success, statusCode, content = self.getLmiStatus()

        if success:
            lastStartTime = content[0].get("start_time", -1)

        if lastStartTime > 0:
            statusCode, content = self.httpPostJson(_SystemSettings.LMI_RESTART)

            if statusCode == 200 and content.get("restart", False) == True:
                _SystemSettings.logger.log(methodName, "Waiting for LMI to restart...")
                self._waitForLmi(lastStartTime)
                result = (True, statusCode, content)
            else:
                result = (False, statusCode, content)
        else:
            message = "An invalid start time was retrieved [%s]" % str(lastStartTime)
            _SystemSettings.logger.error(methodName, message)
            result = (False, statusCode, content)

        _SystemSettings.logger.exitMethod(methodName, str(result))
        return result

    def _waitForLmi(self, lastStartTime, sleepInterval=3):
        methodName = "_waitForLmi()"
        _SystemSettings.logger.enterMethod(methodName)

        if lastStartTime > 0:
            restartTime = lastStartTime

            while (restartTime <= 0 or restartTime == lastStartTime):
                message = "Waiting for LMI to restart. lastStartTime [%s] restartTime [%s]" \
                          % (lastStartTime, restartTime)
                _SystemSettings.logger.trace(methodName, message)
                time.sleep(sleepInterval)

                try:
                    success, statusCode, content = self.getLmiStatus()

                    if success:
                        restartTime = content[0].get("start_time", -1)
                except:
                    restartTime = -1

            time.sleep(sleepInterval)
        else:
            message = "Invalid last start time [%s]" % str(lastStartTime)
            _SystemSettings.logger.error(methodName, message)

        _SystemSettings.logger.exitMethod(methodName)


class SystemSettings9020(_SystemSettings):

    logger = Logger("SystemSettings9020")

    def __init__(self, baseUrl, username, password, logLevel=logging.NOTSET):
        super(SystemSettings9020, self).__init__(baseUrl, username, password, logLevel)
        SystemSettings9020.logger.setLevel(logLevel)
