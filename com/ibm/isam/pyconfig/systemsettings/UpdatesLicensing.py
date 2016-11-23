"""
Created on Nov 22, 2016

@copyright: IBM
"""
from com.ibm.isam.pyconfig.Base import Base
import logging, time, uuid

class UpdatesLicensing(Base):

    CAPABILITIES = "/isam/capabilities/v1"

    def __init__(self, baseUrl, username, password, logLevel=logging.ERROR):
        super(UpdatesLicensing, self).__init__(baseUrl, username, password)

        self.logger = logging.getLogger("UpdatesLicensing")
        self.logger.setLevel(logLevel)

    #
    # Licensing and Activation
    #

    def createActivationOffering(self, code):
        description = "Creating activation offering"
        self.logEntry(description)

        if len(code) == 39:
            jsonObj = {}
            self.addOnStringValue(jsonObj, "code", code)

            statusCode, content = self.postJSON("Activation Offering", self.CAPABILITIES, jsonObj)

            if statusCode == 200:
                self.logSuccess(description)
                return (content or True)
        else:
            self.logger.error("Activation code is invalid [%s]" % code)

        self.logFailed(description)
