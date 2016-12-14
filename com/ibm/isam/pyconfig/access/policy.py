"""
@copyright: IBM
"""

import logging

from com.ibm.isam.util.logger import Logger
from com.ibm.isam.util.restclient import RestClient
import com.ibm.isam.util.utils as Utils


ATTRIBUTE_MATCHERS = "/iam/access/v8/attribute-matchers"
ATTRIBUTES = "/iam/access/v8/attributes"
AUTHENTICATION_MECHANISMS = "/iam/access/v8/authentication/mechanisms"
AUTHENTICATION_MECHANISM_TYPES = "/iam/access/v8/authentication/mechanism/types"
AUTHENTICATION_POLICIES = "/iam/access/v8/authentication/policies"
CLIENTS = "/iam/access/v8/clients"
DEFINITIONS = "/iam/access/v8/definitions"
MAPPING_RULES = "/iam/access/v8/mapping-rules"
POLICIES = "/iam/access/v8/policies"
POLICY_ATTACHMENTS = "/iam/access/v8/policyattachments"
POLICY_ATTACHMENTS_PDADMIN = "/iam/access/v8/policyattachments/pdadmin"
RISK_PROFILES = "/iam/access/v8/risk/profiles"


class Policy(RestClient):

    logger = Logger("Policy")

    def __init__(self, base_url, username, password, log_level=logging.NOTSET):
        super(Policy, self).__init__(base_url, username, password, log_level)
        Policy.logger.set_level(log_level)

    #
    # Access Control
    #

    # Policies

    def create_access_control_policy(
            self, name=None, description=None, dialect=None, policy=None,
            attributes_required=None):
        method_name = "create_access_control_policy()"
        Policy.logger.enter_method(method_name)
        result = None

        data = {}
        Utils.add_value_string(data, "name", name)
        Utils.add_value_string(data, "description", description)
        Utils.add_value_string(data, "dialect", dialect)
        Utils.add_value_string(data, "policy", policy)
        Utils.add_value(data, "attributesrequired", attributes_required)
        Utils.add_value(data, "predefined", False)

        status_code, content = self.http_post_json(POLICIES, data=data)

        result = (status_code == 201, status_code, content)

        Policy.logger.exit_method(method_name, result)
        return result

    def get_access_control_policies(self, sort_by=None, filter=None):
        method_name = "get_access_control_policies()"
        Policy.logger.enter_method(method_name)
        result = None

        parameters = {}
        Utils.add_value_string(parameters, "sortBy", sort_by)
        Utils.add_value_string(parameters, "filter", filter)

        status_code, content = self.http_get_json(
            POLICIES, parameters=parameters)

        result = (status_code == 200, status_code, content)

        Policy.logger.exit_method(method_name, result)
        return result

    # Policy Attachments

    def authenticate_security_access_manager(
            self, username=None, password=None, domain=None):
        method_name = "authenticate_security_access_manager()"
        Policy.logger.enter_method(method_name)
        result = None

        data = {}
        Utils.add_value_string(data, "username", username)
        Utils.add_value_string(data, "password", password)
        Utils.add_value_string(data, "domain", domain)
        Utils.add_value_string(data, "command", "setCredential")

        status_code, content = self.http_post_json(
            POLICY_ATTACHMENTS_PDADMIN, data=data)

        result = (status_code == 200, status_code, content)

        Policy.logger.exit_method(method_name, result)
        return result

    def create_access_control_policy_attachment(
            self, server=None, resource_uri=None,
            policy_combining_algorithm=None, policies=None):
        method_name = "create_access_control_policy_attachment()"
        Policy.logger.enter_method(method_name)
        result = None

        data = {}
        Utils.add_value_string(data, "server", server)
        Utils.add_value_string(data, "resourceUri", resource_uri)
        Utils.add_value_string(
            data, "policyCombiningAlgorithm", policy_combining_algorithm)
        Utils.add_value(data, "policies", policies)

        status_code, content = self.http_post_json(
            POLICY_ATTACHMENTS, data=data)

        result = (status_code == 201, status_code, content)

        Policy.logger.exit_method(method_name, result)
        return result

    def get_access_control_policy_attachment(self, sort_by=None, filter=None):
        method_name = "get_access_control_policy_attachment()"
        Policy.logger.enter_method(method_name)
        result = None

        parameters = {}
        Utils.add_value_string(parameters, "sortBy", sort_by)
        Utils.add_value_string(parameters, "filter", filter)

        status_code, content = self.http_get_json(
            POLICY_ATTACHMENTS, parameters=parameters)

        result = (status_code == 200, status_code, content)

        Policy.logger.exit_method(method_name, result)
        return result

    def publish_access_control_policy_attachment(self, id):
        method_name = "publish_access_control_policy_attachment()"
        Policy.logger.enter_method(method_name)
        result = None

        endpoint = "%s/deployment/%s" % (POLICY_ATTACHMENTS, id)
        status_code, content = self.http_put_json(endpoint)

        result = (status_code == 204, status_code, content)

        Policy.logger.exit_method(method_name, result)
        return result

    #
    # API Protection
    #

    # Clients

    def create_api_protection_client(
            self, name=None, redirect_uri=None, company_name=None,
            company_url=None, contact_person=None, contact_type=None,
            email=None, phone=None, other_info=None, definition=None,
            client_id=None, client_secret=None):
        method_name = "create_api_protection_client()"
        Policy.logger.enter_method(method_name)
        result = None

        data = {}
        Utils.add_value_string(data, "name", name)
        Utils.add_value_string(data, "redirectUri", redirect_uri)
        Utils.add_value_string(data, "companyName", company_name)
        Utils.add_value_string(data, "companyUrl", company_url)
        Utils.add_value_string(data, "contactPerson", contact_person)
        Utils.add_value_string(data, "contactType", contact_type)
        Utils.add_value_string(data, "email", email)
        Utils.add_value_string(data, "phone", phone)
        Utils.add_value_string(data, "otherInfo", other_info)
        Utils.add_value_string(data, "definition", definition)
        Utils.add_value_string(data, "clientId", client_id)
        Utils.add_value_string(data, "clientSecret", client_secret)

        status_code, content = self.http_post_json(CLIENTS, data=data)

        result = (status_code == 201, status_code, content)

        Policy.logger.exit_method(method_name, result)
        return result

    def delete_api_protection_client(self, id):
        method_name = "delete_api_protection_client()"
        Policy.logger.enter_method(method_name)
        result = None

        endpoint = "%s/%s" % (CLIENTS, id)
        status_code, content = self.http_delete_json(endpoint)

        result = (status_code == 204, status_code, content)

        Policy.logger.exit_method(method_name, result)
        return result

    def get_api_protection_client_by_client_id(self, client_id):
        method_name = "get_api_protection_client_by_client_id()"
        Policy.logger.enter_method(method_name)
        result = None

        filter = "clientId equals " + str(client_id)
        success, status_code, content = self.get_api_protection_clients(
            filter=filter)

        if success and content:
            result = (success, status_code, content[0])
        else:
            result = (False, status_code, content)

        Policy.logger.exit_method(method_name, result)
        return result

    def get_api_protection_clients(
            self, sort_by=None, count=None, start=None, filter=None):
        method_name = "get_api_protection_clients()"
        Policy.logger.enter_method(method_name)
        result = None

        parameters = {}
        Utils.add_value_string(parameters, "sortBy", sort_by)
        Utils.add_value_string(parameters, "count", count)
        Utils.add_value_string(parameters, "start", start)
        Utils.add_value_string(parameters, "filter", filter)

        status_code, content = self.http_get_json(
            CLIENTS, parameters=parameters)

        result = (status_code == 200, status_code, content)

        Policy.logger.exit_method(method_name, result)
        return result

    # Definitions

    def create_api_protection_definition(
            self, name=None, description=None, tcm_behavior=None,
            token_char_set=None, access_token_lifetime=None,
            access_token_length=None, authorization_code_lifetime=None,
            authorization_code_length=None, refresh_token_length=None,
            max_authorization_grant_lifetime=None, pin_length=None,
            enforce_single_use_authorization_grant=None,
            issue_refresh_token=None,
            enforce_single_access_token_per_grant=None,
            enable_multiple_refresh_tokens_for_fault_tolerance=None,
            pin_policy_enabled=None, grant_types=None):
        method_name = "create_api_protection_definition()"
        Policy.logger.enter_method(method_name)
        result = None

        data = {}
        Utils.add_value_string(data, "name", name)
        Utils.add_value_string(data, "description", description)
        Utils.add_value_string(data, "tcmBehavior", tcm_behavior)
        Utils.add_value_string(data, "tokenCharSet", token_char_set)
        Utils.add_value(data, "accessTokenLifetime", access_token_lifetime)
        Utils.add_value(data, "accessTokenLength", access_token_length)
        Utils.add_value(
            data, "authorizationCodeLifetime", authorization_code_lifetime)
        Utils.add_value(
            data, "authorizationCodeLength", authorization_code_length)
        Utils.add_value(data, "refreshTokenLength", refresh_token_length)
        Utils.add_value(
            data, "maxAuthorizationGrantLifetime",
            max_authorization_grant_lifetime)
        Utils.add_value(data, "pinLength", pin_length)
        Utils.add_value(
            data, "enforceSingleUseAuthorizationGrant",
            enforce_single_use_authorization_grant)
        Utils.add_value(data, "issueRefreshToken", issue_refresh_token)
        Utils.add_value(
            data, "enforceSingleAccessTokenPerGrant",
            enforce_single_access_token_per_grant)
        Utils.add_value(
            data, "enableMultipleRefreshTokensForFaultTolerance",
            enable_multiple_refresh_tokens_for_fault_tolerance)
        Utils.add_value(data, "pinPolicyEnabled", pin_policy_enabled)
        Utils.add_value(data, "grantTypes", grant_types)

        status_code, content = self.http_post_json(DEFINITIONS, data=data)

        result = (status_code == 201, status_code, content)

        Policy.logger.exit_method(method_name, result)
        return result

    def delete_api_protection_definition(self, id):
        method_name = "delete_api_protection_definition()"
        Policy.logger.enter_method(method_name)
        result = None

        endpoint = "%s/%s" % (DEFINITIONS, id)
        status_code, content = self.http_delete_json(endpoint)

        result = (status_code == 204, status_code, content)

        Policy.logger.exit_method(method_name, result)
        return result

    def get_api_protection_definition_by_name(self, name):
        method_name = "get_api_protection_definition_by_name()"
        Policy.logger.enter_method(method_name)
        result = None

        filter = "name equals " + name
        success, status_code, content = self.get_api_protection_definitions(
            filter=filter)

        if success and content:
            result = (success, status_code, content[0])
        else:
            result = (False, status_code, content)

        Policy.logger.exit_method(method_name, result)
        return result

    def get_api_protection_definitions(
            self, sort_by=None, count=None, start=None, filter=None):
        method_name = "get_api_protection_definitions()"
        Policy.logger.enter_method(method_name)
        result = None

        parameters = {}
        Utils.add_value_string(parameters, "sortBy", sort_by)
        Utils.add_value_string(parameters, "count", count)
        Utils.add_value_string(parameters, "start", start)
        Utils.add_value_string(parameters, "filter", filter)

        status_code, content = self.http_get_json(
            DEFINITIONS, parameters=parameters)

        result = (status_code == 200, status_code, content)

        Policy.logger.exit_method(method_name, result)
        return result

    # Mapping Rules

    def create_api_protection_mapping_rule(
            self, name=None, category=None, file_name=None, content=None):
        method_name = "create_api_protection_mapping_rule()"
        Policy.logger.enter_method(method_name)
        result = None

        data = {}
        Utils.add_value_string(data, "name", name)
        Utils.add_value_string(data, "category", category)
        Utils.add_value_string(data, "fileName", file_name)
        Utils.add_value_string(data, "content", content)

        status_code, content = self.http_post_json(MAPPING_RULES, data=data)

        result = (status_code == 200, status_code, content)

        Policy.logger.exit_method(method_name, result)
        return result

    def get_api_protection_mapping_rules(
            self, sort_by=None, count=None, start=None, filter=None):
        method_name = "get_api_protection_mapping_rules()"
        Policy.logger.enter_method(method_name)
        result = None

        parameters = {}
        Utils.add_value_string(parameters, "sortBy", sort_by)
        Utils.add_value_string(parameters, "count", count)
        Utils.add_value_string(parameters, "start", start)
        Utils.add_value_string(parameters, "filter", filter)

        status_code, content = self.http_get_json(
            MAPPING_RULES, parameters=parameters)

        result = (status_code == 200, status_code, content)

        Policy.logger.exit_method(method_name, result)
        return result

    def update_api_protection_mapping_rule(self, id, content=None):
        method_name = "update_api_protection_mapping_rule()"
        Policy.logger.enter_method(method_name)
        result = None

        data = {}
        Utils.add_value_string(data, "content", content)

        endpoint = "%s/%s" % (MAPPING_RULES, id)
        status_code, content = self.http_put_json(endpoint, data=data)

        result = (status_code == 204, status_code, content)

        Policy.logger.exit_method(method_name, result)
        return result

    #
    # Attributes
    #

    # Attributes

    def create_attribute(
            self, category=None, matcher=None, issuer=None, description=None,
            name=None, datatype=None, uri=None, storage_session=None,
            storage_behavior=None, storage_device=None, type_risk=None,
            type_policy=None):
        method_name = "create_attribute()"
        Policy.logger.enter_method(method_name)
        result = None

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

        Policy.logger.exit_method(method_name, result)
        return result

    def get_attribute_by_uri(self, uri):
        method_name = "get_attribute_by_uri()"
        Policy.logger.enter_method(method_name)
        result = None

        filter = "uri equals %s" % str(uri)
        success, status_code, content = self.get_attributes(filter=filter)

        if success and content:
            result = (success, status_code, content[0])
        else:
            result = (success, status_code, content)

        Policy.logger.exit_method(method_name, result)
        return result

    def get_attributes(self, sort_by=None, count=None, start=None, filter=None):
        method_name = "get_attributes()"
        Policy.logger.enter_method(method_name)
        result = None

        parameters = {}
        Utils.add_value_string(parameters, "sortBy", sort_by)
        Utils.add_value_string(parameters, "count", count)
        Utils.add_value_string(parameters, "start", start)
        Utils.add_value_string(parameters, "filter", filter)

        status_code, content = self.http_get_json(
            ATTRIBUTES, parameters=parameters)

        result = (status_code == 200, status_code, content)

        Policy.logger.exit_method(method_name, result)
        return result

    # Matchers

    def get_attribute_matcher_by_uri(self, uri):
        method_name = "get_attribute_matcher_by_uri()"
        Policy.logger.enter_method(method_name)
        result = None

        filter = "uri equals %s" % str(uri)
        success, status_code, content = self.getAttributeMatchers(
            filter=filter)

        if success and content:
            result = (success, status_code, content[0])
        else:
            result = (success, status_code, content)

        Policy.logger.exit_method(method_name, result)
        return result

    def get_attribute_matchers(self, sort_by=None, filter=None):
        method_name = "get_attribute_matchers()"
        Policy.logger.enter_method(method_name)
        result = None

        parameters = {}
        Utils.add_value_string(parameters, "sortBy", sort_by)
        Utils.add_value_string(parameters, "filter", filter)

        status_code, content = self.http_get_json(
            ATTRIBUTE_MATCHERS, parameters=parameters)

        result = (status_code == 200, status_code, content)

        Policy.logger.exit_method(method_name, result)
        return result

    #
    # Authentication
    #

    # Mechanisms

    def create_authentication_mechanism(
            self, description=None, name=None, uri=None, type_id=None,
            properties=None, attributes=None):
        method_name = "create_authentication_mechanism()"
        Policy.logger.enter_method(method_name)
        result = None

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

        Policy.logger.exit_method(method_name, result)
        return result

    def get_authentication_mechanism_by_uri(self, uri):
        method_name = "get_authentication_mechanism_by_uri()"
        Policy.logger.enter_method(method_name)
        result = None

        filter = "uri equals %s" % str(uri)
        success, status_code, content = self.get_authentication_mechanisms(
            filter=filter)

        if success and content:
            result = (success, status_code, content[0])
        else:
            result = (success, status_code, content)

        Policy.logger.exit_method(method_name, result)
        return result

    def get_authentication_mechanism_types(
            self, sort_by=None, count=None, start=None, filter=None):
        method_name = "get_authentication_mechanism_types()"
        Policy.logger.enter_method(method_name)
        result = None

        parameters = {}
        Utils.add_value_string(parameters, "sortBy", sort_by)
        Utils.add_value_string(parameters, "count", count)
        Utils.add_value_string(parameters, "start", start)
        Utils.add_value_string(parameters, "filter", filter)

        status_code, content = self.http_get_json(
            AUTHENTICATION_MECHANISM_TYPES, parameters=parameters)

        result = (status_code == 200, status_code, content)

        Policy.logger.exit_method(method_name, result)
        return result

    def get_authentication_mechanisms(
            self, sort_by=None, count=None, start=None, filter=None):
        method_name = "get_authentication_mechanisms()"
        Policy.logger.enter_method(method_name)
        result = None

        parameters = {}
        Utils.add_value_string(parameters, "sortBy", sort_by)
        Utils.add_value_string(parameters, "count", count)
        Utils.add_value_string(parameters, "start", start)
        Utils.add_value_string(parameters, "filter", filter)

        status_code, content = self.http_get_json(
            AUTHENTICATION_MECHANISMS, parameters=parameters)

        result = (status_code == 200, status_code, content)

        Policy.logger.exit_method(method_name, result)
        return result

    def update_authentication_mechanism(
            self, id, description=None, name=None, uri=None, type_id=None,
            predefined=None, properties=None, attributes=None):
        method_name = "update_authentication_mechanism()"
        Policy.logger.enter_method(method_name)
        result = None

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

        Policy.logger.exit_method(method_name, result)
        return result

    # Policies

    def create_authentication_policies(
            self, name=None, policy=None, uri=None, description=None,
            dialect=None, id=None, user_last_modified=None, last_modified=None,
            date_created=None):
        method_name = "create_authentication_policies()"
        Policy.logger.enter_method(method_name)
        result = None

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

        Policy.logger.exit_method(method_name, result)
        return result

    #
    # Risk Profiles
    #

    def create_risk_profile(
            self, description=None, name=None, active=None, attributes=None):
        method_name = "create_risk_profile()"
        Policy.logger.enter_method(method_name)
        result = None

        data = {}
        Utils.add_value_string(data, "description", description)
        Utils.add_value_string(data, "name", name)
        Utils.add_value(data, "active", active)
        Utils.add_value(data, "attributes", attributes)
        Utils.add_value(data, "predefined", False)

        status_code, content = self.http_post_json(RISK_PROFILES, data=data)

        result = (status_code == 201, status_code, content)

        Policy.logger.exit_method(method_name, result)
        return result
