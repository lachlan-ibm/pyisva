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
            statusCode, content = self._postJSON("Product Activation", self.CAPABILITIES, jsonObj)

            if content is not None:
                self._logSuccess(description)
                return True
        else:
            self.logger.error("Activation code is invalid [%s]" % code)

        self._logFailed(description)

    def changeAdminPassword(self, newPassword):
        description = "Changing administrator password"
        self.logger.info(description)

        statusCode, content = self._getJSON("Administrator settings", SystemSettings.ADMIN_CONFIG)

        if content is not None:
            sessionTimeout = content['sessionTimeout']

            if sessionTimeout > 0:
                jsonObj = {"sessionTimeout":str(sessionTimeout),"oldPassword":self.PASSWORD,"newPassword":newPassword,"confirmPassword":newPassword}
                statusCode, content = self._putJSON("Administrator settings", SystemSettings.ADMIN_CONFIG, jsonObj)

                if content is not None:
                    self._logSuccess(description)
                    super(SystemSettings, self).changeAdminPassword(newPassword)
                    return True
            else:
                self.logger.error("A valid session timeout was not returned.")
        else:
            oldPassword = self.PASSWORD
            super(SystemSettings, self).changeAdminPassword(newPassword)

            statusCode, content = self._getJSON("Administrator settings", SystemSettings.ADMIN_CONFIG)

            if content is not None:
                self._logSuccess("The password was already configured")
                return True
            else:
                super(SystemSettings, self).changeAdminPassword(oldPassword)

        self._logFailed(description)

    def configureDNS(self, auto=True, autoFromInterface=None, primaryServer=None, secondaryServer=None, tertiaryServer=None, searchDomains=None):
        description = "Configuring DNS settings"
        self.logger.info(description)

        statusCode, jsonObj = self._getJSON("DNS configuration", SystemSettings.NET_DNS)

        if jsonObj is not None:
            jsonObj['auto'] = auto
            if auto is False:
                if autoFromInterface is not None:
                    jsonObj['autoFromInterface'] = str(autoFromInterface)
                if primaryServer is not None:
                    jsonObj['primaryServer'] = str(primaryServer)
                if secondaryServer is not None:
                    jsonObj['secondaryServer'] = str(secondaryServer)
                if tertiaryServer is not None:
                    jsonObj['tertiaryServer'] = str(tertiaryServer)
                if searchDomains is not None:
                    jsonObj['searchDomains'] = str(searchDomains)
        else:
            jsonObj = {}
            jsonObj['auto'] = auto
            if auto is False:
                jsonObj['autoFromInterface'] = str(autoFromInterface)
                jsonObj['primaryServer'] = str(primaryServer)
                jsonObj['secondaryServer'] = str(secondaryServer)
                jsonObj['tertiaryServer'] = str(tertiaryServer)
                jsonObj['searchDomains'] = str(searchDomains)

        statusCode, content = self._putJSON("DNS configuration", SystemSettings.NET_DNS, jsonObj)

        if content is not None:
            self._logSuccess(description)
            return True

        self._logFailed(description)

    def configureNTP(self, dateTime="0000-00-00 00:00:00", ntpServer="pool.ntp.org", timeZone="Australia/Brisbane", enableNtp=True):
        description = "Configuring NTP server"
        self.logger.info(description)

        jsonObj = {"dateTime":str(dateTime),"ntpServers":str(ntpServer),"timeZone":str(timeZone),"enableNtp":enableNtp}
        statusCode, content = self._putJSON("Date and Time settings", SystemSettings.TIME_CONFIG, jsonObj)

        if content is not None:
            self._logSuccess(description)
            return True

        self._logFailed(description)

    def createHostRecord(self, ipv4Address, hostNames):
        description = "Creating a Host record"
        self.logger.info(description)

        success = False
        hostNameList = str(hostNames).split(",")

        ipv4HostEndpoint = SystemSettings.HOST_RECORDS + "/" + ipv4Address + "/hostnames"
        statusCode, content = self._getJSON("Host records", ipv4HostEndpoint, silent=True)

        if content is not None:
            for index in range(len(hostNameList)):
                jsonObj = {"name":hostNameList[index]}
                statusCode, content = self._postJSON("Host records", ipv4HostEndpoint, jsonObj)

                if content is not None:
                    success = True
        else:
            jsonObj = {"addr":ipv4Address,"hostnames":[]}
            for index in range(len(hostNameList)):
                jsonObj['hostnames'].append({"name":hostNameList[index]})

            statusCode, content = self._postJSON("Host records", SystemSettings.HOST_RECORDS, jsonObj)

            if content is not None:
                success = True

        if success:
            self._logSuccess(description)
            return True

        self._logFailed(description)

    def createIPAddress(self, ipv4Address, netmask, interfaceLabel="1.1", enabled=True, management=False):
        description = "Creating an IP address"
        self.logger.info(description)

        alreadyConfigured = False
        jsonObj = None

        statusCode, content = self._getJSON("Interfaces", self.NET_INTERFACES)

        if content is not None:
            for index in range(len(content['interfaces'])):
                if content['interfaces'][index]['label'] == interfaceLabel:
                    jsonObj = content['interfaces'][index]

                    addresses = jsonObj['ipv4']['addresses']
                    for i in range(len(addresses)):
                        if addresses[i]['address'] == str(ipv4Address):
                            alreadyConfigured = True

        if jsonObj is not None:
            if not alreadyConfigured:
                addressPayload = {
                    "maskOrPrefix": str(netmask),
                    "address": str(ipv4Address),
                    "allowManagement": str(management),
                    "uuid": str(uuid.uuid4()),
                    "objType": "ipv4Address",
                    "enabled": enabled
                }

                jsonObj['ipv4']['addresses'].append(addressPayload)
                statusCode, content = self._putJSON("Specific Interface", self.NET_INTERFACES + "/" + str(jsonObj['uuid']), jsonObj)
                if content is not None:
                    self._logSuccess(description)
                    return True
            else:
                self._logSuccess("The IP address is already configured [%s]" % ipv4Address)
                return True

        self._logFailed(description)

    def deployPendingChanges(self):
        description = "Deploying pending changes"
        self.logger.info(description)

        statusCode, content = self._getJSON("Pending Changes", self.PENDING_CHANGES)

        if content is not None:
            if len(content['changes']) > 0:
                if self._deployPendingChanges():
                    self._logSuccess(description)
                    return True
            else:
                self._logSuccess("No pending changes to be deployed")
                return True

        self._logFailed(description)

    def restartLMI(self):
        description = "Restarting the Local Management Interface"
        self.logger.info(description)

        lastStartTime = self._getStartTime("LMI", self.LMI)

        if lastStartTime > 0:
            statusCode, content = self._postJSON("LMI Restart", self.LMI_RESTART)

            if content is not None and content['restart'] == True:
                self._logSuccess(description)
                self._waitForRestart("LMI", self.LMI, lastStartTime)
                return True
            else:
                self._logFailed(description)
        else:
            self._logFailed("Retrieving the LMI start time")

    def _deployPendingChanges(self):
        description = "Deploying pending changes"
        self.logger.debug(description)

        success = True
        runtimeLastStart = self._getStartTime("Runtime", self.RUNTIME_RESTART)

        statusCode, content = self._getJSON("Pending Changes Deploy", self.PENDING_CHANGES_DEPLOY)

        if content is not None and content['result'] == 0:
            status = content['status']

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
            statusCode, content = self._getJSON("%s start time" % service, endpoint, silent=True)

            if content is not None:
                self.logger.debug("Success: %s" % description)
                return content[0]['start_time']
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
            self._logFailed("Invalid lastStartTime value [" + str(lastStartTime) + "]")
