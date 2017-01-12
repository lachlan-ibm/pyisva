"""
@copyright: IBM
"""

import logging

from pyisam.util.restclient import RestClient
import pyisam.util.common as Utils


TEMPLATE_FILES = "/mga/template_files"

logger = logging.getLogger(__name__)


class TemplateFiles(RestClient):

    def __init__(self, base_url, username, password):
        super(TemplateFiles, self).__init__(base_url, username, password)

    def create_directory(self, path, dir_name=None):
        #logger.enter()

        data = {}
        Utils.add_value_string(data, "dir_name", dir_name)
        Utils.add_value_string(data, "type", "dir")

        endpoint = "%s/%s" % (TEMPLATE_FILES, path)
        status_code, content = self.http_post_json(endpoint, data=data)

        result = (status_code == 200, status_code, content)

        #logger.exit(result)
        return result

    def get_directory(self, path, recursive=None):
        #logger.enter()

        parameters = {}
        Utils.add_value(parameters, "recursive", recursive)

        endpoint = "%s/%s" % (TEMPLATE_FILES, path)
        status_code, content = self.http_get_json(
            endpoint, parameters=parameters)

        if status_code == 200:
            if isinstance(content, list):
                result = (True, status_code, content)
            else:
                result = (True, status_code, content.get("contents"))
        else:
            result = (False, status_code, content)

        #logger.exit(result)
        return result

    def create_file(self, path, file_name=None, contents=None):
        #logger.enter()

        data = {}
        Utils.add_value_string(data, "file_name", file_name)
        Utils.add_value_string(data, "contents", contents)
        Utils.add_value_string(data, "type", "file")

        endpoint = "%s/%s" % (TEMPLATE_FILES, path)
        status_code, content = self.http_post_json(endpoint, data=data)

        result = (status_code == 200, status_code, content)

        #logger.exit(result)
        return result

    def delete_file(self, path, file_name):
        #logger.enter()

        endpoint = ("%s/%s/%s" % (TEMPLATE_FILES, path, file_name))
        status_code, content = self.http_delete_json(endpoint)

        result = (status_code == 200, status_code, content)

        #logger.exit(result)
        return result

    def get_file(self, path, file_name):
        #logger.enter()

        endpoint = ("%s/%s/%s" % (TEMPLATE_FILES, path, file_name))
        status_code, content = self.http_get_json(endpoint)

        result = (status_code == 200, status_code, content)

        #logger.exit(result)
        return result

    def import_file(self, path, file_name, file_path):
        #logger.enter()
        result = (False, None, None)

        try:
            with open(file_path, 'rb') as template:
                files = {"file": template}

                endpoint = ("%s/%s/%s" % (TEMPLATE_FILES, path, file_name))
                status_code, content = self.http_post_file(
                    endpoint, files=files)

                result = (status_code == 200, status_code, content)
        except IOError as e:
            logger.error(e)

        #logger.exit(result)
        return result

    def import_files(self, file_path):
        #logger.enter()
        result = (False, None, None)

        try:
            with open(file_path, 'rb') as templates:
                files = {"file": templates}

                data = {}
                Utils.add_value(data, "force", True)

                status_code, content = self.http_post_file(
                    TEMPLATE_FILES, data=data, files=files)

                result = (status_code == 200, status_code, content)
        except IOError as e:
            logger.error(e)

        #logger.exit(result)
        return result

    def update_file(self, path, file_name, content=None):
        #logger.enter()

        data = {}
        Utils.add_value_string(data, "content", content)
        Utils.add_value_string(data, "type", "file")

        endpoint = ("%s/%s/%s" % (TEMPLATE_FILES, path, file_name))
        status_code, content = self.http_put_json(endpoint, data=data)

        result = (status_code == 200, status_code, content)

        #logger.exit(result)
        return result
