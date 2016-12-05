"""
Created on Nov 25, 2016

@copyright: IBM
"""

import logging

from com.ibm.isam.util.logger import Logger
from com.ibm.isam.util.restclient import RestClient
import com.ibm.isam.util.utils as Utils


class _SecureSettings(RestClient):

    SSL_CERTIFICATES = "/isam/ssl_certificates"

    logger = Logger("SecureSettings")

    def __init__(self, baseUrl, username, password, logLevel=logging.NOTSET):
        super(_SecureSettings, self).__init__(baseUrl, username, password, logLevel)
        _SecureSettings.logger.setLevel(logLevel)

    #
    # SSL Certificates
    #

    # Personal

    def importSslCertificatePersonal(self, kdbId, password, filePath):
        methodName = "importSslCertificatePersonal()"
        _SecureSettings.logger.enterMethod(methodName)
        result = None

        try:
            with open(filePath, 'rb') as certificate:
                jsonObj = {}
                Utils.addOnStringValue(jsonObj, "operation", "import")
                Utils.addOnStringValue(jsonObj, "password", password)

                files = {"cert": certificate}

                endpoint = _SecureSettings.SSL_CERTIFICATES + "/" + str(kdbId) + "/personal_cert"
                statusCode, content = self.httpPostFile(endpoint, data=jsonObj, files=files)

                result = (statusCode == 200, statusCode, content)
        except IOError as ioe:
            _SecureSettings.logger.error(methodName, str(ioe))
            result = (False, None, None)

        _SecureSettings.logger.exitMethod(methodName, str(result))
        return result

    # Signer

    def importSslCertificateSigner(self, kdbId, label, filePath):
        methodName = "importSslCertificateSigner()"
        _SecureSettings.logger.enterMethod(methodName)
        result = None

        try:
            with open(filePath, 'rb') as certificate:
                jsonObj = {}
                Utils.addOnStringValue(jsonObj, "label", label)

                files = {"cert": certificate}

                endpoint = _SecureSettings.SSL_CERTIFICATES + "/" + str(kdbId) + "/signer_cert"
                statusCode, content = self.httpPostFile(endpoint, data=jsonObj, files=files)

                result = (statusCode == 200, statusCode, content)
        except IOError as ioe:
            _SecureSettings.logger.error(methodName, str(ioe))
            result = (False, None, None)

        _SecureSettings.logger.exitMethod(methodName, str(result))
        return result

    def loadSslCertificateSigner(self, kdbId, server, port, label):
        methodName = "loadSslCertificateSigner()"
        _SecureSettings.logger.enterMethod(methodName)
        result = None

        jsonObj = {}
        Utils.addOnStringValue(jsonObj, "operation", "load")
        Utils.addOnStringValue(jsonObj, "label", label)
        Utils.addOnStringValue(jsonObj, "server", server)
        Utils.addOnValue(jsonObj, "port", port)

        endpoint = _SecureSettings.SSL_CERTIFICATES + "/" + str(kdbId) + "/signer_cert"
        statusCode, content = self.httpPostJson(endpoint, jsonObj)

        result = (statusCode == 200, statusCode, content)

        _SecureSettings.logger.exitMethod(methodName, str(result))
        return result


class SecureSettings9020(_SecureSettings):

    logger = Logger("SecureSettings9020")

    def __init__(self, baseUrl, username, password, logLevel=logging.NOTSET):
        super(SecureSettings9020, self).__init__(baseUrl, username, password, logLevel)
        SecureSettings9020.logger.setLevel(logLevel)
