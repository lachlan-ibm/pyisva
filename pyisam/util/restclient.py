"""
@copyright: IBM
"""

import base64
import json
import logging
import requests
import time
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from .model import Response


logger = logging.getLogger(__name__)


class RESTClient(object):

    def __init__(self, base_url, username=None, password=None):
        super(RESTClient, self).__init__()
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        self._base_url = base_url
        self._username = username
        self._password = password

    def delete(self, endpoint, accept_type="*/*"):
        logger.debug("DELETE %s", endpoint)

        url = self._base_url + endpoint
        headers = self._get_headers(accept_type)

        r = requests.delete(url=url, headers=headers, params=None, verify=False)

        response = Response()
        response.data = r._content
        response.json = self._decode_json(response.data)
        response.status_code = r.status_code

        r.close()
        return response

    def delete_json(self, endpoint):
        return self.delete(endpoint, accept_type="application/json")

    def get(
            self, endpoint, accept_type="*/*", content_type="application/json",
            parameters=None):
        logger.debug("GET %s", endpoint)

        url = self._base_url + endpoint
        headers = self._get_headers(accept_type, content_type)

        r = requests.get(
            url=url, params=parameters, headers=headers, verify=False)

        response = Response()
        response.data = r._content
        response.json = self._decode_json(response.data)
        response.status_code = r.status_code

        r.close()
        return response

    def get_json(self, endpoint, parameters=None):
        return self.get(
            endpoint, accept_type="application/json", parameters=parameters)

    def get_wait(
            self, endpoint, status_code=200, iteration_wait=3,
            max_iterations=20):
        logger.debug("Waiting for %i response from %s", status_code, endpoint)

        response = Response()
        url = self._base_url + endpoint

        iteration = 1
        while response.status_code != status_code and (
                max_iterations is None or iteration <= max_iterations):
            logger.debug("#%i GET %s", iteration, endpoint)
            try:
                r = requests.get(url=url, verify=False, timeout=1)

                response.data = r._content
                response.status_code = r.status_code
                response.json = self._decode_json(response.data)

                r.close()
            except: # Ignore this
                pass

            if response.status_code != status_code:
                time.sleep(iteration_wait)
                iteration += 1

        return response

    def post(
            self, endpoint, accept_type="*/*", content_type="application/json",
            parameters=None, data=""):
        logger.debug("POST %s", endpoint)

        url = self._base_url + endpoint
        headers = self._get_headers(accept_type, content_type)

        r = requests.post(
            url=url, headers=headers, params=parameters, data=data,
            verify=False)

        response = Response()
        response.data = r._content
        response.json = self._decode_json(response.data)
        response.status_code = r.status_code

        r.close()
        return response

    def post_file(
            self, endpoint, accept_type="application/json", data="", files={}):
        logger.debug("POST %s", endpoint)

        url = self._base_url + endpoint
        headers = self._get_headers(accept_type)

        r = requests.post(
            url=url, headers=headers, data=data, files=files, verify=False)

        response = Response()
        response.data = r._content
        response.json = self._decode_json(response.data)
        response.status_code = r.status_code

        r.close()
        return response

    def post_json(self, endpoint, data=""):
        return self.post(
            endpoint, accept_type="application/json", data=json.dumps(data))

    def put(
            self, endpoint, accept_type="*/*", content_type="application/json",
            data=""):
        logger.debug("PUT %s", endpoint)

        url = self._base_url + endpoint
        headers = self._get_headers(accept_type, content_type)

        r = requests.put(
            url=url, headers=headers, params=None, data=data, verify=False)

        response = Response()
        response.data = r._content
        response.json = self._decode_json(response.data)
        response.status_code = r.status_code

        r.close()
        return response

    def put_json(self, endpoint, data=""):
        return self.put(
            endpoint, accept_type="application/json", data=json.dumps(data))

    def _decode_json(self, data):
        try:
            return json.loads(data)
        except:
            return None

    def _get_headers(self, accept_type=None, content_type=None):
        headers = {}

        if accept_type:
            headers["Accept"] = accept_type

        if content_type:
            headers["Content-type"] = content_type

        if self._username and self._password:
            credential = "%s:%s" % (self._username, self._password)
            credential_encode = base64.b64encode(credential.encode())
            authorization = "Basic " + str(credential_encode.decode()).rstrip()
            headers["Authorization"] = authorization

        return headers
