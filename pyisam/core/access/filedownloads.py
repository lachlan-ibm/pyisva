"""
@copyright: IBM
"""

import logging

from pyisam.util.model import DataObject
from pyisam.util.restclient import RESTClient

FILE_DOWNLOADS = "/isam/downloads"

logger = logging.getLogger(__name__)


class FileDownloads(object):

    def __init__(self, base_url, username, password):
        super(FileDownloads, self).__init__()
        self.client = RESTClient(base_url, username, password)

    def get_file(self, path, file_name):
        endpoint = ("%s/%s/%s" % (FILE_DOWNLOADS, path, file_name))

        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200

        return response

    def get_directory(self, path, recursive=None):
        parameters = DataObject()
        parameters.add_value("recursive", recursive)

        endpoint = "%s/%s" % (FILE_DOWNLOADS, path)

        response = self.client.get_json(endpoint, parameters.data)
        response.success == response.status_code == 200

        if response.success and isinstance(response.json, dict):
            response.json = response.json.get("contents", [])

        return response