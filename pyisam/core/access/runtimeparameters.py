"""
@copyright: IBM
"""

import logging

from pyisam.util.model import DataObject
from pyisam.util.restclient import RESTClient


RUNTIME_TUNING = "/mga/runtime_tuning"
ENDPOINTS = "endpoints"

logger = logging.getLogger(__name__)


class RuntimeParameters(object):

    def __init__(self, base_url, username, password, docker):
        super(RuntimeParameters, self).__init__()
        self.client = RESTClient(base_url, username, password)
        self._docker = docker

    def update(self, parameter, value=None):
        data = DataObject()
        data.add_value("value", value)

        endpoint = "%s/%s/v1" % (RUNTIME_TUNING, parameter)

        response = self.client.put_json(endpoint, data.data)
        response.success = response.status_code == 200

        return response


    def get_runtime_tuning(self):
        endpoint = "%s/v1" % RUNTIME_TUNING

        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200

        return response

    def add_listening_interface(self, interface, port, secure=None):
        if self._docker:
            logger.warning("Runtime listening interfaces cannot be added on docker. No action is being performed.")
            response = {}
            response["success"] = True
        else:
            data = DataObject()
            data.add_value("interface", interface)
            data.add_value("port", port)
            data.add_value("secure", secure)

            endpoint = "%s/%s/v1" % (RUNTIME_TUNING, ENDPOINTS)

            response = self.client.post_json(endpoint, data.data)
            response.success = response.status_code == 200

        return response

    def delete_listening_interface(self, interface, port):
        if self._docker:
            logger.warning("Runtime listening interfaces cannot be removed on docker. No action is being performed.")
            response = {}
            response["success"] = True
        else:
            endpoint = "%s/%s/%s:%d/v1" % (RUNTIME_TUNING, ENDPOINTS, interface, port)

            response = self.client.delete_json(endpoint)
            response.success = response.status_code == 204

        return response
