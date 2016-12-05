"""
Created on Nov 22, 2016

@copyright: IBM
"""

import logging

from com.ibm.isam.util.logger import Logger
from com.ibm.isam.util.restclient import RestClient
import com.ibm.isam.util.utils as Utils


class _UpdatesLicensing(RestClient):

    CAPABILITIES = "/isam/capabilities"
    CAPABILITIES_V1 = CAPABILITIES + "/v1"

    logger = Logger("UpdatesLicensing")

    def __init__(self, baseUrl, username, password, logLevel=logging.NOTSET):
        super(_UpdatesLicensing, self).__init__(baseUrl, username, password, logLevel)
        _UpdatesLicensing.logger.setLevel(logLevel)

    #
    # Licensing and Activation
    #

    def activateModule(self, code):
        methodName = "activateModule()"
        _UpdatesLicensing.logger.enterMethod(methodName)
        result = None

        jsonObj = {}
        Utils.addOnStringValue(jsonObj, "code", code)

        statusCode, content = self.httpPostJson(_UpdatesLicensing.CAPABILITIES_V1, jsonObj)

        result = (statusCode == 200, statusCode, content)

        _UpdatesLicensing.logger.exitMethod(methodName, str(result))
        return result

    def getActivatedModule(self, id):
        methodName = "getActivatedModule()"
        _UpdatesLicensing.logger.enterMethod(methodName)
        result = None

        endpoint = "%s/%s/v1" % (_UpdatesLicensing.CAPABILITIES, str(id))
        statusCode, content = self.httpGetJson(endpoint)

        result = (statusCode == 200, statusCode, content)

        _UpdatesLicensing.logger.exitMethod(methodName, str(result))
        return result

    def getActivatedModules(self):
        methodName = "getActivatedModules()"
        _UpdatesLicensing.logger.enterMethod(methodName)
        result = None

        statusCode, content = self.httpGetJson(_UpdatesLicensing.CAPABILITIES_V1)

        result = (statusCode == 200, statusCode, content)

        _UpdatesLicensing.logger.exitMethod(methodName, str(result))
        return result


class UpdatesLicensing9020(_UpdatesLicensing):

    logger = Logger("UpdatesLicensing9020")

    def __init__(self, baseUrl, username, password, logLevel=logging.NOTSET):
        super(UpdatesLicensing9020, self).__init__(baseUrl, username, password, logLevel)
        UpdatesLicensing9020.logger.setLevel(logLevel)
