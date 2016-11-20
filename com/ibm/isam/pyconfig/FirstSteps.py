"""
Created on Nov 17, 2016

@copyright: IBM
"""
from com.ibm.isam.pyconfig.Common import Common
import logging

class FirstSteps(Common):

    SETUP_COMPLETE = "/setup_complete"
    SERVICE_AGREEMENTS_ACCEPTED = "/setup_service_agreements/accepted"

    def __init__(self, baseUrl, username, password, logLevel=logging.INFO):
        super(FirstSteps, self).__init__(baseUrl, username, password)

        self.logger = logging.getLogger("FirstSteps")
        self.logger.setLevel(logLevel)

    def acceptLicense(self, accept=True):
        description = "Accepting the SLA"
        self.logger.info(description)

        jsonData = {"accepted":accept}
        statusCode, content = self._putJSON("Service Agreement", self.SERVICE_AGREEMENTS_ACCEPTED, jsonData)

        if content is not None:
            self._logSuccess(description)
            return True

        self._logFailed(description)

    def completeSetup(self):
        description = "Completing setup"
        self.logger.info(description)

        statusCode, content = self._putJSON("Setup Complete", self.SETUP_COMPLETE)

        if content is not None:
            self._logSuccess(description)
            return True

        self._logFailed(description)

    def isSetupComplete(self):
        description = "Checking if setup is complete"
        self.logger.info(description)

        statusCode, content = self._getJSON("Setup Complete", self.SETUP_COMPLETE)

        if content is not None:
            self._logSuccess(description)
            return content['configured']

        self._logFailed(description)

    def isLicenseAccepted(self):
        description = "Checking if SLA has been accepted"
        self.logger.info(description)

        statusCode, content = self._getJSON("Service Agreement", self.SERVICE_AGREEMENTS_ACCEPTED)

        if content is not None:
            self._logSuccess(description)
            return content['accepted']

        self._logFailed(description)
