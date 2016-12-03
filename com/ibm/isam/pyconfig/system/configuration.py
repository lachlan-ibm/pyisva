"""
Created on Nov 22, 2016

@copyright: IBM
"""

import logging

from com.ibm.isam.util.logger import Logger
from com.ibm.isam.util.restclient import RestClient

from .system import SystemSettings9020


class _Configuration(RestClient):

    PENDING_CHANGES = "/isam/pending_changes"
    PENDING_CHANGES_DEPLOY = "/isam/pending_changes/deploy"

    logger = Logger("Configuration")

    def __init__(self, baseUrl, username, password, logLevel=logging.NOTSET):
        super(_Configuration, self).__init__(baseUrl, username, password, logLevel)
        _Configuration.logger.setLevel(logLevel)

    #
    # Pending Changes
    #

    def deployPendingChanges(self):
        methodName = "deployPendingChanges()"
        _Configuration.logger.enterMethod(methodName)
        result = None

        content = self.getPendingChanges()

        if content is not None:
            if len(content.get("changes", 0)) > 0:
                result = self._deployPendingChanges()
            else:
                _Configuration.logger.log(methodName, "No pending changes to be deployed.")
                result = True

        _Configuration.logger.exitMethod(methodName, str(result))
        return result

    def getPendingChanges(self):
        methodName = "getPendingChanges()"
        _Configuration.logger.enterMethod(methodName)
        result = None

        statusCode, content = self.httpGetJson(_Configuration.PENDING_CHANGES)

        if statusCode == 200 and content is not None:
            result = content

        _Configuration.logger.exitMethod(methodName, str(result))
        return result

    def _deployPendingChanges(self):
        methodName = "_deployPendingChanges()"
        _Configuration.logger.enterMethod(methodName)
        result = None

        statusCode, content = self.httpGetJson(_Configuration.PENDING_CHANGES_DEPLOY)

        if statusCode == 200 and content is not None and content.get("result", -1) == 0:
            status = content.get("status")
            result = True

            if status == 0:
                _Configuration.logger.log(methodName, "Successful operation. No further action needed.")
            else:
                if (status & 1) != 0:
                    _Configuration.logger.error(methodName, "Deployment of changes resulted in good result but failure status [%s]" % str(status))
                    result = None
                if (status & 2) != 0:
                    _Configuration.logger.error(methodName, "Appliance restart required - halting [%s]" % str(status))
                    result = None
                if (status & 4) != 0 or (status & 8) != 0:
                    _Configuration.logger.log(methodName, "Restarting LMI as required for status [%s]" % str(status))
                    self._restartLmi()
                if (status & 16) != 0:
                    _Configuration.logger.log(methodName, "Deployment of changes indicates a server needs restarting [%s]" % str(status))
                if (status & 32) != 0:
                    _Configuration.logger.log(methodName, "Runtime restart was performed for status [%s]" % str(status))
                    # TODO: Wait for Runtime to restart...

        _Configuration.logger.exitMethod(methodName, str(result))
        return result

    def _restartLmi(self):
        pass


class Configuration9020(_Configuration):

    logger = Logger("Configuration9020")

    def __init__(self, baseUrl, username, password, logLevel=logging.NOTSET):
        super(Configuration9020, self).__init__(baseUrl, username, password, logLevel)
        Configuration9020.logger.setLevel(logLevel)

    def _restartLmi(self):
        systemSettings = SystemSettings9020(self.baseUrl, self.username, self.password,
                                            Configuration9020.logger.getLeve())
        systemSettings.restartLmi()
