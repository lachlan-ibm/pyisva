"""
@copyright: IBM
"""

import logging

from pyisam.util.restclient import RestClient, APPLICATION_JSON, TEXT_HTML
import pyisam.util.common as Utils


CLIENTS = "/iam/access/v8/clients"
DEFINITIONS = "/iam/access/v8/definitions"
MAPPING_RULES = "/iam/access/v8/mapping-rules"

logger = logging.getLogger(__name__)


class APIProtection(RestClient):

    def __init__(self, base_url, username, password):
        super(APIProtection, self).__init__(base_url, username, password)

    def create_client(
            self, name=None, redirect_uri=None, company_name=None,
            company_url=None, contact_person=None, contact_type=None,
            email=None, phone=None, other_info=None, definition=None,
            client_id=None, client_secret=None):
        #logger.enter()

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

        #logger.exit(result)
        return result

    def delete_client(self, id):
        #logger.enter()

        endpoint = "%s/%s" % (CLIENTS, id)
        status_code, content = self.http_delete_json(endpoint)

        result = (status_code == 204, status_code, content)

        #logger.exit(result)
        return result

    def list_clients(self, sort_by=None, count=None, start=None, filter=None):
        #logger.enter()

        parameters = {}
        Utils.add_value_string(parameters, "sortBy", sort_by)
        Utils.add_value_string(parameters, "count", count)
        Utils.add_value_string(parameters, "start", start)
        Utils.add_value_string(parameters, "filter", filter)

        status_code, content = self.http_get_json(
            CLIENTS, parameters=parameters)

        result = (status_code == 200, status_code, content)

        #logger.exit(result)
        return result

    def create_definition(
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
        #logger.enter()

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

        #logger.exit(result)
        return result

    def delete_definition(self, id):
        #logger.enter()

        endpoint = "%s/%s" % (DEFINITIONS, id)
        status_code, content = self.http_delete_json(endpoint)

        result = (status_code == 204, status_code, content)

        #logger.exit(result)
        return result

    def list_definitions(
            self, sort_by=None, count=None, start=None, filter=None):
        #logger.enter()

        parameters = {}
        Utils.add_value_string(parameters, "sortBy", sort_by)
        Utils.add_value_string(parameters, "count", count)
        Utils.add_value_string(parameters, "start", start)
        Utils.add_value_string(parameters, "filter", filter)

        status_code, content = self.http_get_json(
            DEFINITIONS, parameters=parameters)

        result = (status_code == 200, status_code, content)

        #logger.exit(result)
        return result

    def create_mapping_rule(
            self, name=None, category=None, file_name=None, content=None):
        #logger.enter()

        data = {}
        Utils.add_value_string(data, "name", name)
        Utils.add_value_string(data, "category", category)
        Utils.add_value_string(data, "fileName", file_name)
        Utils.add_value_string(data, "content", content)

        status_code, content = self.http_post_json(MAPPING_RULES, data=data)

        result = (status_code == 201, status_code, content)

        #logger.exit(result)
        return result

    def list_mapping_rules(
            self, sort_by=None, count=None, start=None, filter=None):
        #logger.enter()

        parameters = {}
        Utils.add_value_string(parameters, "sortBy", sort_by)
        Utils.add_value_string(parameters, "count", count)
        Utils.add_value_string(parameters, "start", start)
        Utils.add_value_string(parameters, "filter", filter)

        status_code, content = self.http_get_json(
            MAPPING_RULES, parameters=parameters)

        result = (status_code == 200, status_code, content)

        #logger.exit(result)
        return result

    def import_mapping_rule(self, id, file_path):
        #logger.enter()
        result = (False, None, None)

        try:
            with open(file_path, 'rb') as mapping_rule:
                files = {"file": mapping_rule}

                endpoint = "%s/%s/file" % (MAPPING_RULES, id)
                accept_type = "%s,%s" % (APPLICATION_JSON, TEXT_HTML)
                status_code, content = self.http_post_file(
                    endpoint, accept_type=accept_type, files=files)

                result = (status_code == 200, status_code, content)
        except IOError as e:
            logger.error(e)

        #logger.exit(result)
        return result

    def update_mapping_rule(self, id, content=None):
        #logger.enter()

        data = {}
        Utils.add_value_string(data, "content", content)

        endpoint = "%s/%s" % (MAPPING_RULES, id)
        status_code, content = self.http_put_json(endpoint, data=data)

        result = (status_code == 204, status_code, content)

        #logger.exit(result)
        return result
