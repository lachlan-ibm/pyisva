"""
Created on Nov 17, 2016

@copyright: IBM
"""
from com.ibm.isam.pyconfig.Base import Base
from com.ibm.isam.util.HTTPRequest import ISAMRestClient
import logging

class FirstSteps(Base):

    SETUP_COMPLETE = "/setup_complete"
    SERVICE_AGREEMENTS_ACCEPTED = "/setup_service_agreements/accepted"

    def __init__(self, baseUrl, username, password, logLevel=logging.ERROR):
        super(FirstSteps, self).__init__(baseUrl, username, password)

        self.logger = logging.getLogger("FirstSteps")
        self.logger.setLevel(logLevel)

    #
    # First Steps Setup
    #

    def getSetupStatus(self):
        description = "Retrieving Setup status"
        self.logEntry(description)

        statusCode, content = self.getJSON("Setup Complete", self.SETUP_COMPLETE)

        if statusCode == 200 and content is not None:
            self.logSuccess(description)
            return content.get("configured", False)

        self.logFailed(description)

    def setSetupComplete(self):
        description = "Completing Setup"
        self.logEntry(description)

        statusCode, content = self.putJSON("Setup Complete", self.SETUP_COMPLETE)

        if statusCode == 200:
            self.logSuccess(description)
            return (content or True)

        self.logFailed(description)

    #
    # Service Agreements
    #

    def getSLAStatus(self):
        description = "Retrieving SLA acceptance status"
        self.logEntry(description)

        statusCode, content = self.getJSON("Service Agreement", self.SERVICE_AGREEMENTS_ACCEPTED)

        if statusCode == 200 and content is not None:
            self.logSuccess(description)
            return content.get("accepted", False)

        self.logFailed(description)

    def setSLAStatus(self, accept=True):
        description = "Updating SLA acceptance status"
        self.logEntry(description)

        jsonData = {"accepted":accept}
        statusCode, content = self.putJSON("Service Agreement", self.SERVICE_AGREEMENTS_ACCEPTED, jsonData)

        if statusCode == 200:
            self.logSuccess(description)
            return (content or True)

        self.logFailed(description)

    #
    # Miscellaneous
    #

    def testPassword(self, password=None):
        if password is None:
            password = self.PASSWORD

        client = ISAMRestClient(username=self.USERNAME, password=password)
        statusCode, contentHeader, content = client.get(self.BASE_URL, self.SETUP_COMPLETE, self.APPLICATION_JSON)

        if statusCode == 200:
            return True
