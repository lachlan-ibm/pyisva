"""
@copyright: IBM
"""

import logging

from pyisam.util.restclient import RestClient
import pyisam.util.common as Utils


AUTHENTICATION_MECHANISMS = "/iam/access/v8/authentication/mechanisms"
AUTHENTICATION_MECHANISM_TYPES = "/iam/access/v8/authentication/mechanism/types"
AUTHENTICATION_POLICIES = "/iam/access/v8/authentication/policies"

logger = logging.getLogger(__name__)


class Authentication(RestClient):

    def __init__(self, base_url, username, password):
        super(Authentication, self).__init__(base_url, username, password)

    def create_mechanism(
            self, description=None, name=None, uri=None, type_id=None,
            properties=None, attributes=None):
        #logger.enter()

        data = {}
        Utils.add_value_string(data, "description", description)
        Utils.add_value_string(data, "name", name)
        Utils.add_value_string(data, "uri", uri)
        Utils.add_value_string(data, "typeId", type_id)
        Utils.add_value(data, "properties", properties)
        Utils.add_value(data, "attributes", attributes)

        status_code, content = self.http_post_json(
            AUTHENTICATION_MECHANISMS, data=data)

        result = (status_code == 201, status_code, content)

        #logger.exit(result)
        return result

    def list_mechanism_types(
            self, sort_by=None, count=None, start=None, filter=None):
        #logger.enter()

        parameters = {}
        Utils.add_value_string(parameters, "sortBy", sort_by)
        Utils.add_value_string(parameters, "count", count)
        Utils.add_value_string(parameters, "start", start)
        Utils.add_value_string(parameters, "filter", filter)

        status_code, content = self.http_get_json(
            AUTHENTICATION_MECHANISM_TYPES, parameters=parameters)

        result = (status_code == 200, status_code, content)

        #logger.exit(result)
        return result

    def list_mechanisms(self, sort_by=None, count=None, start=None, filter=None):
        #logger.enter()

        parameters = {}
        Utils.add_value_string(parameters, "sortBy", sort_by)
        Utils.add_value_string(parameters, "count", count)
        Utils.add_value_string(parameters, "start", start)
        Utils.add_value_string(parameters, "filter", filter)

        status_code, content = self.http_get_json(
            AUTHENTICATION_MECHANISMS, parameters=parameters)

        result = (status_code == 200, status_code, content)

        #logger.exit(result)
        return result

    def update_mechanism(
            self, id, description=None, name=None, uri=None, type_id=None,
            predefined=None, properties=None, attributes=None):
        #logger.enter()

        data = {}
        Utils.add_value_string(data, "id", id)
        Utils.add_value_string(data, "description", description)
        Utils.add_value_string(data, "name", name)
        Utils.add_value_string(data, "uri", uri)
        Utils.add_value_string(data, "typeId", type_id)
        Utils.add_value(data, "predefined", predefined)
        Utils.add_value(data, "properties", properties)
        Utils.add_value(data, "attributes", attributes)

        endpoint = "%s/%s" % (AUTHENTICATION_MECHANISMS, id)
        status_code, content = self.http_put_json(endpoint, data=data)

        result = (status_code == 204, status_code, content)

        #logger.exit(result)
        return result

    def create_policy(
            self, name=None, policy=None, uri=None, description=None,
            dialect=None, id=None, user_last_modified=None, last_modified=None,
            date_created=None):
        #logger.enter()

        data = {}
        Utils.add_value_string(data, "name", name)
        Utils.add_value_string(data, "policy", policy)
        Utils.add_value_string(data, "uri", uri)
        Utils.add_value_string(data, "description", description)
        Utils.add_value_string(data, "dialect", dialect)
        Utils.add_value_string(data, "id", id)
        Utils.add_value_string(data, "userlastmodified", user_last_modified)
        Utils.add_value_string(data, "lastmodified", last_modified)
        Utils.add_value_string(data, "datecreated", date_created)

        status_code, content = self.http_post_json(
            AUTHENTICATION_POLICIES, data=data)

        result = (status_code == 201, status_code, content)

        #logger.exit(result)
        return result


class Authentication9021(Authentication):

    def __init__(self, base_url, username, password):
        super(Authentication9021, self).__init__(base_url, username, password)

    def create_policy(
            self, name=None, policy=None, uri=None, description=None,
            dialect=None, id=None, user_last_modified=None, last_modified=None,
            date_created=None, enabled=None):
        #logger.enter()

        data = {}
        Utils.add_value_string(data, "name", name)
        Utils.add_value_string(data, "policy", policy)
        Utils.add_value_string(data, "uri", uri)
        Utils.add_value_string(data, "description", description)
        Utils.add_value_string(data, "dialect", dialect)
        Utils.add_value_string(data, "id", id)
        Utils.add_value_string(data, "userlastmodified", user_last_modified)
        Utils.add_value_string(data, "lastmodified", last_modified)
        Utils.add_value_string(data, "datecreated", date_created)
        Utils.add_value(data, "enabled", enabled)

        status_code, content = self.http_post_json(
            AUTHENTICATION_POLICIES, data=data)

        result = (status_code == 201, status_code, content)

        #logger.exit(result)
        return result
