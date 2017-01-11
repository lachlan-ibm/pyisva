"""
@copyright: IBM
"""

import logging

from pyisam.util.restclient import RestClient
import pyisam.util.common as Utils


ATTRIBUTE_MATCHERS = "/iam/access/v8/attribute-matchers"
ATTRIBUTES = "/iam/access/v8/attributes"

logger = logging.getLogger(__name__)


class Attributes(RestClient):

    def __init__(self, base_url, username, password):
        super(Attributes, self).__init__(base_url, username, password)

    def create_attribute(
            self, category=None, matcher=None, issuer=None, description=None,
            name=None, datatype=None, uri=None, storage_session=None,
            storage_behavior=None, storage_device=None, type_risk=None,
            type_policy=None):
        #logger.enter()

        storage_data = {}
        Utils.add_value(storage_data, "session", storage_session)
        Utils.add_value(storage_data, "behavior", storage_behavior)
        Utils.add_value(storage_data, "device", storage_device)

        type_data = {}
        Utils.add_value(type_data, "risk", type_risk)
        Utils.add_value(type_data, "policy", type_policy)

        data = {}
        Utils.add_value_string(data, "category", category)
        Utils.add_value_string(data, "matcher", matcher)
        Utils.add_value_string(data, "issuer", issuer)
        Utils.add_value_string(data, "description", description)
        Utils.add_value_string(data, "name", name)
        Utils.add_value_string(data, "datatype", datatype)
        Utils.add_value_string(data, "uri", uri)
        Utils.add_value(data, "predefined", False)
        Utils.add_value_not_empty(data, "storageDomain", storage_data)
        Utils.add_value_not_empty(data, "type", type_data)

        status_code, content = self.http_post_json(ATTRIBUTES, data=data)

        result = (status_code == 201, status_code, content)

        #logger.exit(result)
        return result

    def list_attributes(
            self, sort_by=None, count=None, start=None, filter=None):
        #logger.enter()

        parameters = {}
        Utils.add_value_string(parameters, "sortBy", sort_by)
        Utils.add_value_string(parameters, "count", count)
        Utils.add_value_string(parameters, "start", start)
        Utils.add_value_string(parameters, "filter", filter)

        status_code, content = self.http_get_json(
            ATTRIBUTES, parameters=parameters)

        result = (status_code == 200, status_code, content)

        #logger.exit(result)
        return result

    def list_attribute_matchers(self, sort_by=None, filter=None):
        #logger.enter()

        parameters = {}
        Utils.add_value_string(parameters, "sortBy", sort_by)
        Utils.add_value_string(parameters, "filter", filter)

        status_code, content = self.http_get_json(
            ATTRIBUTE_MATCHERS, parameters=parameters)

        result = (status_code == 200, status_code, content)

        #logger.exit(result)
        return result
