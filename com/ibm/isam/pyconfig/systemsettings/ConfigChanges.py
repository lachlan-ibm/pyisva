"""
Created on Nov 22, 2016

@copyright: IBM
"""
from com.ibm.isam.pyconfig.Base import Base
from SystemSettings import SystemSettings
import logging, time, uuid

class ConfigChanges(Base):

    PENDING_CHANGES = "/isam/pending_changes"
    PENDING_CHANGES_DEPLOY = "/isam/pending_changes/deploy"

    def __init__(self, baseUrl, username, password, logLevel=logging.ERROR):
        super(ConfigChanges, self).__init__(baseUrl, username, password)

        self.logger = logging.getLogger("ConfigChanges")
        self.logger.setLevel(logLevel)

    #
    # Configuration Changes
    #

    def getPendingChanges(self):
        description = "Retrieving pending changes"
        self.logEntry(description)

        statusCode, content = self.getJSON("Pending Changes", self.PENDING_CHANGES)

        if statusCode == 200 and content is not None:
            self.logSuccess(description)
            return content

        self.logFailed(description)

    def deployPendingChanges(self):
        description = "Deploying pending changes"
        self.logEntry(description)

        content = self.getPendingChanges()

        if content is not None:
            if len(content.get("changes", 0)) > 0:
                if self._deployPendingChanges():
                    self.logSuccess(description)
                    return True
            else:
                self.logSuccess("No pending changes to be deployed.")
                return True

        self.logFailed(description)

    def _deployPendingChanges(self):
        description = "Deploying pending changes"
        self.logEntry(description)

        success = True

        statusCode, content = self.getJSON("Pending Changes Deploy", self.PENDING_CHANGES_DEPLOY)

        if statusCode == 200 and content.get("result", -1) == 0:
            status = content.get("status")

            if status == 0:
                self.logger.info("Successful operation. No further action needed.")
            else:
                if (status & 1) != 0:
                    self.logger.warning("Deployment of changes resulted in good result but failure status [%s]" % str(status))
                    success = False
                if (status & 2) != 0:
                    self.logger.warning("Appliance restart required - halting [%s]" % str(status))
                    success = False
                if (status & 4) != 0 or (status & 8) != 0:
                    self.logger.info("Restarting LMI as required for status [%s]" % str(status))
                    sysSettings = SystemSettings(self.BASE_URL, self.USERNAME, self.PASSWORD, self.logger.getEffectiveLevel())
                    sysSettings.restartLMI()
                if (status & 16) != 0:
                    self.logger.info("Deployment of changes indicates a server needs restarting [%s]" % str(status))
                if (status & 32) != 0:
                    self.logger.info("Runtime restart was performed for status [%s]" % str(status))
                    # TODO: Wait for Runtime to restart...

        if success:
            self.logSuccess(description)
            return True

        self.logFailed(description)
