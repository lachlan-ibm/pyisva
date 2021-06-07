"""
@copyright: IBM
"""

import logging

from pyisam.util.model import DataObject, Response
from pyisam.util.restclient import RESTClient

STS_BASE = "/iam/access/v8/sts/"
STS_MODULES = STS_BASE + "modules"
STS_MODULE_TYPES = STS_BASE + "module-types"
STS_TEMPLATES = STS_BASE + "templates"
STS_CHAINS = STS_BASE + "chains"

logger = logging.getLogger(__name__)

class SecurityTokenService(object):

    def __init__(self, base_url, username, password):
        super(SecurityTokenService, self).__init__()
        self.client = RESTClient(base_url, username, password)

    def get_module_types(self):

        endpoint = STS_MODULE_TYPES

        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200

        return response

    def get_modules(self):

        endpoint = STS_MODULES

        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200

        return response

    def get_module(self, module_id):

        endpoint = "%s/%s" % (STS_MODULES, module_id)

        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200

        return response


    def get_templates(self):

        endpoint = STS_TEMPLATES

        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200

        return response

    def get_template(self, template_id):

        endpoint = "%s/%s" % (STS_TEMPLATES, template_id)

        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200

        return response

    def create_template(self, name, description=None, modules=[]):

        data = DataObject()
        data.add_value_string("name", name)
        data.add_value_string("description", description)
        data.add_value("chainItems", modules)

        response = self.client.post_json(STS_TEMPLATES, data.data)
        response.success = response.status_code == 201

        return response

    def delete_template(self, template_id):

        endpoint = "%s/%s" % (STS_TEMPLATES, template_id)

        response = self.client.delete_json(endpoint)
        response.success = response.status_code == 204

        return response


    def get_chains(self):

        response = self.client.get_json(STS_CHAINS)
        response.success = response.status_code == 200

        return response

    def get_chain(self, chain_id):

        endpoint = "%s/%s" % (STS_CHAINS, chain_id)

        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200

        return response

    def create_chain(self, name, description=None, template_id=None, request_type=None, 
                     applies_to=None, issuer=None, 
                     validate_requests=None, sign_responses=None, send_validation_confirmation=None, 
                     properties=[]):

        data = DataObject()
        data.add_value_string("name", name)
        data.add_value_string("description", description)
        data.add_value_string("chainId", template_id)
        data.add_value_string("requestType", request_type)

        data.add_value("appliesTo", {"address": applies_to})

        data.add_value("issuer", {"address": issuer})

        data.add_value_boolean("validateRequests", validate_requests)
        data.add_value_boolean("signResponses", sign_responses)
        data.add_value_boolean("sendValidationConfirmation", send_validation_confirmation)


        data.add_value("properties", {
            "self": properties
        })

        response = self.client.post_json(STS_CHAINS, data.data)
        response.success = response.status_code == 201

        return response

    def delete_chain(self, chain_id):

        endpoint = "%s/%s" % (STS_CHAINS, chain_id)

        response = self.client.delete_json(endpoint)
        response.success = response.status_code == 204

        return response

