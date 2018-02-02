"""
@copyright: IBM
"""

import logging
import uuid

from pyisam.util.model import DataObject
from pyisam.util.restclient import RESTClient

ACCESS_POLICY = "/iam/access/v8/access-policies/"

logger = logging.getLogger(__name__)

class AccessPolicy(object):

    def __init__(self, base_url, username, password):
        super(AccessPolicy, self).__init__()
        self.client = RESTClient(base_url, username, password)

    def get_policies(self, filter=None):

        endpoint = None
        if filter != None:
            endpoint = "%s?filter=%s" % (ACCESS_POLICY, filter)
        else:
            endpoint = ACCESS_POLICY


        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200

        return response

    def get_policy(self, policy_id=None):

        endpoint = "%s/%s" % (ACCESS_POLICY, policy_id)

        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200

        return response

    def create_policy(self, policy_name=None, category=None, policy_type="JavaScript", file_name=None):
        data = DataObject()

        try:
            with open(file_name, 'rb') as content:
                data.add_value_string('category',category)
                data.add_value_string('type',policy_type)
                data.add_value_string('name',policy_name)
                data.add_value_string("content", content.read().decode('utf-8'))
        except IOError as e:
            logger.error(e)
            response.success = False

        endpoint = ACCESS_POLICY
        response = self.client.post_json(endpoint, data.data)
        response.success = response.status_code == 201

        return response

    def update_policy(self, policy_id=None, file_name=None):
        data = DataObject()
        try:
            with open(file_name, 'rb') as content:
                data.add_value_string("content", content.read().decode('utf-8'))
        except IOError as e:
            logger.error(e)
            response.success = False

        endpoint = "%s/%s" % (ACCESS_POLICY, policy_id)
        response = self.client.put_json(endpoint, data.data)
        response.success = response.status_code == 204

        return response
