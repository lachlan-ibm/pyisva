"""
@copyright: IBM
"""

import logging

from pyisam.util.model import DataObject
from pyisam.util.restclient import RESTClient


POLICIES = "/iam/access/v8/policies"
POLICY_ATTACHMENTS = "/iam/access/v8/policyattachments"
POLICY_ATTACHMENTS_PDADMIN = "/iam/access/v8/policyattachments/pdadmin"

logger = logging.getLogger(__name__)


class AccessControl(object):

    def __init__(self, base_url, username, password):
        super(AccessControl, self).__init__()
        self.client = RESTClient(base_url, username, password)

    def create_policy(
            self, name=None, description=None, dialect=None, policy=None,
            attributes_required=None):
        data = DataObject()
        data.add_value_string("name", name)
        data.add_value_string("description", description)
        data.add_value_string("dialect", dialect)
        data.add_value_string("policy", policy)
        data.add_value("attributesrequired", attributes_required)
        data.add_value("predefined", False)

        response = self.client.post_json(POLICIES, data.data)
        response.success = response.status_code == 201

        return response

    def delete_policy(
            self, id=None):
        endpoint = "%s/%s" % (POLICIES, id)
        response = self.client.delete_json(endpoint)
        response.success = response.status_code == 204

        return response

    def list_policies(self, sort_by=None, filter=None):
        parameters = DataObject()
        parameters.add_value_string("sortBy", sort_by)
        parameters.add_value_string("filter", filter)

        response = self.client.get_json(POLICIES, parameters.data)
        response.success = response.status_code == 200

        return response

    def authenticate_security_access_manager(
            self, username=None, password=None, domain=None):
        data = DataObject()
        data.add_value_string("username", username)
        data.add_value_string("password", password)
        data.add_value_string("domain", domain)
        data.add_value_string("command", "setCredential")

        response = self.client.post_json(POLICY_ATTACHMENTS_PDADMIN, data.data)
        response.success = response.status_code == 200

        return response

    def configure_resource(
            self, server=None, resource_uri=None,
            policy_combining_algorithm=None, policies=None):
        data = DataObject()
        data.add_value_string("server", server)
        data.add_value_string("resourceUri", resource_uri)
        data.add_value_string(
            "policyCombiningAlgorithm", policy_combining_algorithm)
        data.add_value("policies", policies)

        response = self.client.post_json(POLICY_ATTACHMENTS, data.data)
        response.success = response.status_code == 201

        return response

    def remove_resource(
            self, id):
        endpoint = "%s/%s" % (POLICY_ATTACHMENTS, id)
        response = self.client.delete_json(endpoint)
        response.success = response.status_code == 204

        return response

    def list_resources(self, sort_by=None, filter=None):
        parameters = DataObject()
        parameters.add_value_string("sortBy", sort_by)
        parameters.add_value_string("filter", filter)

        response = self.client.get_json(POLICY_ATTACHMENTS, parameters.data)
        response.success = response.status_code == 200

        return response

    def publish_policy_attachment(self, id):
        endpoint = "%s/deployment/%s" % (POLICY_ATTACHMENTS, id)

        response = self.client.put_json(endpoint)
        response.success = response.status_code == 204

        return response
