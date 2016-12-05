"""
Created on Nov 17, 2016

@copyright: IBM
"""

import json
import logging
from base64 import b64encode

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from .logger import Logger


class RestClient(object):

    ACCEPT = "Accept"
    ALL = "*/*"
    APPLICATION_JSON = "application/json"
    AUTHORIZATION = "Authorization"
    CONTENT_TYPE = "Content-type"
    MULTIPART_FORM = "multipart/form-data"

    logger = Logger("RestClient")

    def __init__(self, baseUrl, username=None, password=None, logLevel=logging.NOTSET):
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        RestClient.logger.setLevel(logLevel)

        self.__dumpJson = False
        self._baseUrl = baseUrl
        self._username = username
        self._password = password

    def enableJsonDump(self, enable=True):
        self.__dumpJson = enable

    def httpGet(self, endpoint, acceptType=ALL, contentType=APPLICATION_JSON, parameters=None):
        methodName = "httpGet()"
        RestClient.logger.enterMethod(methodName, (endpoint, parameters))

        url = self._baseUrl + endpoint
        headers = self.__getHeaders(acceptType, contentType)

        response = requests.get(url=url, params=parameters, headers=headers, verify=False)

        statusCode = response.status_code
        content = response._content

        response.close()

        RestClient.logger.exitMethod(methodName, (statusCode, content))
        return statusCode, content

    def httpGetJson(self, endpoint, parameters=None):
        statusCode, content = self.httpGet(endpoint, acceptType=RestClient.APPLICATION_JSON,
                                           parameters=parameters)
        return statusCode, self.__decodeJson(content)

    def httpPost(self, endpoint, acceptType=ALL, contentType=APPLICATION_JSON, parameters=None, data=""):
        methodName = "httpPost()"
        RestClient.logger.enterMethod(methodName, (endpoint, data))

        url = self._baseUrl + endpoint
        headers = self.__getHeaders(acceptType, contentType)

        response = requests.post(url=url, headers=headers, params=parameters, data=data, verify=False)

        statusCode = response.status_code
        content = response._content

        response.close()

        RestClient.logger.exitMethod(methodName, (statusCode, content))
        return statusCode, content

    def httpPostFile(self, endpoint, acceptType=APPLICATION_JSON, data="", files={}):
        methodName = "httpPostFile()"
        RestClient.logger.enterMethod(methodName, (endpoint, data))

        url = self._baseUrl + endpoint
        headers = self.__getHeaders(acceptType)

        response = requests.post(url=url, headers=headers, data=data, files=files, verify=False)

        statusCode = response.status_code
        content = response._content

        response.close()

        RestClient.logger.exitMethod(methodName, (statusCode, content))
        return statusCode, content

    def httpPostJson(self, endpoint, data=""):
        statusCode, content = self.httpPost(endpoint, acceptType=RestClient.APPLICATION_JSON,
                                            data=json.dumps(data))
        return statusCode, self.__decodeJson(content)

    def httpPut(self, endpoint, acceptType=ALL, contentType=APPLICATION_JSON, data=""):
        methodName = "httpPut()"
        RestClient.logger.enterMethod(methodName, (endpoint, data))

        url = self._baseUrl + endpoint
        headers = self.__getHeaders(acceptType, contentType)

        response = requests.put(url=url, headers=headers, params=None, data=data, verify=False)

        statusCode = response.status_code
        content = response._content

        response.close()

        RestClient.logger.exitMethod(methodName, (statusCode, content))
        return statusCode, content

    def httpPutJson(self, endpoint, data=""):
        statusCode, content = self.httpPut(endpoint, acceptType=RestClient.APPLICATION_JSON,
                                           data=json.dumps(data))
        return statusCode, self.__decodeJson(content)

    def httpDelete(self, endpoint, acceptType=ALL):
        methodName = "httpDelete()"
        RestClient.logger.enterMethod(methodName, (endpoint))

        url = self._baseUrl + endpoint
        headers = self.__getHeaders(acceptType)

        response = requests.delete(url=url, headers=headers, params=None, verify=False)

        statusCode = response.status_code
        content = response._content

        response.close()

        RestClient.logger.exitMethod(methodName, (statusCode, content))
        return statusCode, content

    def httpDeleteJson(self, endpoint):
        statusCode, content = self.httpDelete(endpoint, acceptType=RestClient.APPLICATION_JSON)
        return statusCode, self.__decodeJson(content)

    def waitOnHttpGet(self, endpoint, successCode=200, sleepInterval=3):
        methodName = "waitOnHttpGet()"
        RestClient.logger.enterMethod(methodName, (endpoint))

        message = "Waiting for a [%s] response from [%s]" % (str(successCode), str(endpoint))

        statusCode = 0
        while statusCode != successCode:
            try:
                statusCode, content = self.httpGet(endpoint, acceptType=None, contentType=None)
            except: # Ignore this
                pass

            if statusCode != successCode:
                RestClient.logger.trace(methodName, message)
                time.sleep(sleepInterval)

        RestClient.logger.exitMethod(methodName)

    def __decodeJson(self, content):
        try:
            jsonObj = json.loads(content)

            if self.__dumpJson:
                print(json.dumps(jsonObj, sort_keys=True, indent=4, separators=(',', ': ')))

            return jsonObj
        except:
            return content

    def __getHeaders(self, acceptType=None, contentType=None):
        headers = {}

        if acceptType is not None:
            headers[RestClient.ACCEPT] = acceptType

        if contentType is not None:
            headers[RestClient.CONTENT_TYPE] = contentType

        if self._username is not None and self._password is not None:
            credential = "%s:%s" % (self._username, self._password)
            credential_encode = b64encode(credential.encode())
            headers[RestClient.AUTHORIZATION] = "Basic " + str(credential_encode.decode()).rstrip()

        return headers
