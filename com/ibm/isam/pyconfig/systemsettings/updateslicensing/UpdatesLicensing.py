"""
Created on Nov 22, 2016

@copyright: IBM
"""
from com.ibm.isam.util.RestClient import RestClient
from com.ibm.isam.util.Logger import Logger
import com.ibm.isam.util.Utils as Utils
import abc, logging

class UpdatesLicensing(RestClient):
    __metaclass__ = abc.ABCMeta

    CAPABILITIES = "/isam/capabilities"
    CAPABILITIES_V1 = CAPABILITIES + "/v1"

    logger = Logger("UpdatesLicensing")

    def __init__(self, baseUrl, username, password, logLevel=logging.NOTSET):
        super(UpdatesLicensing, self).__init__(baseUrl, username, password, logLevel)
        UpdatesLicensing.logger.setLevel(logLevel)

    @abc.abstractmethod
    def getIsamVersion(self):
        pass

    #
    # Licensing and Activation
    #

    def createActivationOffering(self, code):
        methodName = "createActivationOffering()"
        UpdatesLicensing.logger.enterMethod(methodName)
        result = None

        jsonObj = {}
        Utils.addOnStringValue(jsonObj, "code", code)

        statusCode, content = self.httpPostJson(UpdatesLicensing.CAPABILITIES_V1, jsonObj)

        if statusCode == 200:
            result = True if content is None else content

        UpdatesLicensing.logger.exitMethod(methodName, str(result))
        return result

    def getActivationOffering(self, id):
        methodName = "getActivationOffering()"
        UpdatesLicensing.logger.enterMethod(methodName)
        result = None

        endpoint = "%s/%s/v1" % (UpdatesLicensing.CAPABILITIES, str(id))
        statusCode, content = self.httpGetJson(endpoint)

        if statusCode == 200 and content is not None:
            result = content

        UpdatesLicensing.logger.exitMethod(methodName, str(result))
        return result

    def getActivationOfferings(self):
        methodName = "getActivationOfferings()"
        UpdatesLicensing.logger.enterMethod(methodName)
        result = None

        statusCode, content = self.httpGetJson(UpdatesLicensing.CAPABILITIES_V1)

        if statusCode == 200 and content is not None:
            result = content

        UpdatesLicensing.logger.exitMethod(methodName, str(result))
        return result
