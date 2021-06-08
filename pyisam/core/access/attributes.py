"""
@copyright: IBM
"""

import logging

from pyisam.util.model import DataObject
from pyisam.util.restclient import RESTClient


ATTRIBUTE_MATCHERS = "/iam/access/v8/attribute-matchers"
ATTRIBUTES = "/iam/access/v8/attributes"

logger = logging.getLogger(__name__)


class Attributes(object):

    def __init__(self, base_url, username, password):
        super(Attributes, self).__init__()
        self.client = RESTClient(base_url, username, password)

    def create_attribute(
            self, category=None, matcher=None, issuer=None, description=None,
            name=None, datatype=None, uri=None, storage_session=None,
            storage_behavior=None, storage_device=None, type_risk=None,
            type_policy=None):
        '''
        Create an CBA attribute.

        Args:
            category (:obj:`str`): The part of the XACML request that the attribute value comes from.
            matcher (:obj:`str`): ID of the attribute matcher.
            issuer (:obj:`str`): The name of the policy information point from which the value of the attribute is retrieved.
            description (:obj:`str`, optional): Description of the attribute.
            name (:obj:`str`): Name of the attribute
            datatype (:obj:`str`): The type of values that the attribute can accept.
            uri (:obj:`str`): The identifier of the attribute that is used in the generated XACML policy.
            storage_session (bool): True if the attribute is collected in the user session.
            storage_behavior (bool): True if historic data for this attribute is stored in the database and used for behavior-based attribute matching.
            storage_device (bool): True if the attribute is stored when a device is registered as part of the device fingerprint.
            type_risk (bool): True if the attribute is used in risk profiles.
            type_policy (bool): True if the attribute is used in policies.

        Returns:
            :obj:`~requests.Response`: The response from verify access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the id of the created obligation can be acess from the 
            response.id_from_location attribute

        '''
        storage_data = DataObject()
        storage_data.add_value("session", storage_session)
        storage_data.add_value("behavior", storage_behavior)
        storage_data.add_value("device", storage_device)

        type_data = DataObject()
        type_data.add_value("risk", type_risk)
        type_data.add_value("policy", type_policy)

        data = DataObject()
        data.add_value_string("category", category)
        data.add_value_string("matcher", matcher)
        data.add_value_string("issuer", issuer)
        data.add_value_string("description", description)
        data.add_value_string("name", name)
        data.add_value_string("datatype", datatype)
        data.add_value_string("uri", uri)
        data.add_value("predefined", False)
        data.add_value_not_empty("storageDomain", storage_data.data)
        data.add_value_not_empty("type", type_data.data)

        response = self.client.post_json(ATTRIBUTES, data.data)
        response.success = response.status_code == 201

        return response

    def list_attributes(self, sort_by=None, count=None, start=None, filter=None):
        '''
        Get a list of the configured attributes.

        Args:
            sort_by (:obj:`str`, optional): Attribute to sort results by.
            count (:obj:`str`, optional): Maximum number of results to fetch.
            start (:obj:`str`, optional): Pagenation offset of returned results.
            filter (:obj:`str`): Attribute to filter results by.

        Returns:
            :obj:`~requests.Response`: The response from verify access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the obligations are returned as JSON and can be accessed from
            the response.json attribute

        '''
        parameters = DataObject()
        parameters.add_value_string("sortBy", sort_by)
        parameters.add_value_string("count", count)
        parameters.add_value_string("start", start)
        parameters.add_value_string("filter", filter)

        response = self.client.get_json(ATTRIBUTES, parameters.data)
        response.success = response.status_code == 200

        return response

    def list_attribute_matchers(self, sort_by=None, filter=None):
        '''
        Get a list of the configured attribute matchers.

        Args:
            sort_by (:obj:`str`, optional): Attribute to sort results by.
            filter (:obj:`str`): Attribute to filter results by.

        Returns:
            :obj:`~requests.Response`: The response from verify access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the obligations are returned as JSON and can be accessed from
            the response.json attribute

        '''
        parameters = DataObject()
        parameters.add_value_string("sortBy", sort_by)
        parameters.add_value_string("filter", filter)

        response = self.client.get_json(ATTRIBUTE_MATCHERS, parameters.data)
        response.success = response.status_code == 200

        return response
