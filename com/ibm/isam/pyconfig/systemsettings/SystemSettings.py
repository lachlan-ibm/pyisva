"""
Created on Nov 22, 2016

@copyright: IBM
"""
from com.ibm.isam.pyconfig.Base import Base
import logging, time, uuid

class SystemSettings(Base):

    ADMIN_CONFIG = "/core/admin_cfg"
    LMI = "/lmi"
    LMI_RESTART = "/restarts/restart_server"
    TIME_CONFIG = "/core/time_cfg"

    def __init__(self, baseUrl, username, password, logLevel=logging.ERROR):
        super(SystemSettings, self).__init__(baseUrl, username, password)

        self.logger = logging.getLogger("SystemSettings")
        self.logger.setLevel(logLevel)

    #
    # Administrator Settings
    #

    def getAdministratorSettings(self):
        description = "Retrieving administrator settings"
        self.logEntry(description)

        statusCode, content = self.getJSON("Administrator settings", SystemSettings.ADMIN_CONFIG)

        if statusCode == 200 and content is not None:
            self.logSuccess(description)
            return content

        self.logFailed(description)

    def updateAdministratorSettings(self, oldPassword=None, newPassword=None, confirmPassword=None, \
            minHeapSize=None, maxHeapSize=None, sessionTimeout=None, httpPort=None, httpsPort=None, \
            minThreads=None, maxThreads=None, maxPoolSize=None, lmiDebuggingEnabled=None, consoleLogLevel=None, \
            acceptClientCerts=None, validateClientCertIdentity=None, excludeCsrfChecking=None, enableSSLv3=None):
        description = "Updating administrator settings"
        self.logEntry(description)

        jsonObj = {}
        self.addOnStringValue(jsonObj, "oldPassword", oldPassword)
        self.addOnStringValue(jsonObj, "newPassword", newPassword)
        self.addOnStringValue(jsonObj, "confirmPassword", confirmPassword)
        self.addOnValue(jsonObj, "minHeapSize", minHeapSize)
        self.addOnValue(jsonObj, "maxHeapSize", maxHeapSize)
        self.addOnValue(jsonObj, "sessionTimeout", sessionTimeout)
        self.addOnValue(jsonObj, "httpPort", httpPort)
        self.addOnValue(jsonObj, "httpsPort", httpsPort)
        self.addOnValue(jsonObj, "minThreads", minThreads)
        self.addOnValue(jsonObj, "maxThreads", maxThreads)
        self.addOnValue(jsonObj, "maxPoolSize", maxPoolSize)
        self.addOnValue(jsonObj, "lmiDebuggingEnabled", lmiDebuggingEnabled)
        self.addOnStringValue(jsonObj, "consoleLogLevel", consoleLogLevel)
        self.addOnValue(jsonObj, "acceptClientCerts", acceptClientCerts)
        self.addOnValue(jsonObj, "validateClientCertIdentity", validateClientCertIdentity)
        self.addOnStringValue(jsonObj, "excludeCsrfChecking", excludeCsrfChecking)
        self.addOnValue(jsonObj, "enableSSLv3", enableSSLv3)

        statusCode, content = self.putJSON("Administrator settings", SystemSettings.ADMIN_CONFIG, jsonObj)

        if statusCode == 200:
            self.logSuccess(description)
            return (content or True)

        self.logFailed(description)

    def updateAdministratorPassword(self, newPassword):
        description = "Changing administrator password"
        self.logEntry(description)

        content = self.getAdministratorSettings()

        if content is not None:
            sessionTimeout = content.get("sessionTimeout", -1)

            if sessionTimeout > 0:
                if self.updateAdministratorSettings(sessionTimeout=sessionTimeout, oldPassword=self.PASSWORD, newPassword=newPassword, confirmPassword=newPassword):
                    self.logSuccess(description)
                    return True
            else:
                self.logger.debug("A valid session timeout was not returned.")
        else:
            oldPassword = self.PASSWORD
            self.PASSWORD = newPassword

            if self.getAdministratorSettings():
                self.logSuccess("The password was already configured.")
                return True
            else:
                self.PASSWORD = oldPassword

        self.logFailed(description)

    #
    # Date and Time Settings
    #

    def updateDateTimeSettings(self, enableNtp=True, dateTime="0000-00-00 00:00:00", ntpServers="pool.ntp.org", timeZone="Australia/Brisbane"):
        description = "Updating date and time settings"
        self.logEntry(description)

        jsonObj = {}
        self.addOnValue(jsonObj, "enableNtp", enableNtp)
        self.addOnStringValue(jsonObj, "dateTime", dateTime)
        self.addOnStringValue(jsonObj, "ntpServers", ntpServers)
        self.addOnStringValue(jsonObj, "timeZone", timeZone)

        statusCode, content = self.putJSON("Date and Time settings", SystemSettings.TIME_CONFIG, jsonObj)

        if statusCode == 200:
            self.logSuccess(description)
            return (content or True)

        self.logFailed(description)

    #
    # Restart and Shutdown
    #

    def getLMIStatus(self):
        description = "Retrieving Local Management Interface status"
        self.logEntry(description)

        statusCode, content = self.getJSON("LMI", self.LMI)

        if statusCode == 200 and content is not None:
            self.logSuccess(description)
            return content

        self.logFailed(description)

    def restartLMI(self):
        description = "Restarting Local Management Interface"
        self.logEntry(description)

        content = self.getLMIStatus()

        lastStartTime = -1
        if content is not None:
            lastStartTime = content[0].get("start_time", -1)

        if lastStartTime > 0:
            statusCode, content = self.postJSON("LMI Restart", self.LMI_RESTART)

            if statusCode == 200 and content.get("restart", False) == True:
                self.logSuccess(description)
                self.waitForLMI(lastStartTime)
                return True
            else:
                self.logFailed(description)
        else:
            self.logFailed("Retrieving Local Management Interface start time")

    def waitForLMI(self, lastStartTime, sleepInterval=3):
        description = "Waiting for Local Management Interface"
        self.logEntry(description)

        if lastStartTime > 0:
            restartTime = lastStartTime

            while (restartTime <= 0 or restartTime == lastStartTime):
                self.logger.debug("Waiting for LMI to restart. lastStartTime [%s] restartTime [%s]" % (lastStartTime, restartTime))
                time.sleep(sleepInterval)

                try:
                    content = self.getLMIStatus()

                    if content is not None:
                        restartTime = content[0].get("start_time", -1)
                except:
                    restartTime = -1

            time.sleep(sleepInterval)
        else:
            self.logFailed("Invalid lastStartTime value [%s]" % lastStartTime)
