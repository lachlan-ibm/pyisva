"""
@copyright: IBM
"""

import logging
import uuid

from pyisam.util.model import DataObject
from pyisam.util.restclient import RESTClient

ATTRIBUTE_SOURCES = "/mga/attribute_sources/"

logger = logging.getLogger(__name__)

class AttributeSources(object):

    def __init__(self, base_url, username, password):
        super(AttributeSources, self).__init__()
        self.client = RESTClient(base_url, username, password)

    def create_attribute_source(
            self, attribute_name=None, attribute_type=None,
            attribute_value=True, properties=None):

        data = DataObject()
        data.add_value_string("name", attribute_name)
        data.add_value_string("type", attribute_type)
        data.add_value_string("value", attribute_value)
        data.add_value("properties", properties)

        response = self.client.post_json(ATTRIBUTE_SOURCES, data.data)
        response.success = response.status_code == 201

        return response
