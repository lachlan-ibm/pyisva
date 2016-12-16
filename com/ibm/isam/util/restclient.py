"""
@copyright: IBM
"""

import json
import logging
from base64 import b64encode

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from .logger import Logger


ACCEPT = "Accept"
ALL = "*/*"
APPLICATION_JSON = "application/json"
AUTHORIZATION = "Authorization"
CONTENT_TYPE = "Content-type"


class RestClient(object):

    logger = Logger("RestClient")

    def __init__(
            self, base_url, username=None, password=None,
            log_level=logging.NOTSET):
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        RestClient.logger.set_level(log_level)

        self._dump_json = False
        self._base_url = base_url
        self._username = username
        self._password = password

    def enableJsonDump(self, enable=True):
        self._dump_json = enable

    def http_get(
            self, endpoint, accept_type=ALL, content_type=APPLICATION_JSON,
            parameters=None):
        RestClient.logger.enter(endpoint, parameters)

        url = self._base_url + endpoint
        headers = self._get_headers(accept_type, content_type)

        response = requests.get(
            url=url, params=parameters, headers=headers, verify=False)

        status_code = response.status_code
        content = self._decode_json(response._content)

        response.close()

        RestClient.logger.exit(status_code, content)
        return (status_code, content)

    def http_get_json(self, endpoint, parameters=None):
        return self.http_get(
            endpoint, accept_type=APPLICATION_JSON, parameters=parameters)

    def http_post(
            self, endpoint, accept_type=ALL, content_type=APPLICATION_JSON,
            parameters=None, data=""):
        RestClient.logger.enter(endpoint, data)

        url = self._base_url + endpoint
        headers = self._get_headers(accept_type, content_type)

        response = requests.post(
            url=url, headers=headers, params=parameters, data=data,
            verify=False)

        status_code = response.status_code
        content = self._decode_json(response._content)

        response.close()

        RestClient.logger.exit(status_code, content)
        return (status_code, content)

    def http_post_file(
            self, endpoint, accept_type=APPLICATION_JSON, data="", files={}):
        RestClient.logger.enter(endpoint, data)

        url = self._base_url + endpoint
        headers = self._get_headers(accept_type)

        response = requests.post(
            url=url, headers=headers, data=data, files=files, verify=False)

        status_code = response.status_code
        content = self._decode_json(response._content)

        response.close()

        RestClient.logger.exit(status_code, content)
        return (status_code, content)

    def http_post_json(self, endpoint, data=""):
        return self.http_post(
            endpoint, accept_type=APPLICATION_JSON, data=json.dumps(data))

    def http_put(
            self, endpoint, accept_type=ALL, content_type=APPLICATION_JSON,
            data=""):
        RestClient.logger.enter(endpoint, data)

        url = self._base_url + endpoint
        headers = self._get_headers(accept_type, content_type)

        response = requests.put(
            url=url, headers=headers, params=None, data=data, verify=False)

        status_code = response.status_code
        content = self._decode_json(response._content)

        response.close()

        RestClient.logger.exit(status_code, content)
        return (status_code, content)

    def http_put_json(self, endpoint, data=""):
        return self.http_put(
            endpoint, accept_type=APPLICATION_JSON, data=json.dumps(data))

    def http_delete(self, endpoint, accept_type=ALL):
        RestClient.logger.enter(endpoint)

        url = self._base_url + endpoint
        headers = self._get_headers(accept_type)

        response = requests.delete(
            url=url, headers=headers, params=None, verify=False)

        status_code = response.status_code
        content = self._decode_json(response._content)

        response.close()

        RestClient.logger.exit(status_code, content)
        return (status_code, content)

    def http_delete_json(self, endpoint):
        return self.http_delete(endpoint, accept_type=APPLICATION_JSON)

    def wait_on_http_get(self, endpoint, success_code=200, sleep_interval=3):
        RestClient.logger.enter(endpoint)

        status_code = 0
        while status_code != success_code:
            try:
                status_code, content = self.http_get(
                    endpoint, accept_type=None, content_type=None)
            except: # Ignore this
                pass

            if status_code != success_code:
                RestClient.logger.debug(
                    "Waiting for a %i response from %s", success_code, endpoint)
                time.sleep(sleep_interval)

        RestClient.logger.exit()

    def _decode_json(self, content):
        try:
            data = json.loads(content)

            if self._dump_json:
                print(json.dumps(
                    data, sort_keys=True, indent=4, separators=(',', ': ')))

            return data
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
