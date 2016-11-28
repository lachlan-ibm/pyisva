"""
Created on Nov 17, 2016

@copyright: IBM
"""
from .Logger import Logger
from base64 import b64encode
import json, logging, requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

class RestClient(object):

    ACCEPT = "Accept"
    ALL = "*/*"
    APPLICATION_JSON = "application/json"
    AUTHORIZATION = "Authorization"
    CONTENT_TYPE = "Content-type"
    MULTIPART_FORM = "multipart/form-data"

    logger = Logger("RestClient")

    def __init__(self, baseUrl, username=None, password=None, logLevel=logging.NOTSET):
        RestClient.logger.setLevel(logLevel)

        self.baseUrl = baseUrl
        self.username = username
        self.password = password

        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

    def httpGet(self, endpoint, acceptType=ALL, parameters=None, contentType=APPLICATION_JSON):
        methodName = "httpGet()"
        RestClient.logger.enterMethod(methodName, (endpoint, parameters))

        headers = self._getHeaders(acceptType, contentType)

        url = self.baseUrl + endpoint
        response = requests.get(url=url, params=parameters, headers=headers, verify=False)

        statusCode = response.status_code
        content = response._content

        response.close()

        RestClient.logger.exitMethod(methodName, (statusCode, content))
        return statusCode, content

    def httpGetJson(self, endpoint):
        statusCode, content = self.httpGet(endpoint, RestClient.APPLICATION_JSON)
        return statusCode, self._decodeJson(content)

    def httpPost(self, endpoint, acceptType=ALL, data="", contentType=APPLICATION_JSON):
        methodName = "httpPost()"
        RestClient.logger.enterMethod(methodName, (endpoint, data))

        headers = self._getHeaders(acceptType, contentType)

        url = self.baseUrl + endpoint
        response = requests.post(url=url, params=None, data=data, headers=headers, verify=False)

        statusCode = response.status_code
        content = response._content

        response.close()

        RestClient.logger.exitMethod(methodName, (statusCode, content))
        return statusCode, content

    def httpPostFile(self, endpoint, acceptType=APPLICATION_JSON, data="", files={}):
        methodName = "httpPostFile()"
        RestClient.logger.enterMethod(methodName, (endpoint, data))

        headers = self._getHeaders(acceptType)

        url = self.baseUrl + endpoint
        response = requests.post(url=url, data=data, headers=headers, verify=False, files=files)

        statusCode = response.status_code
        content = response._content

        response.close()

        RestClient.logger.exitMethod(methodName, (statusCode, content))
        return statusCode, content

    def httpPostJson(self, endpoint, jsonObj=""):
        statusCode, content = self.httpPost(endpoint, RestClient.APPLICATION_JSON, json.dumps(jsonObj))
        return statusCode, self._decodeJson(content)

    def httpPut(self, endpoint, acceptType=ALL, data="", contentType=APPLICATION_JSON):
        methodName = "httpPut()"
        RestClient.logger.enterMethod(methodName, (endpoint, data))

        headers = self._getHeaders(acceptType, contentType)

        url = self.baseUrl + endpoint
        response = requests.put(url=url, params=None, data=data, headers=headers, verify=False)

        statusCode = response.status_code
        content = response._content

        response.close()

        RestClient.logger.exitMethod(methodName, (statusCode, content))
        return statusCode, content

    def httpPutJson(self, endpoint, jsonObj=""):
        statusCode, content = self.httpPut(endpoint, RestClient.APPLICATION_JSON, json.dumps(jsonObj))
        return statusCode, self._decodeJson(content)

    def httpDelete(self, endpoint, acceptType=ALL):
        methodName = "httpDelete()"
        RestClient.logger.enterMethod(methodName, (endpoint))

        headers = self._getHeaders(acceptType, RestClient.APPLICATION_JSON)

        url = self.baseUrl + endpoint
        response = requests.delete(url=url, params=None, headers=headers, verify=False)

        statusCode = response.status_code
        content = response._content

        response.close()

        RestClient.logger.exitMethod(methodName, (statusCode, content))
        return statusCode, content

    def httpDeleteJson(self, endpoint):
        statusCode, content = self.httpDelete(endpoint, RestClient.APPLICATION_JSON)
        return statusCode, self._decodeJson(content)

    def _decodeJson(self, content):
        try:
            return json.loads(content)
        except:
            return None

    def _getHeaders(self, acceptType=None, contentType=None):
        headers = {}

        if acceptType is not None:
            headers[RestClient.ACCEPT] = acceptType

        if contentType is not None:
            headers[RestClient.CONTENT_TYPE] = contentType

        if self.username is not None and self.password is not None:
            credential = "%s:%s" % (self.username, self.password)
            credential_encode = b64encode(credential.encode())
            headers[RestClient.AUTHORIZATION] = "Basic " + str(credential_encode.decode()).rstrip()

        return headers
