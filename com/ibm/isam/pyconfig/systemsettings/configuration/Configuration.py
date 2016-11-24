"""
Created on Nov 22, 2016

@copyright: IBM
"""
from com.ibm.isam.pyconfig.Factory import Factory
from com.ibm.isam.util.RestClient import RestClient
from com.ibm.isam.util.Logger import Logger
import com.ibm.isam.util.Utils as Utils
import abc, logging

class Configuration(RestClient):
    __metaclass__ = abc.ABCMeta

    PENDING_CHANGES = "/isam/pending_changes"
    PENDING_CHANGES_DEPLOY = "/isam/pending_changes/deploy"

    logger = Logger("Configuration")

    def __init__(self, baseUrl, username, password, logLevel=logging.NOTSET):
        super(Configuration, self).__init__(baseUrl, username, password, logLevel)
        Configuration.logger.setLevel(logLevel)

    @abc.abstractmethod
    def getIsamVersion(self):
        pass

    #
    # Configuration Changes
    #

    def getPendingChanges(self):
        methodName = "getPendingChanges()"
        Configuration.logger.enterMethod(methodName)
        result = None

        statusCode, content = self.httpGetJson(Configuration.PENDING_CHANGES)

        if statusCode == 200 and content is not None:
            result = content

        Configuration.logger.exitMethod(methodName, str(result))
        return result

    def deployPendingChanges(self):
        methodName = "deployPendingChanges()"
        Configuration.logger.enterMethod(methodName)
        result = None

        content = self.getPendingChanges()

        if content is not None:
            if len(content.get("changes", 0)) > 0:
                if self._deployPendingChanges():
                    result = True
            else:
                Configuration.logger.log(methodName, "No pending changes to be deployed.")
                result = True

        Configuration.logger.exitMethod(methodName, str(result))
        return result

    def _deployPendingChanges(self):
        methodName = "_deployPendingChanges()"
        Configuration.logger.enterMethod(methodName)
        result = False

        statusCode, content = self.httpGetJson(Configuration.PENDING_CHANGES_DEPLOY)

        if statusCode == 200 and content is not None and content.get("result", -1) == 0:
            status = content.get("status")
            result = True

            if status == 0:
                Configuration.logger.log(methodName, "Successful operation. No further action needed.")
            else:
                if (status & 1) != 0:
                    Configuration.logger.error(methodName, "Deployment of changes resulted in good result but failure status [%s]" % str(status))
                    result = False
                if (status & 2) != 0:
                    Configuration.logger.error(methodName, "Appliance restart required - halting [%s]" % str(status))
                    result = False
                if (status & 4) != 0 or (status & 8) != 0:
                    Configuration.logger.log(methodName, "Restarting LMI as required for status [%s]" % str(status))
                    sysSettings = Factory(self.getIsamVersion()).getSystemSystemSettings(self.baseUrl, self.username, self.password, Configuration.logger.getLevel())
                    sysSettings.restartLMI()
                if (status & 16) != 0:
                    Configuration.logger.log(methodName, "Deployment of changes indicates a server needs restarting [%s]" % str(status))
                if (status & 32) != 0:
                    Configuration.logger.log(methodName, "Runtime restart was performed for status [%s]" % str(status))
                    # TODO: Wait for Runtime to restart...

        Configuration.logger.exitMethod(methodName, str(result))
        return result
