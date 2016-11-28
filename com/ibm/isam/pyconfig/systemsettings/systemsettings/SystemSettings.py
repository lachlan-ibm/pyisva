"""
Created on Nov 22, 2016

@copyright: IBM
"""
from com.ibm.isam.util.RestClient import RestClient
from com.ibm.isam.util.Logger import Logger
import com.ibm.isam.util.Utils as Utils
import abc, logging, time

class SystemSettings(RestClient):
    __metaclass__ = abc.ABCMeta

    ADMIN_CONFIG = "/core/admin_cfg"
    ADVANCED_PARAMETERS = "/core/adv_params"
    LMI = "/lmi"
    LMI_RESTART = "/restarts/restart_server"
    TIME_CONFIG = "/core/time_cfg"

    logger = Logger("SystemSettings")

    def __init__(self, baseUrl, username, password, logLevel=logging.NOTSET):
        super(SystemSettings, self).__init__(baseUrl, username, password, logLevel)
        SystemSettings.logger.setLevel(logLevel)

    @abc.abstractmethod
    def getIsamVersion(self):
        pass

    #
    # Administrator Settings
    #

    def getAdministratorSettings(self):
        methodName = "getAdministratorSettings()"
        SystemSettings.logger.enterMethod(methodName)
        result = None

        statusCode, content = self.httpGetJson(SystemSettings.ADMIN_CONFIG)

        if statusCode == 200 and content is not None:
            result = content

        SystemSettings.logger.exitMethod(methodName, str(result))
        return result

    def updateAdministratorSettings(self, oldPassword=None, newPassword=None, confirmPassword=None, \
            minHeapSize=None, maxHeapSize=None, sessionTimeout=None, httpPort=None, httpsPort=None, \
            minThreads=None, maxThreads=None, maxPoolSize=None, lmiDebuggingEnabled=None, consoleLogLevel=None, \
            acceptClientCerts=None, validateClientCertIdentity=None, excludeCsrfChecking=None, enableSSLv3=None):
        methodName = "updateAdministratorSettings()"
        SystemSettings.logger.enterMethod(methodName)
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

        statusCode, content = self.httpPutJson(SystemSettings.ADMIN_CONFIG, jsonObj)

        if statusCode == 200:
            result = True if content is None else content

        SystemSettings.logger.exitMethod(methodName, str(result))
        return result

    def updateAdministratorPassword(self, newPassword):
        methodName = "updateAdministratorPassword()"
        SystemSettings.logger.enterMethod(methodName)
        result = None

        content = self.getAdministratorSettings()

        if content is not None:
            sessionTimeout = content.get("sessionTimeout", -1)

            if sessionTimeout > 0:
                if self.updateAdministratorSettings(sessionTimeout=sessionTimeout, oldPassword=self.password, newPassword=newPassword, confirmPassword=newPassword):
                    result = True
            else:
                SystemSettings.logger.error(methodName, "A valid session timeout was not returned.")
        else:
            oldPassword = self.password
            self.password = newPassword

            if self.getAdministratorSettings():
                SystemSettings.logger.log(methodName, "The password was already configured.")
                result = True
            else:
                self.password = oldPassword

        SystemSettings.logger.exitMethod(methodName, str(result))
        return result

    #
    # Advanced Tuning Parameters
    #

    def getAdvancedTuningParameters(self):
        methodName = "getAdvancedTuningParameters()"
        SystemSettings.logger.enterMethod(methodName)
        result = None

        statusCode, content = self.httpGetJson(SystemSettings.ADVANCED_PARAMETERS)

        if statusCode == 200 and content is not None:
            result = content.get("tuningParameters", [])

        SystemSettings.logger.exitMethod(methodName, str(result))
        return result

    def getAdvancedTuningParameter(self, key, default=None):
        methodName = "getAdvancedTuningParameter()"
        SystemSettings.logger.enterMethod(methodName)
        result = None

        parameters = self.getAdvancedTuningParameters()

        if parameters is not None:
            for index in range(len(parameters)):
                if parameters[index].get("key", "") == key:
                    result = parameters[index].get("value", default)

        SystemSettings.logger.exitMethod(methodName, str(result))
        return result

    #
    # Date and Time Settings
    #

    def updateDateTimeSettings(self, enableNtp=True, dateTime="0000-00-00 00:00:00", ntpServers="pool.ntp.org", timeZone="Australia/Brisbane"):
        methodName = "updateDateTimeSettings()"
        SystemSettings.logger.enterMethod(methodName)
        result = None

        jsonObj = {}
        Utils.addOnStringValue(jsonObj, "dateTime", dateTime)
        Utils.addOnStringValue(jsonObj, "ntpServers", ntpServers)
        Utils.addOnStringValue(jsonObj, "timeZone", timeZone)
        Utils.addOnValue(jsonObj, "enableNtp", enableNtp)

        statusCode, content = self.httpPutJson(SystemSettings.TIME_CONFIG, jsonObj)

        if statusCode == 200:
            result = True if content is None else content

        SystemSettings.logger.exitMethod(methodName, str(result))
        return result

    #
    # Restart and Shutdown
    #

    def getLMIStatus(self):
        methodName = "getLMIStatus()"
        SystemSettings.logger.enterMethod(methodName)
        result = None

        statusCode, content = self.httpGetJson(SystemSettings.LMI)

        if statusCode == 200 and content is not None:
            result = content

        SystemSettings.logger.exitMethod(methodName, str(result))
        return result

    def restartLMI(self):
        methodName = "restartLMI()"
        SystemSettings.logger.enterMethod(methodName)
        result = None

        lastStartTime = -1

        content = self.getLMIStatus()

        if content is not None:
            lastStartTime = content[0].get("start_time", -1)

        if lastStartTime > 0:
            statusCode, content = self.httpPostJson(SystemSettings.LMI_RESTART)

            if statusCode == 200 and content is not None and content.get("restart", False) == True:
                SystemSettings.logger.log(methodName, "Waiting for LMI to restart...")
                self.waitForLMI(lastStartTime)
                result = True
        else:
            SystemSettings.logger.error(methodName, "Retrieved an invalid start time [%s]" % str(lastStartTime))

        SystemSettings.logger.exitMethod(methodName, str(result))
        return result

    def waitForLMI(self, lastStartTime, sleepInterval=3):
        methodName = "waitForLMI()"
        SystemSettings.logger.enterMethod(methodName)

        if lastStartTime > 0:
            restartTime = lastStartTime

            while (restartTime <= 0 or restartTime == lastStartTime):
                SystemSettings.logger.trace(methodName, "Waiting for LMI to restart. lastStartTime [%s] restartTime [%s]" % (lastStartTime, restartTime))
                time.sleep(sleepInterval)

                try:
                    content = self.getLMIStatus()

                    if content is not None:
                        restartTime = content[0].get("start_time", -1)
                except:
                    restartTime = -1

            time.sleep(sleepInterval)
        else:
            SystemSettings.logger.error(methodName, "Invalid last start time [%s]" % str(lastStartTime))

        SystemSettings.logger.exitMethod(methodName)
