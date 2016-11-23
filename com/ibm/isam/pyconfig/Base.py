"""
Created on Nov 17, 2016

@copyright: IBM
"""
from com.ibm.isam.util.HTTPRequest import ISAMRestClient
import json, logging

class Base(object):

    APPLICATION_JSON = "application/json"

    def __init__(self, baseUrl, username, password, logLevel=logging.ERROR):
        self.logger = logging.getLogger("Base")
        self.logger.setLevel(logLevel)

        self.BASE_URL = baseUrl
        self.USERNAME = username
        self.PASSWORD = password

    def addOnStringValue(self, dictionary, key, value):
        if value is not None:
            dictionary[key] = str(value)

    def addOnValue(self, dictionary, key, value):
        if value is not None:
            dictionary[key] = value

    def getJSON(self, description, endpoint, successCode=200, silent=False):
        self.logger.debug("GET to %s" % description)

        client = ISAMRestClient(username=self.USERNAME, password=self.PASSWORD)
        statusCode, contentHeader, content = client.get(self.BASE_URL, endpoint, self.APPLICATION_JSON)

        if statusCode == successCode:
            self._toDebug("Successful GET to %s." % description, content, statusCode)
        elif not silent:
            self._toWarning("Unsuccessful GET to %s." % description, content, statusCode)

        return statusCode, self._decodeJson(content)

    def logEntry(self, message):
        self.logger.info(message)

    def logFailed(self, message):
        self.logger.info("Failed: %s" % message)

    def logSuccess(self, message):
        self.logger.info("Success: %s" % message)

    def postJSON(self, description, endpoint, jsonObj="", successCode=200, silent=False):
        self.logger.debug("POST to %s [%s]" % (description, jsonObj))

        client = ISAMRestClient(username=self.USERNAME, password=self.PASSWORD)
        statusCode, contentHeader, content = client.post(self.BASE_URL, endpoint, self.APPLICATION_JSON, json.dumps(jsonObj))

        if statusCode == successCode:
            self._toDebug("Successful POST to %s." % description, content, statusCode)
        elif not silent:
            self._toWarning("Unsuccessful POST to %s." % description, content, statusCode)

        return statusCode, self._decodeJson(content)

    def putJSON(self, description, endpoint, jsonObj="", successCode=200, silent=False):
        self.logger.debug("PUT to %s [%s]" % (description, jsonObj))

        client = ISAMRestClient(username=self.USERNAME, password=self.PASSWORD)
        statusCode, contentHeader, content = client.put(self.BASE_URL, endpoint, self.APPLICATION_JSON, json.dumps(jsonObj))

        if statusCode == successCode:
            self._toDebug("Successful PUT to %s." % description, content, statusCode)
        elif not silent:
            self._toWarning("Unsuccessful PUT to %s." % description, content, statusCode)

        return statusCode, self._decodeJson(content)

    def _decodeJson(self, string):
        try:
            return json.loads(string)
        except:
            return None

    def _toDebug(self, message, content=None, statusCode=None):
        self.logger.debug("%s Content: [%s] Status Code: [%s]" % (message, content, statusCode))

    def _toWarning(self, message, content=None, statusCode=None):
        self.logger.warning("%s Content: [%s] Status Code: [%s]" % (message, content, statusCode))
