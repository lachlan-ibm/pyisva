"""
@copyright: IBM
"""

import logging

from pyisam.util.model import DataObject, Response
from pyisam.util.restclient import RESTClient

FILE_DOWNLOADS = "/isam/downloads"

logger = logging.getLogger(__name__)


class FileDownloads(object):

    def __init__(self, base_url, username, password):
        super(FileDownloads, self).__init__()
        self.client = RESTClient(base_url, username, password)

    def get(self, file_path, type=None):
        parameters = DataObject()
        parameters.add_value_string("type", type)

        endpoint = ("%s/%s" % (FILE_DOWNLOADS, file_path))

        response = Response()
        if type == "file":
            response = self.client.get(endpoint, parameters=parameters.data)
        else:
            response = self.client.get_json(endpoint, parameters.data)
        response.success = response.status_code == 200

        return response
