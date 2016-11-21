"""
Created on Nov 17, 2016

@copyright: IBM
"""
from com.ibm.isam.pyconfig.Common import Common
import logging, time, uuid

class SystemSettings(Common):

    ADMIN_CONFIG = "/core/admin_cfg"
    CAPABILITIES = "/isam/capabilities/v1"
    HOST_RECORDS = "/isam/host_records"
    LMI = "/lmi"
    LMI_RESTART = "/restarts/restart_server"
    NET_DNS = "/net/dns"
    NET_INTERFACES = "/net/ifaces/"
    PENDING_CHANGES = "/isam/pending_changes"
    PENDING_CHANGES_DEPLOY = "/isam/pending_changes/deploy"
    RUNTIME_RESTART = "/isam/runtime_profile/local/v1"
    TIME_CONFIG = "/core/time_cfg"

    def __init__(self, baseUrl, username, password, logLevel=logging.INFO):
        super(SystemSettings, self).__init__(baseUrl, username, password)

        self.logger = logging.getLogger("SystemSettings")
        self.logger.setLevel(logLevel)

    def activateOffering(self, code):
        description = "Activating product offering"
        self.logger.info(description)

        if len(code) == 39:
            jsonObj = {"code":str(code)}
            statusCode, content = self.postJSON("Product Activation", self.CAPABILITIES, jsonObj)

            if statusCode == 200:
                self.logSuccess(description)
                return True
        else:
            self.logger.error("Activation code is invalid [%s]" % code)

        self.logFailed(description)

    def changeAdminPassword(self, newPassword):
        description = "Changing administrator password"
        self.logger.info(description)

        statusCode, content = self.getJSON("Administrator settings", SystemSettings.ADMIN_CONFIG)

        if statusCode == 200 and content is not None:
            sessionTimeout = content.get("sessionTimeout", -1)

            if sessionTimeout > 0:
                jsonObj = {
                    "sessionTimeout":str(sessionTimeout),
                    "oldPassword":self.PASSWORD,
                    "newPassword":newPassword,
                    "confirmPassword":newPassword
                }
                statusCode, content = self.putJSON("Administrator settings", SystemSettings.ADMIN_CONFIG, jsonObj)

                if statusCode == 200:
                    self.logSuccess(description)
                    self.PASSWORD = newPassword
                    return True
            else:
                self.logger.error("A valid session timeout was not returned.")
        else:
            oldPassword = self.PASSWORD
            self.PASSWORD = newPassword

            statusCode, content = self.getJSON("Administrator settings", SystemSettings.ADMIN_CONFIG)

            if statusCode == 200:
                self.logSuccess("The password was already configured")
                return True
            else:
                self.PASSWORD = oldPassword

        self.logFailed(description)

    def configureDNS(self, auto=True, autoFromInterface=None, primaryServer=None, secondaryServer=None, tertiaryServer=None, searchDomains=None):
        description = "Configuring DNS settings"
        self.logger.info(description)

        statusCode, jsonObj = self.getJSON("DNS configuration", SystemSettings.NET_DNS)

        if statusCode != 200:
            jsonObj = {}

        jsonObj["auto"] = auto
        if auto is False:
            self.addOnValue(jsonObj, "autoFromInterface", autoFromInterface)
            self.addOnValue(jsonObj, "primaryServer", primaryServer)
            self.addOnValue(jsonObj, "secondaryServer", secondaryServer)
            self.addOnValue(jsonObj, "tertiaryServer", tertiaryServer)
            self.addOnValue(jsonObj, "searchDomains", searchDomains)

        statusCode, content = self.putJSON("DNS configuration", SystemSettings.NET_DNS, jsonObj)

        if statusCode == 200:
            self.logSuccess(description)
            return True

        self.logFailed(description)

    def configureNTP(self, enableNtp=True, dateTime="0000-00-00 00:00:00", ntpServer="pool.ntp.org", timeZone="Australia/Brisbane"):
        description = "Configuring NTP server"
        self.logger.info(description)

        jsonObj = {
            "enableNtp":enableNtp,
            "dateTime":str(dateTime),
            "ntpServers":str(ntpServer),
            "timeZone":str(timeZone)
        }
        statusCode, content = self.putJSON("Date and Time settings", SystemSettings.TIME_CONFIG, jsonObj)

        if statusCode == 200:
            self.logSuccess(description)
            return True

        self.logFailed(description)

    def createHostRecord(self, ipv4Address, hostNames):
        description = "Creating a Host record"
        self.logger.info(description)

        success = False
        hostNameList = str(hostNames).split(",")

        ipv4HostEndpoint = SystemSettings.HOST_RECORDS + "/" + ipv4Address + "/hostnames"
        statusCode, content = self.getJSON("Host records", ipv4HostEndpoint, silent=True)

        if statusCode == 200:
            for index in range(len(hostNameList)):
                jsonObj = {"name":hostNameList[index]}
                statusCode, content = self.postJSON("Host records", ipv4HostEndpoint, jsonObj)

                if statusCode == 200:
                    success = True
        else:
            jsonObj = {"addr":ipv4Address,"hostnames":[]}
            for index in range(len(hostNameList)):
                jsonObj["hostnames"].append({"name":hostNameList[index]})

            statusCode, content = self.postJSON("Host records", SystemSettings.HOST_RECORDS, jsonObj)

            if statusCode == 200:
                success = True

        if success:
            self.logSuccess(description)
            return True

        self.logFailed(description)

    def createIPAddress(self, ipv4Address, netmask, interfaceLabel="1.1", enabled=True, management=False):
        description = "Creating an IP address"
        self.logger.info(description)

        statusCode, content = self.getJSON("Interfaces", self.NET_INTERFACES)

        if statusCode == 200 and content is not None:
            for index in range(len(content.get("interfaces", []))):
                if content["interfaces"][index].get("label") == str(interfaceLabel):
                    jsonObj = content["interfaces"][index]

                    addresses = jsonObj.get("ipv4", {}).get("addresses", [])
                    for i in range(len(addresses)):
                        if addresses[i].get("address") == str(ipv4Address):
                            self.logSuccess("The IP address is already configured [%s]" % ipv4Address)
                            return True

                    addressObj = {"objType":"ipv4Address","enabled":enabled}
                    self.addOnValue(addressObj, "maskOrPrefix", netmask)
                    self.addOnValue(addressObj, "address", ipv4Address)
                    self.addOnValue(addressObj, "allowManagement", management)
                    self.addOnValue(addressObj, "uuid", uuid.uuid4())

                    jsonObj["ipv4"]["addresses"].append(addressObj)
                    statusCode, content = self.putJSON("Specific Interface", self.NET_INTERFACES + "/" + str(jsonObj['uuid']), jsonObj)
                    if statusCode == 200:
                        self.logSuccess(description)
                        return True

        self.logFailed(description)

    def deployPendingChanges(self):
        description = "Deploying pending changes"
        self.logger.info(description)

        statusCode, content = self.getJSON("Pending Changes", self.PENDING_CHANGES)

        if statusCode == 200 and content is not None:
            if len(content.get("changes", 0)) > 0:
                if self._deployPendingChanges():
                    self.logSuccess(description)
                    return True
            else:
                self.logSuccess("No pending changes to be deployed")
                return True

        self.logFailed(description)

    def restartLMI(self):
        description = "Restarting the Local Management Interface"
        self.logger.info(description)

        lastStartTime = self._getStartTime("LMI", self.LMI)

        if lastStartTime > 0:
            statusCode, content = self.postJSON("LMI Restart", self.LMI_RESTART)

            if statusCode == 200 and content.get("restart", False) == True:
                self.logSuccess(description)
                self._waitForRestart("LMI", self.LMI, lastStartTime)
                return True
            else:
                self.logFailed(description)
        else:
            self.logFailed("Retrieving the LMI start time")

    def _deployPendingChanges(self):
        description = "Deploying pending changes"
        self.logger.debug(description)

        success = True
        runtimeLastStart = self._getStartTime("Runtime", self.RUNTIME_RESTART)

        statusCode, content = self.getJSON("Pending Changes Deploy", self.PENDING_CHANGES_DEPLOY)

        if statusCode == 200 and content.get("result", -1) == 0:
            status = content.get("status")

            if status == 0:
                self.logger.debug("Successful operation. No further action needed.")
            else:
                if (status & 1) != 0:
                    self.logger.error("Deployment of changes resulted in good result but failure status [" + str(status) + "]")
                    success = False
                if (status & 2) != 0:
                    self.logger.error("Appliance restart required - halting [" + str(status) + "]")
                    success = False
                if (status & 4) != 0 or (status & 8) != 0:
                    self.logger.debug("Restarting LMI as required for status [" + str(status) + "]")
                    self.restartLMI()
                if (status & 16) != 0:
                    self.logger.debug("Deployment of changes indicates a server needs restarting [" + str(status) + "]")
                if (status & 32) != 0:
                    self.logger.debug("Runtime restart was performed for status [" + str(status) + "]")
                    self._waitForRestart("Runtime", self.RUNTIME_RESTART, runtimeLastStart)

        if success:
            self.logger.debug("Success: %s" % description)
            return True

        self.logger.debug("Failed: %s" % description)

    def _getStartTime(self, service, endpoint):
        description = "Retrieving %s start time" % service
        self.logger.debug(description)

        try:
            statusCode, content = self.getJSON("%s start time" % service, endpoint, silent=True)

            if statusCode == 200:
                self.logger.debug("Success: %s" % description)
                return content[0].get("start_time")
            else:
                self.logger.debug("Failed: %s" % description)
        except:
            self.logger.debug("Failed: %s" % description)

        return -1

    def _waitForRestart(self, service, endpoint, lastStartTime, sleepInterval=3):
        description = "Waiting for %s to restart" % service
        self.logger.debug(description)

        if lastStartTime > 0:
            restartTime = lastStartTime

            while (restartTime <= 0 or restartTime == lastStartTime):
                self.logger.debug("Waiting for %s to restart. lastStartTime [%s] restartTime [%s]" % (service, lastStartTime, restartTime))
                time.sleep(sleepInterval)
                restartTime = self._getStartTime(service, endpoint)

            time.sleep(sleepInterval)
        else:
            self.logFailed("Invalid lastStartTime value [" + str(lastStartTime) + "]")
