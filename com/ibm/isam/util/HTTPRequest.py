"""
Created on Nov 17, 2016

@copyright: IBM
"""
from base64 import b64encode
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

class ISAMRestClient(object):

    def __init__(self, username=None, password=None):
        self.username = username
        self.password = password
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

    def get(self, baseurl, endpoint, accept_type="*/*", parameters=None, content_type="application/json"):
        headers = self._getHeaders(accept_type, content_type)
        url = baseurl + endpoint

        response = requests.get(url=url, params=parameters, headers=headers, verify=False)

        statusCode = response.status_code
        contentHeader = response.headers
        content = response._content

        response.close()

        return statusCode, contentHeader, content

    def post(self, baseurl, endpoint, accept_type="*/*", jsonObj=""):
        headers = self._getHeaders(accept_type, "application/json")
        url = baseurl + endpoint

        response = requests.post(url=url, params=None, data=jsonObj, headers=headers, verify=False)

        statusCode = response.status_code
        contentHeader = response.headers
        content = response._content

        response.close()

        return statusCode, contentHeader, content

    def put(self, baseurl, endpoint, accept_type="*/*", jsonObj=""):
        headers = self._getHeaders(accept_type, "application/json")
        url = baseurl + endpoint

        response = requests.put(url=url, params=None, data=jsonObj, headers=headers, verify=False)

        statusCode = response.status_code
        contentHeader = response.headers
        content = response._content

        response.close()

        return statusCode, contentHeader, content

    def delete(self, baseurl, endpoint, accept_type="*/*"):
        headers = self._getHeaders(accept_type, "application/json")
        url = baseurl + endpoint

        response = requests.delete(url=url, params=None, headers=headers, verify=False)

        statusCode = response.status_code
        contentHeader = response.headers
        content = response._content

        response.close()

        return statusCode, contentHeader, content

    def _getHeaders(self, acceptType="application/json", contentType="application/json"):
        headers = {"Accept": acceptType, "Content-type": contentType}

        if self.username is not None and self.password is not None:
            credential_encode = b64encode("%s:%s" % (self.username, self.password))
            headers['Authorization'] = "Basic " + str(credential_encode).rstrip()

        return headers
