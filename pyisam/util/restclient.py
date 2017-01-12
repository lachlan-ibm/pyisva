"""
@copyright: IBM
"""

import json
import logging
import time
from base64 import b64encode

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning


ACCEPT = "Accept"
ALL = "*/*"
APPLICATION_JSON = "application/json"
AUTHORIZATION = "Authorization"
CONTENT_TYPE = "Content-type"
TEXT_HTML = "text/html"


logger = logging.getLogger(__name__)


class RestClient(object):

    def __init__(self, base_url, username=None, password=None):
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

        self._base_url = base_url
        self._username = username
        self._password = password

    def http_delete(self, endpoint, accept_type=ALL):
        logger.debug("DELETE %s", endpoint)

        url = self._base_url + endpoint
        headers = self._get_headers(accept_type)

        response = requests.delete(
            url=url, headers=headers, params=None, verify=False)

        status_code = response.status_code
        content = self._decode_json(response._content)

        response.close()

        return (status_code, content)

    def http_delete_json(self, endpoint):
        return self.http_delete(endpoint, accept_type=APPLICATION_JSON)

    def http_get(
            self, endpoint, accept_type=ALL, content_type=APPLICATION_JSON,
            parameters=None):
        logger.debug("GET %s", endpoint)

        url = self._base_url + endpoint
        headers = self._get_headers(accept_type, content_type)

        response = requests.get(
            url=url, params=parameters, headers=headers, verify=False)

        status_code = response.status_code
        content = self._decode_json(response._content)

        response.close()

        return (status_code, content)

    def http_get_json(self, endpoint, parameters=None):
        return self.http_get(
            endpoint, accept_type=APPLICATION_JSON, parameters=parameters)

    def http_get_wait(
            self, endpoint, success_code=200, poll_interval=3,
            max_number_polls=20):
        logger.debug("Waiting for %i response from %s", success_code, endpoint)

        url = self._base_url + endpoint
        status_code = 0
        content = ""

        poll_count = 0
        while status_code != success_code and (
                max_number_polls is None or poll_count < max_number_polls):
            logger.debug("GET %s", endpoint)
            try:
                response = requests.get(url=url, verify=False, timeout=1)
                status_code = response.status_code
                content = self._decode_json(response._content)
            except: # Ignore this
                pass
            logger.debug("Status Code: %i", status_code)

            if status_code != success_code:
                time.sleep(poll_interval)
                poll_count += 1

        return (status_code, content)

    def http_post(
            self, endpoint, accept_type=ALL, content_type=APPLICATION_JSON,
            parameters=None, data=""):
        logger.debug("POST %s", endpoint)

        url = self._base_url + endpoint
        headers = self._get_headers(accept_type, content_type)

        response = requests.post(
            url=url, headers=headers, params=parameters, data=data,
            verify=False)

        status_code = response.status_code
        content = self._decode_json(response._content)

        response.close()

        return (status_code, content)

    def http_post_file(
            self, endpoint, accept_type=APPLICATION_JSON, data="", files={}):
        logger.debug("POST %s", endpoint)

        url = self._base_url + endpoint
        headers = self._get_headers(accept_type)

        response = requests.post(
            url=url, headers=headers, data=data, files=files, verify=False)

        status_code = response.status_code
        content = self._decode_json(response._content)

        response.close()

        return (status_code, content)

    def http_post_json(self, endpoint, data=""):
        return self.http_post(
            endpoint, accept_type=APPLICATION_JSON, data=json.dumps(data))

    def http_put(
            self, endpoint, accept_type=ALL, content_type=APPLICATION_JSON,
            data=""):
        logger.debug("PUT %s", endpoint)

        url = self._base_url + endpoint
        headers = self._get_headers(accept_type, content_type)

        response = requests.put(
            url=url, headers=headers, params=None, data=data, verify=False)

        status_code = response.status_code
        content = self._decode_json(response._content)

        response.close()

        return (status_code, content)

    def http_put_json(self, endpoint, data=""):
        return self.http_put(
            endpoint, accept_type=APPLICATION_JSON, data=json.dumps(data))

    def _decode_json(self, content):
        try:
            return json.loads(content)
        except:
            return content

    def _get_headers(self, accept_type=None, content_type=None):
        headers = {}

        if accept_type:
            headers[ACCEPT] = accept_type

        if content_type:
            headers[CONTENT_TYPE] = content_type

        if self._username and self._password:
            credential = "%s:%s" % (self._username, self._password)
            credential_encode = b64encode(credential.encode())
            authorization = "Basic " + str(credential_encode.decode()).rstrip()
            headers[AUTHORIZATION] = authorization

        return headers
