"""
Created on Nov 17, 2016

@copyright: IBM
"""
from com.ibm.isam.util.RestClient import RestClient
from com.ibm.isam.util.Logger import Logger
import abc, logging

class FirstSteps(RestClient):
    __metaclass__ = abc.ABCMeta

    SETUP_COMPLETE = "/setup_complete"
    SERVICE_AGREEMENTS_ACCEPTED = "/setup_service_agreements/accepted"

    logger = Logger("FirstSteps")

    def __init__(self, baseUrl, username, password, logLevel=logging.NOTSET):
        super(FirstSteps, self).__init__(baseUrl, username, password, logLevel)
        FirstSteps.logger.setLevel(logLevel)

    @abc.abstractmethod
    def getIsamVersion(self):
        pass

    #
    # First Steps Setup
    #

    def getSetupStatus(self):
        methodName = "getSetupStatus()"
        FirstSteps.logger.enterMethod(methodName)
        result = False

        statusCode, content = self.httpGetJson(FirstSteps.SETUP_COMPLETE)

        if statusCode == 200 and content is not None:
            result = content.get("configured", False)

        FirstSteps.logger.exitMethod(methodName)
        return result

    def setSetupComplete(self):
        methodName = "setSetupComplete()"
        FirstSteps.logger.enterMethod(methodName)
        result = None

        statusCode, content = self.httpPutJson(FirstSteps.SETUP_COMPLETE)

        if statusCode == 200:
            result = True if content is None else content

        FirstSteps.logger.exitMethod(methodName)
        return result

    #
    # Service Agreements
    #

    def getSLAStatus(self):
        methodName = "getSLAStatus()"
        FirstSteps.logger.enterMethod(methodName)
        result = False

        statusCode, content = self.httpGetJson(FirstSteps.SERVICE_AGREEMENTS_ACCEPTED)

        if statusCode == 200 and content is not None:
            result = content.get("accepted", False)

        FirstSteps.logger.exitMethod(methodName)
        return result

    def setSLAStatus(self, accept=True):
        methodName = "setSLAStatus(accept)"
        FirstSteps.logger.enterMethod(methodName)
        result = None

        jsonData = {"accepted":accept}
        statusCode, content = self.httpPutJson(FirstSteps.SERVICE_AGREEMENTS_ACCEPTED, jsonData)

        if statusCode == 200:
            result = True if content is None else content

        FirstSteps.logger.exitMethod(methodName)
        return result

    #
    # Miscellaneous
    #

    def testPassword(self):
        methodName = "testPassword()"
        FirstSteps.logger.enterMethod(methodName)

        statusCode, content = self.httpGetJson(FirstSteps.SETUP_COMPLETE)

        FirstSteps.logger.exitMethod(methodName)
        return statusCode == 200
