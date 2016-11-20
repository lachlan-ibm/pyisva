"""
Created on Nov 17, 2016

@copyright: IBM
"""
from com.ibm.isam.util.HTTPRequest import ISAMRestClient
import json, logging

class Common(object):

    APPLICATION_JSON = "application/json"

    def __init__(self, baseUrl, username, password, logLevel=logging.INFO):
        self.logger = logging.getLogger("Common")
        self.logger.setLevel(logLevel)

        self.BASE_URL = baseUrl
        self.USERNAME = username
        self.PASSWORD = password

    def changeAdminPassword(self, newPassword):
        self.PASSWORD = newPassword

    def checkPassword(self, password=None):
        if password is None:
            password = self.PASSWORD

        client = ISAMRestClient(username=self.USERNAME, password=password)
        statusCode, contentHeader, content = client.get(self.BASE_URL, "/setup_complete", self.APPLICATION_JSON)
        return statusCode == 200

    def _getJSON(self, description, endpoint, successCode=200, silent=False):
        self.logger.debug("GET to %s" % description)

        client = ISAMRestClient(username=self.USERNAME, password=self.PASSWORD)
        statusCode, contentHeader, content = client.get(self.BASE_URL, endpoint, self.APPLICATION_JSON)

        if statusCode == successCode:
            self._toDebug("Successful GET to %s." % description, content, statusCode)
            return statusCode, json.loads(content)
        elif not silent:
            self._toError("Unsuccessful GET to %s." % description, content, statusCode)

        return statusCode, None

    def _postJSON(self, description, endpoint, jsonObj="", successCode=200, silent=False):
        self.logger.debug("POST to %s [%s]" % (description, jsonObj))

        client = ISAMRestClient(username=self.USERNAME, password=self.PASSWORD)
        statusCode, contentHeader, content = client.post(self.BASE_URL, endpoint, self.APPLICATION_JSON, json.dumps(jsonObj))

        if statusCode == successCode:
            self._toDebug("Successful POST to %s." % description, content, statusCode)
            return statusCode, json.loads(content)
        elif not silent:
            self._toError("Unsuccessful POST to %s." % description, content, statusCode)

        return statusCode, None

    def _putJSON(self, description, endpoint, jsonObj="", successCode=200, silent=False):
        self.logger.debug("PUT to %s [%s]" % (description, jsonObj))

        client = ISAMRestClient(username=self.USERNAME, password=self.PASSWORD)
        statusCode, contentHeader, content = client.put(self.BASE_URL, endpoint, self.APPLICATION_JSON, json.dumps(jsonObj))

        if statusCode == successCode:
            self._toDebug("Successful PUT to %s." % description, content, statusCode)
            return statusCode, True
        elif not silent:
            self._toError("Unsuccessful PUT to %s." % description, content, statusCode)

        return statusCode, None

    def _logFailed(self, message):
        self.logger.error("Failed: %s" % message)

    def _logSuccess(self, message):
        self.logger.info("Success: %s" % message)

    def _toDebug(self, message, content=None, statusCode=None):
        self.logger.debug("%s Content: [%s] Status Code: [%s]" % (message, content, statusCode))

    def _toError(self, message, content=None, statusCode=None):
        self.logger.error("%s Content: [%s] Status Code: [%s]" % (message, content, statusCode))
