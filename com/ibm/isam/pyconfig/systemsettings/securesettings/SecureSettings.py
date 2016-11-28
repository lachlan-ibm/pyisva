"""
Created on Nov 25, 2016

@copyright: IBM
"""
from com.ibm.isam.util.RestClient import RestClient
from com.ibm.isam.util.Logger import Logger
import com.ibm.isam.util.Utils as Utils
import abc, logging, time

class SecureSettings(RestClient):
    __metaclass__ = abc.ABCMeta

    SSL_CERTIFICATES = "/isam/ssl_certificates"

    logger = Logger("SecureSettings")

    def __init__(self, baseUrl, username, password, logLevel=logging.NOTSET):
        super(SecureSettings, self).__init__(baseUrl, username, password, logLevel)
        SecureSettings.logger.setLevel(logLevel)

    @abc.abstractmethod
    def getIsamVersion(self):
        pass

    #
    # SSL Certificates
    #

    # Personal Certificates

    def importPersonalCertificate(self, kdbId, password, filePath):
        methodName = "importPersonalCertificate()"
        SecureSettings.logger.enterMethod(methodName)
        result = None

        try:
            with open(filePath, 'rb') as certificate:
                jsonObj = {}
                Utils.addOnStringValue(jsonObj, "operation", "import")
                Utils.addOnStringValue(jsonObj, "password", password)

                files = {"cert": certificate}

                endpoint = SecureSettings.SSL_CERTIFICATES + "/" + str(kdbId) + "/personal_cert"
                statusCode, content = self.httpPostFile(endpoint, data=jsonObj, files=files)

                if statusCode == 200:
                    result = True if content is None else content
        except IOError, e:
            SecureSettings.logger.error(methodName, str(e))

        SecureSettings.logger.exitMethod(methodName, str(result))
        return result

    # Signer Certificates

    def importSignerCertificate(self, kdbId, label, filePath):
        methodName = "importPersonalCertificate()"
        SecureSettings.logger.enterMethod(methodName)
        result = None

        try:
            with open(filePath, 'rb') as certificate:
                jsonObj = {}
                Utils.addOnStringValue(jsonObj, "label", label)

                files = {"cert": certificate}

                endpoint = SecureSettings.SSL_CERTIFICATES + "/" + str(kdbId) + "/signer_cert"
                statusCode, content = self.httpPostFile(endpoint, data=jsonObj, files=files)

                if statusCode == 200:
                    result = True if content is None else content
        except IOError, e:
            SecureSettings.logger.error(methodName, str(e))

        SecureSettings.logger.exitMethod(methodName, str(result))
        return result

    def loadSignerCertificate(self, kdbId, server, port, label):
        methodName = "loadSignerCertificate()"
        SecureSettings.logger.enterMethod(methodName)
        result = None

        jsonObj = {}
        Utils.addOnStringValue(jsonObj, "operation", "load")
        Utils.addOnStringValue(jsonObj, "label", label)
        Utils.addOnStringValue(jsonObj, "server", server)
        Utils.addOnValue(jsonObj, "port", port)

        endpoint = SecureSettings.SSL_CERTIFICATES + "/" + str(kdbId) + "/signer_cert"
        statusCode, content = self.httpPostJson(endpoint, jsonObj)

        if statusCode == 200:
            result = True if content is None else content

        SecureSettings.logger.exitMethod(methodName, str(result))
        return result
