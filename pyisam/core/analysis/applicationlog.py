""""
@copyright: IBM
"""

import logging

from pyisam.util.model import DataObject
from pyisam.util.restclient import RESTClient

APPLICATION_LOGS = "/isam/application_logs"

logger = logging.getLogger(__name__)


class ApplicationLog(object):

    def __init__(self, base_url, username, password):
        super(ApplicationLog, self).__init__()
        self.client = RESTClient(base_url, username, password)

    def get_application_log(self, path):
        parameters = DataObject()
        parameters.add_value_string("type", "File")

        endpoint = "%s/%s" % (APPLICATION_LOGS, path)

        response = self.client.get_json(endpoint, parameters.data)
        response.success = response.status_code == 200

        return response


    def delete_application_logs(self, paths=[]):
        files = DataObject()
        for path in paths:
            files.add_value_string("fullname", path)

        parameters = DataObject()
        parameters.add_value_not_empty("files", files.data)

        endpoint = "{}?action=delete".format(APPLICATION_LOGS)

        response = self.client.put_json(endpoint, parameters.data)
        response.success = response.status_code == 200

        return response


    def clear_application_logs(self, paths=[]):
        files = DataObject()
        for path in paths:
            files.add_value_string("fullname", path)

        parameters = DataObject()
        parameters.add_value_not_empty("files", files.data)

        endpoint = "{}?action=clear".format(APPLICATION_LOGS)

        response = self.client.put_json(endpoint, parameters.data)
        response.success = response.status_code == 200

        return response
