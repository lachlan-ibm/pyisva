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
        statusCode, content = self.putJSON("Service Agreement", self.SERVICE_AGREEMENTS_ACCEPTED, jsonData)

        if statusCode == 200:
            self.logSuccess(description)
            return True

        self.logFailed(description)

    def completeSetup(self):
        description = "Completing setup"
        self.logger.info(description)

        statusCode, content = self.putJSON("Setup Complete", self.SETUP_COMPLETE)

        if statusCode == 200:
            self.logSuccess(description)
            return True

        self.logFailed(description)

    def isSetupComplete(self):
        description = "Checking if setup is complete"
        self.logger.info(description)

        statusCode, content = self.getJSON("Setup Complete", self.SETUP_COMPLETE)

        if statusCode == 200 and content is not None:
            self.logSuccess(description)
            return content.get("configured", False)

        self.logFailed(description)

    def isLicenseAccepted(self):
        description = "Checking if SLA has been accepted"
        self.logger.info(description)

        statusCode, content = self.getJSON("Service Agreement", self.SERVICE_AGREEMENTS_ACCEPTED)

        if statusCode == 200 and content is not None:
            self.logSuccess(description)
            return content.get("accepted", False)

        self.logFailed(description)
