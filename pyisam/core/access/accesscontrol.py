"""
@copyright: IBM
"""

import logging

from pyisam.util.restclient import RestClient
import pyisam.util.common as Utils


POLICIES = "/iam/access/v8/policies"
POLICY_ATTACHMENTS = "/iam/access/v8/policyattachments"
POLICY_ATTACHMENTS_PDADMIN = "/iam/access/v8/policyattachments/pdadmin"

logger = logging.getLogger(__name__)


class AccessControl(RestClient):

    def __init__(self, base_url, username, password):
        super(AccessControl, self).__init__(base_url, username, password)

    def create_policy(
            self, name=None, description=None, dialect=None, policy=None,
            attributes_required=None):
        #logger.enter()

        data = {}
        Utils.add_value_string(data, "name", name)
        Utils.add_value_string(data, "description", description)
        Utils.add_value_string(data, "dialect", dialect)
        Utils.add_value_string(data, "policy", policy)
        Utils.add_value(data, "attributesrequired", attributes_required)
        Utils.add_value(data, "predefined", False)

        status_code, content = self.http_post_json(POLICIES, data=data)

        result = (status_code == 201, status_code, content)

        #logger.exit(result)
        return result

    def get_policies(self, sort_by=None, filter=None):
        #logger.enter()

        parameters = {}
        Utils.add_value_string(parameters, "sortBy", sort_by)
        Utils.add_value_string(parameters, "filter", filter)

        status_code, content = self.http_get_json(
            POLICIES, parameters=parameters)

        result = (status_code == 200, status_code, content)

        #logger.exit(result)
        return result

    def authenticate_security_access_manager(
            self, username=None, password=None, domain=None):
        #logger.enter()

        data = {}
        Utils.add_value_string(data, "username", username)
        Utils.add_value_string(data, "password", password)
        Utils.add_value_string(data, "domain", domain)
        Utils.add_value_string(data, "command", "setCredential")

        status_code, content = self.http_post_json(
            POLICY_ATTACHMENTS_PDADMIN, data=data)

        result = (status_code == 200, status_code, content)

        #logger.exit(result)
        return result

    def configure_resource(
            self, server=None, resource_uri=None,
            policy_combining_algorithm=None, policies=None):
        #logger.enter()

        data = {}
        Utils.add_value_string(data, "server", server)
        Utils.add_value_string(data, "resourceUri", resource_uri)
        Utils.add_value_string(
            data, "policyCombiningAlgorithm", policy_combining_algorithm)
        Utils.add_value(data, "policies", policies)

        status_code, content = self.http_post_json(
            POLICY_ATTACHMENTS, data=data)

        result = (status_code == 201, status_code, content)

        #logger.exit(result)
        return result

    def get_resources(self, sort_by=None, filter=None):
        #logger.enter()

        parameters = {}
        Utils.add_value_string(parameters, "sortBy", sort_by)
        Utils.add_value_string(parameters, "filter", filter)

        status_code, content = self.http_get_json(
            POLICY_ATTACHMENTS, parameters=parameters)

        result = (status_code == 200, status_code, content)

        #logger.exit(result)
        return result

    def publish_policy_attachment(self, id):
        #logger.enter()

        endpoint = "%s/deployment/%s" % (POLICY_ATTACHMENTS, id)
        status_code, content = self.http_put_json(endpoint)

        result = (status_code == 204, status_code, content)

        #logger.exit(result)
        return result
