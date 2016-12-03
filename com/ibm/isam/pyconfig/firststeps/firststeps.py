"""
Created on Nov 17, 2016

@copyright: IBM
"""

import logging

from com.ibm.isam.util.logger import Logger
from com.ibm.isam.util.restclient import RestClient


class _FirstSteps(RestClient):

    SETUP_COMPLETE = "/setup_complete"
    SERVICE_AGREEMENTS_ACCEPTED = "/setup_service_agreements/accepted"

    logger = Logger("FirstSteps")

    def __init__(self, baseUrl, username, password, logLevel=logging.NOTSET):
        super(_FirstSteps, self).__init__(baseUrl, username, password, logLevel)
        _FirstSteps.logger.setLevel(logLevel)

    #
    # First Steps Setup
    #

    def getSetupStatus(self):
        methodName = "getSetupStatus()"
        _FirstSteps.logger.enterMethod(methodName)
        result = None

        statusCode, content = self.httpGetJson(_FirstSteps.SETUP_COMPLETE)

        if statusCode == 200 and content is not None:
            result = content

        _FirstSteps.logger.exitMethod(methodName, result)
        return result

    def setSetupComplete(self):
        methodName = "setSetupComplete()"
        _FirstSteps.logger.enterMethod(methodName)
        result = None

        statusCode, content = self.httpPutJson(_FirstSteps.SETUP_COMPLETE)

        if statusCode == 200:
            result = True if content is None else content

        _FirstSteps.logger.exitMethod(methodName, result)
        return result

    #
    # Service Agreements
    #

    def getSLAStatus(self):
        methodName = "getSLAStatus()"
        _FirstSteps.logger.enterMethod(methodName)
        result = None

        statusCode, content = self.httpGetJson(_FirstSteps.SERVICE_AGREEMENTS_ACCEPTED)

        if statusCode == 200 and content is not None:
            result = content

        _FirstSteps.logger.exitMethod(methodName, result)
        return result

    def setSLAStatus(self, accept=True):
        methodName = "setSLAStatus(accept)"
        _FirstSteps.logger.enterMethod(methodName)
        result = None

        jsonData = {"accepted":accept}
        statusCode, content = self.httpPutJson(_FirstSteps.SERVICE_AGREEMENTS_ACCEPTED, jsonData)

        if statusCode == 200:
            result = True if content is None else content

        _FirstSteps.logger.exitMethod(methodName, result)
        return result


class FirstSteps9020(_FirstSteps):

    logger = Logger("FirstSteps9020")

    def __init__(self, baseUrl, username, password, logLevel=logging.NOTSET):
        super(FirstSteps9020, self).__init__(baseUrl, username, password, logLevel)
        FirstSteps9020.logger.setLevel(logLevel)
