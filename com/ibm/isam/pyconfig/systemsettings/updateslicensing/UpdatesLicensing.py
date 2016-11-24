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

    CAPABILITIES = "/isam/capabilities/v1"

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

        if len(code) == 39:
            jsonObj = {}
            Utils.addOnStringValue(jsonObj, "code", code)

            statusCode, content = self.httpPostJson(UpdatesLicensing.CAPABILITIES, jsonObj)

            if statusCode == 200:
                result = (content or True)
        else:
            UpdatesLicensing.logger.error(methodName, "Activation code is invalid [%s]" % code)

        UpdatesLicensing.logger.exitMethod(methodName, str(result))
        return result
