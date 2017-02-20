"""
@copyright: IBM
"""

import logging

from pyisam.util.model import DataObject, Response
from pyisam.util.restclient import RESTClient


TEMPLATE_FILES = "/mga/template_files"

logger = logging.getLogger(__name__)


class TemplateFiles(object):

    def __init__(self, base_url, username, password):
        super(TemplateFiles, self).__init__()
        self.client = RESTClient(base_url, username, password)

    def create_directory(self, path, dir_name=None):
        data = DataObject()
        data.add_value_string("dir_name", dir_name)
        data.add_value_string("type", "dir")

        endpoint = "%s/%s" % (TEMPLATE_FILES, path)

        response = self.client.post_json(endpoint, data.data)
        response.success = response.status_code == 200

        return response

    def get_directory(self, path, recursive=None):
        parameters = DataObject()
        parameters.add_value("recursive", recursive)

        endpoint = "%s/%s" % (TEMPLATE_FILES, path)

        response = self.client.get_json(endpoint, parameters.data)
        response.success == response.status_code == 200

        if response.success and isinstance(response.json, dict):
            response.json = response.json.get("contents", [])

        return response

    def create_file(self, path, file_name=None, contents=None):
        data = DataObject()
        data.add_value_string("file_name", file_name)
        data.add_value_string("contents", contents)
        data.add_value_string("type", "file")

        endpoint = "%s/%s" % (TEMPLATE_FILES, path)

        response = self.client.post_json(endpoint, data.data)
        response.success = response.status_code == 200

        return response

    def delete_file(self, path, file_name):
        endpoint = ("%s/%s/%s" % (TEMPLATE_FILES, path, file_name))

        response = self.client.delete_json(endpoint)
        response.success = response.status_code == 200

        return response

    def get_file(self, path, file_name):
        endpoint = ("%s/%s/%s" % (TEMPLATE_FILES, path, file_name))

        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200

        return response

    def import_file(self, path, file_name, file_path):
        response = Response()

        try:
            with open(file_path, 'rb') as template:
                files = {"file": template}

                endpoint = ("%s/%s/%s" % (TEMPLATE_FILES, path, file_name))

                response = self.client.post_file(endpoint, files=files)
                response.success = response.status_code == 200
        except IOError as e:
            logger.error(e)
            response.success = False

        return response

    def import_files(self, file_path):
        response = Response()

        try:
            with open(file_path, 'rb') as templates:
                files = {"file": templates}

                data = DataObject()
                data.add_value("force", True)

                response = self.client.post_file(
                    TEMPLATE_FILES, data=data.data, files=files)
                response.success = response.status_code == 200
        except IOError as e:
            logger.error(e)
            response.success = False

        return response

    def update_file(self, path, file_name, contents=None):
        data = DataObject()
        data.add_value_string("contents", contents)
        data.add_value_string("type", "file")

        endpoint = ("%s/%s/%s" % (TEMPLATE_FILES, path, file_name))

        response = self.client.put_json(endpoint, data.data)
        response.success = response.status_code == 200

        return response
