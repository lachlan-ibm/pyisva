"""
@copyright: IBM
"""

import logging
import uuid
import json

from pyisva.util.model import DataObject
from pyisva.util.restclient import RESTClient

FEDERATIONS = "/iam/access/v8/federations/"

logger = logging.getLogger(__name__)

class Federations(object):

    def __init__(self, base_url, username, password):
        super(Federations, self).__init__()
        self.client = RESTClient(base_url, username, password)

    def create_oidc_federation(self, name=None, role=None, redirect_uri_prefix=None, response_types_supported=None, 
            attribute_mappings=[], identity_delegate_id=None, identity_rule_type="JAVASCRIPT", identity_mapping_rule=None, 
            identity_applies_to=None, identity_auth_type=None, identity_ba_user=None, identity_ba_password=None,
            identity_client_keystore=None, identity_client_key_alias=None, identity_issuer_uri=None, 
            identity_message_format=None, identity_ssl_keystore=None, identity_uri=None, adv_delegate_id=None,
            adv_rule_type="JAVASCRIPT", adv_mapping_rule=None):
        """
        Create an OIDC Federation.

        Args:
            name (:obj:`str`): 	A meaningful name to identify this federation.
            role (:obj:`str`): The role of a federation, valid values are "ip", "sp", "op" and "rp".
            redirect_uri_prefix (:obj:`str`): The reverse proxy address to prepend to the redirect URI sent to the provider to 
                                              communicate with this instance.
            response_types_supported (:obj:`str`): List of response types which determine the flow to be executed. Valid values 
                                                   to be included are "code", "token", "id_token". This selects the default flow
                                                   to run when a metadata URL is specified in the partner configuration.
            attribute_mappings (:obj:`list` of :obj:`dict`): The attribute mapping data. format 
                                                            is::

                                                                [
                                                                    {"name":"email",
                                                                     "source":"ldap_email"
                                                                    },
                                                                    {"name":"mobile",
                                                                     "source":"ldap_phone"
                                                                    }
                                                                ]

            identity_delegate_id (:obj:`str`): The active mapping module instance.
            identity_rule_type (:obj:`str`): The type of the mapping rule. The only supported type currently is "JAVASCRIPT".
            identity_mapping_rule (:obj:`str`): A reference to an ID of an identity mapping rule. 
            identity_applies_to (:obj:`str`): Refers to the STS chain that consumes callout responses. Required if WSTRUST 
                                              messageFormat is specified, ignored otherwise.
            identity_auth_type (:obj:`str`): Authentication method used when contacting external service. Supported 
                            values are NONE, BASIC or CERTIFICATE.
            identity_ba_user (:obj:`str`): Username for authentication to external service. Required if BASIC authType 
                            is specified, ignored otherwise.
            identity_ba_password (:obj:`str`): Password for authentication to external service. Required if BASIC 
                            authType is specified, ignored otherwise.
            identity_client_keystore (:obj:`str`): Contains key for HTTPS client authentication. Required if CERTIFICATE 
                            authType is specified, ignored otherwise.
            identity_client_key_alias (:obj:`str`): Alias of the key for HTTPS client authentication. Required if 
                            CERTIFICATE authType is specified, ignored otherwise.
            identity_issuer_uri (:obj:`str`): Refers to STS chain that provides input for callout request. Required if 
                            WSTRUST messageFormat is specified, ignored otherwise.
            identity_message_format (:obj:`str`): Message format of callout request. Supported values are XML or WSTRUST.
            identity_ssl_keystore (:obj:`str`): SSL certificate trust store to use when validating SSL certificate of 
                            external service.
            identity_uri (:obj:`str`): Address of destination server to call out to. 
            adv_delegate_id (:obj:`str`): The active module instance. Valid values are "skip-advance-map" and "default-map".
            adv_rule_type (:obj:`str`): The type of the mapping rule. The only supported type currently is JAVASCRIPT.
            adv_mapping_rule (:obj:`str`): A reference to an ID of an advance configuration mapping rule.

        Returns:
            :obj:`~requests.Response`: The response from verify access. 

            Success can be checked by examining the response.success boolean attribute.

            If the request is successful the id of the created obligation can be access from the
            response.id_from_location attribute.

        """
        attributeMapping = DataObject()
        attributeMapping.add_value_not_empty("map", attribute_mappings)

        advConfig = DataObject()
        advConfig.add_value_string("activeDelegateId", adv_delegate_id)
        advConfigProps = DataObject()
        advConfigProps.add_value_string("ruleType", adv_rule_type)
        advConfigProps.add_value_string("advanceMappingRuleReference", adv_mapping_rule)
        advConfig.add_value_not_empty("properties", advConfigProps.data)

        identityMapping = DataObject()
        identityMapping.add_value_string("activeDelegateId", identity_delegate_id)
        properties = DataObject()
        if identity_delegate_id == "default-map":
            properties.add_value_string("ruleType", identity_rule_type)
            properties.add_value_string("identityMappingRuleReference", identity_mapping_rule_reference)

        elif identity_delegate_id == "default-http-custom-map":
            properties.add_value_string("appliesTo", identity_applies_to)
            properties.add_value_string("authType", identity_auth_type)
            properties.add_value_string("basicAuthUsername", identity_ba_user)
            properties.add_value_string("basicAuthPassword", identity_ba_password)
            properties.add_value_string("clientKeyStore", identity_client_keystore)
            properties.add_value_string("clientKeyAlias", identity_client_key_alias)
            properties.add_value_string("issuerUri", identity_issuer_uri)
            properties.add_value_string("messageFormat", identity_message_format)
            properties.add_value_string("sslKeyStore", identity_ssl_keystore)
            properties.add_value_string("uri", identity_uri)
        identityMapping.add_value_not_empty("properties", properties.data)

        configuration = DataObject()
        configuration.add_value_not_empty("identityMapping", identityMapping.data)
        configuration.add_value_not_empty("attributeMapping", attributeMapping.data)
        configuration.add_value_not_empty("advancedConfiguration", advConfig.data)
        configuration.add_value_string("redirectUriPrefix", redirect_uri_prefix)
        configuration.add_value_string("responseTypes", response_types_supported)

        data = DataObject()
        data.add_value_string("name", name)
        data.add_value_string("protocol", "OIDC")
        data.add_value_string("role", role)
        data.add_value_not_empty("configuration", configuration.data)

        response = self.client.post_json(FEDERATIONS, data.data)
        response.success = response.status_code == 201

        return response


    def create_oidc_partner(self, federation_id, name=None, role="rp", redirect_uri_prefix=None,
        response_types=[], attribute_mappings=[], identity_delegate_id=None, identity_mapping_rule=None,
        identity_auth_type=None, identity_ba_user=None, identity_ba_password=None, identity_client_keystore=None, 
        identity_client_key_alias=None, identity_issuer_uri=None, identity_msg_fmt=None, identity_ssl_keystore=None,
        identity_uri=None, adv_config_delegate_id=None, adv_config_rule_type="JAVASCRIPT", adv_config_mapping_rule=None):
        """
        Add a partner configuration to an ODIC RP.

        Args:
            federation_id (:obj:`str`): The id of the ODIC federation to create a partner for.
            name (:obj:`str`): The name o the partner to be created.
            role (:obj:`str`, optional): The role this partner plays in its federation. Default is "rp"
            response_types (:obj:`str`, optional): List of response type which determines which flow to be executed.
            attribute_mappings (:obj:`list` of :obj:`dict`, optional): List of configured attribute sources. Format of
                            dictionary is::

                                                [
                                                    {"name":"email", 
                                                     "source": "ldap"
                                                    }, 
                                                    {"name":"preferred_name", 
                                                     "source":"credential"
                                                    }
                                                ]

            identity_delegate_id (:obj:`str`): The active mapping module instance. Valid values are "skip-identity-map", 
                                               "default-map" and "default-http-custom-map".
            identity_mapping_rule (:obj:`str`): A reference to an ID of an identity mapping rule.
            identity_auth_type (:obj:`str`, optional): Authentication method used when contacting external service. Supported 
                                                       values are NONE, BASIC or CERTIFICATE.
            identity_ba_user (:obj:`str`, optional): Username for authentication to external service.
            identity_ba_password (:obj:`str`, optional): Password for authentication to external service.
            identity_client_keystore (:obj:`str`, optional): Contains key for HTTPS client authentication.
            identity_client_key_alias (:obj:`str`, optional): Alias of the key for HTTPS client authentication.
            identity_issuer_uri (:obj:`str`, optional): Refers to STS chain that provides input for callout request.
            identity_msg_fmt (:obj:`str`, optional): Message format of callout request.
            identity_ssl_keystore (:obj:`str`, optional): SSL certificate trust store to use when validating SSL 
                                                          certificate of external service.
            identity_uri (:obj:`str`): Address of destination server to call out to.
            adv_config_delegate_id (:obj:`str`): The active module instance. Valid values are "skip-advance-map" and 
                                                 "default-map".
            adv_config_rule_type (:obj:`str`, optional): The type of the mapping rule. The only supported type currently 
                                                         is "JAVASCRIPT".
            adv_config_mapping_rule (:obj:`str`, optional): A reference to an ID of an advance configuration.

        Returns:
            :obj:`~requests.Response`: The response from verify access. 

            Success can be checked by examining the response.success boolean attribute.

            If the request is successful the id of the created obligation can be access from the
            response.id_from_location attribute.

        """
        data = DataObject()
        data.add_value_string("name", name)
        data.add_value_string("role", role)

        identityMapping = DataObject()
        identityMapping.add_value_string("activeDelegateId", identity_delegate_id)
        identityProps = DataObject()
        if identity_mapping_rule:
            identityProps.add_value_string("identityMappingRuleReference", identity_mapping_rule)
            identityProps.add_value_string("ruleType", "JAVASCRIPT")
        else:
            identityProps.add_value_string("authType", identity_auth_type)
            identityProps.add_value_string("basicAuthUsername", identity_ba_user)
            identityProps.add_value_string("basicAuthPassword", identity_ba_password)
            identityProps.add_value_string("clientKeyStore", identity_client_keystore)
            identityProps.add_value_string("clientKeyAlias", identity_client_key_alias)
            identityProps.add_value_string("issuerUri", identity_issuer_uri)
            identityProps.add_value_string("messageFormat", identity_msg_fmt)
            identityProps.add_value_string("sslKeyStore", identity_ssl_keystore)
            identityProps.add_value_string("uri", identity_uri)
        identityMapping.add_value_not_empty("properties", identityProps.data)

        advConfig = DataObject()
        advConfProps = DataObject()
        advConfProps.add_value_string("ruleType", adv_config_rule_type)
        advConfProps.add_value_string("advanceMappingRuleReference", adv_config_mapping_rule)
        advConfig.add_value_not_empty("properties", advConfProps.data)
        advConfig.add_value_string("activeDelegateId", adv_config_delegate_id)

        configuration = DataObject()
        configuration.add_value_not_empty("advanceConfiguration", advConfig.data)
        configuration.add_value_not_empty("identityMapping", identityMapping.data)
        attributeMapping = DataObject()
        attributeMapping.add_value_not_empty("map", attribute_mappings)
        configuration.add_value_not_empty("attributeMapping", attributeMapping.data)
        configuration.add_value_string("redirect_uri_prefix", redirect_uri_prefix)
        configuration.add_value_not_empty("responseTypes", response_types)

        data.add_value_not_empty("configuration", configuration.data)

        endpoint = "%s/%s/partners" % (FEDERATIONS, federation_id)

        response = self.client.post_json(endpoint, data.data)
        response.success = response.status_code == 201

        return response


    def create_saml_federation(self, name=None, role=None, template_name=None, access_policy=None, artifact_lifetime=None, 
            assertion_attr_types=[], assertion_session_not_on_or_after=None, assertion_multi_attr_stmt=None, 
            assertion_valid_before=None, assertion_valid_after=None, artifact_resolution_service=[], attribute_mappings=[], 
            company_name=None, encrypt_block_alg=None, encrypt_key_transport_alg=None, encrypt_key_alias=None, 
            encrypt_key_store=None, encrypt_name_id=None, encrypt_assertions=None, encrypt_assertion_attrs=None, 
            decrypt_key_alias=None, decrypt_key_store=None, identity_delegate_id=None, identity_rule_type='JAVASCRIPT', 
            identity_rule_id=None, identity_applies_to=None, identity_auth_type=None, identity_ba_user=None, 
            identity_ba_password=None, identity_client_keystore=None, identity_client_key_alias=None, identity_issuer_uri=None, 
            identity_msg_fmt=None, identity_ssl_keystore=None, identity_uri=None, ext_delegate_id=None, ext_mapping_rule=None, 
            manage_name_id_services=[], msg_valid_time=None, msg_issuer_fmt=None, msg_issuer_name_qualifier=None, 
            name_id_default=None, name_id_supported=[], consent_to_federate=True, exclude_session_index_logout_request=False, 
            poc_url=None, provider_id=None, session_timeout=None, sign_alg=None, sign_digest_alg=None, sign_valid_key_store=None, 
            sign_valid_key_alias=None, sign_assertion=None, sign_auth_rsp=None, sign_arti_req=None, sign_arti_rsp=None, 
            sign_logout_req=None, sign_logout_rsp=None, sign_name_id_req=None, sign_name_id_rsp=None, validate_auth_req=None,
            validate_assert=None, validate_arti_req=None, validate_arti_rsp=None, validate_logout_req=None, validate_logout_rsp=None,
            validate_name_id_req=None, validate_name_id_rsp=None, transform_include_namespace=None, sign_include_pubkey=None,
            sign_include_cert=None, sign_include_issuer=None, sign_include_ski=None, sign_include_subject=None, sign_keystore=None,
            sign_key_alias=None, sso_svc_data=[], slo_svc_data=[], alias_svc_db_type=None, alias_svc_ldap_con=None,
            alias_svc_ldap_base_dn=None, assertion_consume_svc=[], authn_req_delegate_id=None, authn_req_mr=None):
        """
        Create a SAML 2.0 IDP or SP federation.

        Args:
            name (:obj:`str`): The name of the federation
            role (:obj:`str`): The role of a federation: "ip" for a SAML 2.0 identity provider federation, and "sp" for 
                            a SAML 2.0 service provider federation.
            template_name (:obj:`str`): An identifier for the template on which to base this federation.
            access_policy (:obj:`str`, optional): The access policy that should be applied during single sign-on.
            artifact_lifetime(`int`, optional): The number of seconds that an artifact is valid. The default value is 120.
            assertion_attr_types (:obj:`list` of :obj:`str`, optional): A setting that specifies the types of attributes 
                            to include in the assertion.
            assertion_session_not_on_or_after (`int`, optional): The number of seconds that the security context established for 
                            the principal should be discarded by the service provider.The default value is 3600.
            assertion_mult_attr_stmt (`bool`, optional): A setting that specifies whether to keep multiple attribute 
                            statements in the groups in which they were received.
            assertion_valid_before (`int`, optional): The number of seconds before the issue date that an assertion is 
                            considered valid.
            assertion_valid_after (`int`, optional): The number of seconds the assertion is valid after being issued.
            artifact_resolution_service (:obj:`list` of :obj:`dict`, optional): Endpoints where artifacts are exchanged 
                            for actual SAML messages. Required if artifact binding is enabled. Format of artifact 
                            resolution service data is::

                                                        [
                                                            {"binding":"soap",
                                                             "default":false,
                                                             "index":0,
                                                             "url":"https://demo.com/endpoint"
                                                            },
                                                            {"binding":"soap",
                                                             "default":true,
                                                             "index":1,
                                                             "url":"https://domain.com/endpoint"
                                                            }
                                                        ]

            attribute_mappings (:obj:`list` of :obj:`dict`, optional): The attribute mapping data. format 
                            is::

                                [
                                    {"name":"email",
                                     "source":"ldap_email"
                                    },
                                    {"name":"mobile",
                                     "source":"ldap_phone"
                                    }
                                ]

            company_name (:obj:`str`, optional): The name of the company that creates the identity provider or service 
                            provider.
            encrypt_block_alg (:obj:`str`, optional): Block encryption algorithm used to encrypt and decrypt SAML message.
            encrypt_key_transport_alg (:obj:`str`): Key transport algorithm used to encrypt and decrypt keys.
            encrypt_key_alias (:obj:`str`, optional): The certificate for encryption of outgoing SAML messages.
            encrypt_key_store (:obj:`str`, optioanl): The certificate database name.
            encrypt_name_id (`bool`, optional): A setting that specifies whether the name identifiers should be encrypted.
            encrypt_assertions (`bool`, optional): A setting that specifies whether to encrypt assertions.
            encrypt_assertion_attrs (`bool`, optional): A setting that specifies whether to encrypt assertion attributes
            decrypt_key_alias (:obj:`str`, optional): A public/private key pair that the federation partners can use to
                            encrypt certain message content.
            decrypt_key_store (:obj:`str`, optional): The certificate database name.
            identity_delegate_id (:obj:`str`): The active identity mapping module instance.
            identity_rule_type (:obj:`str`): The type of the mapping rule. The only supported type currently is JAVASCRIPT.
            identity_rule_id (:obj:`str`): A reference to an ID of an identity mapping rule.
            identity_applies_to (:obj:`str`): Refers to STS chain that consumes callout response.
            identity_auth_type (:obj:`str`): Authentication method used when contacting external service.
            identity_ba_user (:obj:`str`, optional): Username for authentication to external service.
            identity_ba_password (:obj:`str`, optional): Password for authentication to external service.
            identity_client_keystore (:obj:`str`, optional): Contains key for HTTPS client authentication.
            identity_client_key_alias (:obj:`str`, optional): Alias of the key for HTTPS client authentication.
            identity_issuer_uri (:obj:`str`): Refers to STS chain that provides input for callout request.
            identity_msg_fmt (:obj:`str`): Message format of callout request. Supported values are XML or WSTRUST.
            identity_ssl_keystore (:obj:`str`): SSL certificate trust store to use when validating SSL certificate of 
                            external service.
            identity_uri (:obj:`str`): Address of destination server to call out to.
            ext_delegate_id (:obj:`str`): The active extension mapping module instance.
            ext_mapping_rule (:obj:`str`): A reference to an ID of an extension mapping rule.
            manage_name_id_services (:obj:`list` of :obj:`dict`): Endpoints that accept SAML name ID management requests or responses.
            msg_valid_time (`int`, optional): The number of seconds that a message is valid. The default value is 300.
            msg_issuer_fmt (:obj:`str`, optional): The format of the issuer of SAML message.
            msg_issuer_name_qualifier (:obj:`str`): The name qualifier of the issuer of SAML messaged.
            name_id_default (:obj:`str`): The name identifier format to use when the format attribute is not set, or is 
                            set to ``urn:oasis:names:tc:SAML:1.1:nameid-format:unspecified``.
            name_id_supported (:obj:`list` of :obj:`str`): The list of supported name identifier formats.
            consent_to_federate (`bool`, optional): A setting that specifies whether to ask user's consent before linking 
                            the account.
            exclude_session_index_logout_request (`bool`, optional): A setting that specifies whether the LogoutRequest 
                            messages sent out from this entity will exclude SessionIndex during IP init SLO flow. 
                            The default value is false.
            poc_url (:obj:`str`): The endpoint URL of the point of contact server.
            provider_id (:obj:`str`, optional): A unique identifier that identifies the provider to its partner provider.
            session_timeout (`int`, optional): The number of seconds that the SAML session remains valid. 
                            The default value is 7200.
            sign_alg (:obj:`str`): The signature algorithm to sign and validate SAML messages and assertions.
            sign_digest_alg (:obj:`str`): The hash algorithm to apply to the transformed resources and validate its 
                            integrity.
            sign_valid_key_store (:obj:`str`, optional): The certificate validation database name.
            sign_valid_key_alias (:obj:`str`, optional): The signer certificate label used to validate the signatures 
                            on the incoming SAML assertions and messages.
            sign_assertion (`bool`, optional): A setting that specifies whether to sign the assertion. 
                            The default value is false.
            sign_auth_rsp (`bool`, optional): A setting that specifies whether to sign the authentication responses. 
                            The default value is false.
            sign_arti_req (`bool`, optional): A setting that specifies whether to sign the artifact request. 
                            The default value is false.
            sign_arti_rsp (`bool`, optional): A setting that specifies whether to sign the artifact response. 
                            The default value is false.
            sign_logout_req (`bool`, optional): A setting that specifies whether to sign the logout request. 
                            The default value is false.
            sign_logout_rsp (`bool`, optional): A setting that specifies whether to sign the logout response. 
                            The default value is false.
            sign_name_id_req (`bool`, optional): A setting that specifies whether to sign the name ID management request. 
                            The default value is false.
            sign_name_id_rsp (`bool`, optional): A setting that specifies whether to sign the name ID management response. 
                            The default value is false.
            validate_auth_req (`bool`, optional): A setting that specifies whether to validate the digital signature of 
                            an authentication request. The default value is false.
            validate_assert (`bool`, optional): A setting that specifies whether to validate the digital signature of 
                            an assertion. The default value is false.
            validate_arti_req (`bool`): A setting that specifies whether to validate the digital signature of an 
                            artifact request.
            validate_arti_rsp (`bool`): A setting that specifies whether to validate the digital signature of an 
                            artifact response.
            validate_logout_req (`bool`): A setting that specifies whether to validate the digital signature of a 
                            logout request.
            validate_logout_rsp (`bool`): A setting that specifies whether to validate the digital signature of a 
                            logout response.
            validate_name_id_req (`bool`): A setting that specifies whether to validate the digital signature of a name 
                            ID management request.
            validate_name_id_rsp (`bool`): A setting that specifies whether to validate the digital signature of a name 
                            ID management response.
            transform_include_namespace (`bool`, optional): A setting that specifies whether to include the 
                            InclusiveNamespaces element in the digital signature.
            sign_include_pubkey (:`bool`, optional): A setting that specifies whether to include the public key in the 
                            KeyInfo element in the digital signature when signing a SAML message or assertion. 
                            The default value is false.
            sign_include_cert (`bool`, optional): A setting that specifies whether to include the base 64 encoded 
                            certificate data to be included in the KeyInfo element in the digital signature when signing 
                            a SAML message or assertion. The default value is true.
            sign_include_issuer (`bool`, optional): A setting that specifies whether to include the issuer name and the 
                            certificate serial number in the KeyInfo element in the digital signature when signing a 
                            SAML message or assertion. The default value is false.
            sign_include_ski (`bool`, optional): A setting that specifies whether to include the X.509 subject key 
                            identifier in the KeyInfo element in the digital signature when signing a SAML message or 
                            assertion. The default value is false.
            sign_include_subject (`bool`, optional): A setting that specifies whether to include the subject name in the 
                            KeyInfo element in the digital signature when signing a SAML message or assertion. 
                            The default value is false.
            sign_keystore (:obj:`str`, optional): The certificate database which contains the private key used to sign
                            messages.
            sign_key_alias (:obj:`str`, optional): The personal public/private key pair for signing the SAML messages 
                            and the assertion. If not provided, the default value is null.
            sso_svc_data (:obj:`list` of :obj:`dict`): Endpoints at an Identity Provider that accept SAML authentication 
                            requests. Format of dictionary is `{"binding":"post","url":"https://my.idp.com"}`.
            slo_svc_data (:obj:`list` of :obj:`dict`): Endpoints that accept SAML logout requests or responses. Format 
                            of dictionary is `{"binding":"post","url":"https://my.idp.com"}`.
            alias_svc_db_type (:obj:`str`): A setting that specifies whether the user's alias is store in jdbc or ldap.
            alias_svc_ldap_con (:obj:`str`): A setting that specifies the LDAP Connection to store the alias.
            alias_svc_ldap_base_dn (:obj:`str`): A setting that specifies the LDAP BaseDN to search for the user.
            assertion_consume_svc (:obj:`list` of :obj:`dict`): Endpoints at a Service Provider that receive SAML \
                            assertions. Format of dictionary is `{"binding":"artifact","default":False,"index":1,
                            "url":"https:/my.sp.com"}`
            authn_req_delegate_id (:obj:`str`): The active mapping module instance. Valid values are 
                            "skip-authn-request-map" and "default-map".
            authn_req_mr (:obj:`str`): A reference to an ID of an authentication request rule.

        Returns:
            :obj:`~requests.Response`: The response from verify access. 

            Success can be checked by examining the response.success boolean attribute.

            If the request is successful the id of the created obligation can be access from the
            response.id_from_location attribute.
        """
        data = DataObject()
        data.add_value_string("name", name)
        data.add_value_string("protocol", "SAML2_0")
        data.add_value_string("role", role)
        data.add_value_string("templateName", template_name)

        encryptionSettings = DataObject()
        signatureSettings = DataObject()
        assertionSettings = DataObject()
        nameIdFmt = DataObject()

        identityMapping = None
        if (identity_delegate_id is not None):
            identityMapping = DataObject()
            identityMapping.add_value_string("activeDelegateId", identity_delegate_id)
            if (identity_mapping_rule is not None):
                identityMapping.add_value_not_empty("properties", 
                        {"identityMappingRuleReference": identity_rule_id,
                         "ruleType": identity_rule_type})
            else:
                identProps = DataObject()
                identProps.add_value_string("appliesTo", identity_applies_to)
                identProps.add_value_string("authType", identity_auth_type)
                identProps.add_value_string("basicAuthUsername", identity_ba_user)
                identProps.add_value_string("basicAuthPassword", identity_ba_password)
                identProps.add_value_string("clientKeyStore", identity_client_keystore)
                identProps.add_value_string("clientKeyAlias", identity_client_key_alias)
                identProps.add_value_string("issuerUri", identity_issuer_uri)
                identProps.add_value_string("messageFormat", identity_msg_fmt)
                identProps.add_value_string("sslKeyStore", identity_ssl_keystore)
                identProps.add_value_string("uri", identity_uri)
                identityMapping.add_value_not_empty("properties", identProps.data)

        extensionMapping = None
        if(ext_delegate_id is not None):
            extensionMapping = DataObject()
            extensionMapping.add_value_string("activeDelegateId")
            if ext_mapping_rule is not None:
                extensionMapping.add_value("properties", {"extensionMappingRuleReference", ext_mapping_rule})

        decryptionKeyIdentifier = DataObject()
        decryptionKeyIdentifier.add_value_string("keystore", decrypt_keystore)
        decryptionKeyIdentifier.add_value_string("label", decrypt_key_label)

        encryptionSettings.add_value_not_empty("decryptionKeyIdentifier", decryptionKeyIdentifier.data)
        signatureSettings.add_value_not_empty("signingKeyIdentifier", signingKeyIdentifier.data)
        signatureSettings.add_value_string("signatureAlgorithm", sign_alg)
        signatureSettings.add_value_string("digestAlgorithm", sign_digest_alg)
        signOpts = DataObject()
        signOpts.add_value_boolean("signAssertion", sign_assertion)
        signOpts.add_value_boolean("signAuthnResponse", sign_authn_rsp)
        signOpts.add_value_boolean("signArtifactRequest", sign_arti_req)
        signOpts.add_value_boolean("signArtifactResponse", sign_arti_rsp)
        signOpts.add_value_boolean("signLogoutRequest", sign_logout_req)
        signOpts.add_value_boolean("signLogoutResponse", sign_logout_rsp)
        signOpts.add_value_boolean("signNameIDManagementRequest", sign_name_id_req)
        signOpts.add_value_boolean("signNameIDManagementResponse", sign_name_id_rsp)
        signatureSettings.add_value_not_empty("signingOptions", signOpts.data)

        validOpts = DataObject()
        validOpts.add_value_boolean("validateAuthnRequest", validate_auth_req)
        validOpts.add_value_boolean("validateAssertion", validate_assert)
        validOpts.add_value_boolean("validateArtifactRequest", validate_arti_req)
        validOpts.add_value_boolean("validateArtifactResponse", validate_arti_rsp)
        validOpts.add_value_boolean("validateLogoutRequest", validate_logout_req)
        validOpts.add_value_boolean("validateLogoutResponse", validate_logout_rsp)
        validOpts.add_value_boolean("validateNameIDManagementRequest", validate_name_id_req)
        validOpts.add_value_boolean("validateNameIDManagementResponse", validate_name_id_rsp)
        signatureSettings.add_value_not_empty("validationOptions", validOpts.data)
        if transform_include_namespace is not None:
            signatureSettings.add_value(
                "transformAlgorithmElements", {"includeInclusiveNamespaces": transform_include_namespace})
        keyInfo = DataObject()
        keyInfo.add_value_boolean("includePublicKey", sign_include_pubkey)
        keyInfo.add_value_boolean("includeX509CertificateData", sign_include_cert)
        keyInfo.add_value_boolean("includeX509IssuerDetails", sign_include_issuer)
        keyInfo.add_value_boolean("includeX509SubjectKeyIdentifier", sign_include_ski)
        keyInfo.add_value_boolean("includeX509SubjectName", sign_include_subject)
        keyInfo.add_value_boolean("includeX509SubjectName", sign_include_subject)
        signatureSettings.add_value_not_empty("keyInfoElements", keyInfo.data)
        signingKeyIdentifier = DataObject()
        signingKeyIdentifier.add_value_string("keystore", signing_keystore)
        signingKeyIdentifier.add_value_string("label", signing_key_label)


        if name_id_default is not None or name_id_supported is not None:
            nameIdFmt.add_value_string("default", name_id_default)
            nameIdFmt.add_value_not_empty("supported", name_id_supported)

        aliasSvc = DataObject()
        aliasSvc.add_value_string("aliasServiceDBType", alias_svc_db_type)
        aliasSvc.add_value_string("aliasServiceLDAPConnection", alias_svc_ldap_con)
        aliasSvc.add_value_string("aliasServiceLDAPBaseDN", alias_svc_ldap_base_dn)

        configuration = DataObject()
        configuration.add_value_string("accessPolicy", access_policy)
        configuration.add_value("artifactLifeTime", artifact_lifetime)
        configuration.add_value_not_empty("assertionConsumerService", assertion_consume_svc)
        configuration.add_value_not_empty("assertionSettings", assertionSettings.data)
        configuration.add_value_not_empty("artifactResolutionService", artifact_resolution_service)
        configuration.add_value_not_empty("attributeMapping", {} if not attribute_mappings else {"map": attribute_mappings})
        configuration.add_value_string("companyName", company_name)
        configuration.add_value_not_empty("encryptionSettings", encryptionSettings.data)
        configuration.add_value_not_empty("identityMapping", identityMapping.data)
        configuration.add_value_not_empty("extensionMapping", extensionMapping.data)
        configuration.add_value_not_empty("manageNameIDService", manage_name_id_services)
        configuration.add_value("messageValidTime", msg_valid_time)
        configuration.add_value_string("messageIssuerFormat", msg_issuer_fmt)
        configuration.add_value_string("messageIssuerNameQualifier", msg_issuer_name_qualifier)
        configuration.add_value_not_empty("nameIDFormat", nameIdFmt.data)
        configuration.add_value_boolean("needConsentToFederate", consent_to_federate)
        configuration.add_value_boolean("excludeSessionIndexInSingleLogoutRequest", exclude_session_index_logout_request)
        configuration.add_value_string("pointOfContactUrl", poc_url)
        configuration.add_value_string("providerId", provider_id)
        configuration.add_value("sessionTimeout", session_timeout)
        configuration.add_value_not_empty("signatureSettings", signatureSettings.data)
        configuration.add_value_not_empty("singleSignOnService", sso_svc_data)
        configuration.add_value_not_empty("singleLogoutService", slo_svc_data)
        configuration.add_value_not_empty("aliasServiceSettings", aliasSvc.data)

        data.add_value_not_empty("configuration", configuration.data)
        response = self.client.post_json(FEDERATIONS, data.data)
        response.success = response.status_code == 201

        return response


    def create_saml_partner(self, federation_id, name=None, enabled=False, role=None, template_name=None, access_policy=None,
            arti_resolution_svc=[], assert_consume_svc=[], assert_valid_before=None, assert_valid_after=None, assert_attr_types=[],
            assert_session_not_after=None, assert_multi_attr_stmt=None, attr_mapping=[], decrypt_key_store=None, 
            decrypt_key_alias=None, encrypt_block_alg=None, encrypt_transport_alg=None, encrypt_key_store=None, 
            encrypt_key_alias=None, encrypt_name_id=None, encrypt_assertion=None, encrypt_assertion_attrs=None,
            identity_delegate_id=None, identity_rule_type='JAVASCRIPT', identity_mr=None, identity_applies_to=None,
            identity_auth_type=None, identity_ba_user=None, identity_ba_password=None,
            identity_client_key_store=None, identity_client_key_alias=None, identity_issuer_uri=None, identity_mgs_fmt=None,
            identity_ssl_key_store=None, identity_uri=None, ext_delegate_id=None, ext_mr=None, include_fed_id_in_partner_id=None, 
            logout_req_lifetime=None, manage_name_id_services=[], name_id_default=None, name_id_supported=[],
            provider_id=None, session_timeout=None, sign_include_pub_key=None, sign_include_cert=None, sign_include_issuer=None, 
            sign_include_ski=None, sign_include_subject=None, sign_key_store=None, sign_key_alias=None, sign_arti_request=None, 
            sign_arti_rsp=None, sign_assertion=None, sign_authn_rsp=None, sign_logout_req=None, sign_logout_rsp=None, 
            sign_name_id_req=None, sign_name_id_rsp=None, transform_include_namespace=None, validate_assertion=None, 
            validate_authn_req=None, validate_arti_req=None, validate_arti_rsp=None, validate_logout_req=None, 
            validate_logout_rsp=None, validate_name_id_req=None, validate_name_id_rsp=None, sign_alg=None, sign_digest_alg=None, 
            validation_key_store=None, validation_key_alias=None, slo_svc=[], soap_key_store=None, soap_key_alias=None, 
            soap_client_auth_method=None, soap_client_auth_ba_user=None, soap_client_auth_ba_password=None, 
            soap_client_auth_key_store=None, soap_client_auth_key_alias=None, anon_user_name=None, force_authn_to_federate=None, 
            authn_req_delegate_id=None, authn_req_mr=None, map_unknown_alias=None, sso_svc=[], default_target_url=None):
        """
        Create a SAML 2.0 IDP or SP Partner

        Args:
            federation_id (:obj:`str`): The system-assigned federation identifier.
            name (:obj:`str`): A meaningful name to identify this partner.
            enabled (:obj:`str`): Whether to enable the partner.
            role (:obj:`str`): The role this partner plays in its federation: "ip" for a SAML 2.0 identity provider 
                            partner, and "sp" for a SAML 2.0 service provider partner.
            template_name (:obj:`str`): An identifier for the template on which to base this partner.
            access_policy (:obj:`str`): The access policy that should be applied during single sign-on.
            arti_resolution_svc (:obj:`list` of :obj:`dict`): Partner's endpoints where artifacts are exchanged for 
                            actual SAML messages. Required if artifact binding is enabled. Format of dictionary is
                            `{"binding":"post","default":True,"index":1,"url":"https://my.idp.com"}`
            assert_consume_svc (:obj:`list` of :obj:`dict`): Endpoints at a Service Provider that receive SAML assertions.
                            Format of dictionary is `{"binding":"post","default":True,"index":1,"url":"https://my.idp.com"}`
            assert_valid_before (`int`, optional): The number of seconds before the issue date that an assertion 
                            is considered valid.
            assert_valid_after (`int`, optional): The number of seconds the assertion is valid after being issued.
            assert_attr_types (:obj:`list` of :obj:`str`): A setting that specifies the types of attributes to include 
                            in the assertion.
            assert_session_not_after (`int`, optional): The number of seconds that the security context established for 
                            the principal should be discarded by the service provider.
            assert_multi_attr_stmt (`bool`, optional): A setting that specifies whether to keep multiple attribute 
                            statements in the groups in which they were received.
            attr_mapping (:obj:`list` of :obj:`dict`, optional): The attribute mapping data. Format of the dictionary is
                            `{"name":"email_address","source":"LDAP"}`.
            decrypt_key_store (:obj:`str`, optional): The certificate database name which contains the key to decrypt messages.
            decrypt_key_alias (:obj:`str`, optional): A public/private key pair that the federation partners can use to 
                            encrypt certain message content.
            encrypt_block_alg (:obj:`str`): Block encryption algorithm used to encrypt and decrypt SAML message. 
            encrypt_transport_alg (:obj:`str`): Key transport algorithm used to encrypt and decrypt keys.
            encrypt_key_store (:obj:`str`, optional): The certificate database name which contains the key to encrypt
                            SMAL messages..
            encrypt_key_alias (:obj:`str`, optional): The certificate for encryption of outgoing SAML messages. 
            encrypt_name_id (`bool`): A setting that specifies whether the name identifiers should be encrypted.
            encrypt_assertion (`bool`): A setting that specifies whether to encrypt assertions.
            encrypt_assertion_attrs (`bool`): A setting that specifies whether to encrypt assertion attributes.
            identity_delegate_id (:obj:`str`): The active mapping module instance. Valid values are "skip-identity-map", 
                            "default-map" and "default-http-custom-map".
            identity_rule_type (:obj:`str`, optional): The type of the mapping rule. The only supported type currently is JAVASCRIPT. 
            identity_mr (:obj:`str`, optional): A reference to an ID of an identity mapping rule. 
            identity_applies_to (:obj:`str`, optional): Refers to STS chain that consumes callout response.
            identity_auth_type (:obj:`str`, optional): Authentication method used when contacting external service. 
                            Supported values are NONE, BASIC or CERTIFICATE.
            identity_ba_user (:obj:`str`, optional): Username for authentication to external service. 
            identity_ba_password (:obj:`str`, optional): Password for authentication to external service.
            identity_ssl_key_store (:obj:`str`, optional): Contains key for HTTPS client authentication. 
            identity_client_key_alias (:obj:`str`, optional): Alias of the key for HTTPS client authentication.
            identity_issuer_uri (:obj:`str`, optional): Refers to STS chain that provides input for callout request.
            identity_mgs_fmt (:obj:`str`, optional): Message format of callout request.
            identity_ssl_key_store (:obj:`str`): SSL certificate trust store to use when validating SSL certificate of 
                            external service.
            identity_uri (:obj:`str`): Address of destination server to call out to. 
            ext_delegate_id (:obj:`str`): The active mapping module instance. Valid values are "skip-extension-map" 
                            and "default-map".
            ext_mr (:obj:`str`): A reference to an ID of an extension mapping rule. 
            include_fed_id_in_partner_id (`bool`, optional): A setting that specifies whether to append federation ID 
            to partner ID when mapping user aliases.
            logout_req_lifetime (`int`, optional): A setting that specifies Logout request lifetime in number of seconds. 
            manage_name_id_services (:obj:`list` of :obj:`dict`): Partner's endpoints that accept SAML name ID management 
                            requests or responses. Format of dictionary is `{"binding":"soap","url":"https://my.sp.com"}`
            name_id_default (:obj:`str`, optional): The name identifier format to use when the format attribute is not 
                            set, or is set to "urn:oasis:names:tc:SAML:1.1:nameid-format:unspecified".
            name_id_supported (:obj:`list` of :obj:`str`), optional): The list of supported name identifier formats. 
            provider_id (;obj:`str`): A unique identifier that identifies the partner.
            session_timeout
            sign_include_pub_key (`bool`, optional): A setting that specifies whether to include the public key in the 
                            KeyInfo element in the digital signature when signing a SAML message or assertion.
            sign_include_cert (`bool`, optional): A setting that specifies whether to include the base 64 encoded 
                            certificate data to be included in the KeyInfo element in the digital signature when signing 
                            a SAML message or assertion.
            sign_include_issuer (`bool`, optional): A setting that specifies whether to include the issuer name and the 
                            certificate serial number in the KeyInfo element in the digital signature when signing a 
                            SAML message or assertion.
            sign_include_ski (`bool`, optional): A setting that specifies whether to include the X.509 subject key 
                            identifier in the KeyInfo element in the digital signature when signing a SAML message or 
                            assertion.
            sign_include_subject (`bool`, optional): A setting that specifies whether to include the subject name in the 
                            KeyInfo element in the digital signature when signing a SAML message or assertion. 
            sign_key_store (:obj:`str`): The certificate database name which contians the private key to sign SAML messages.
            sign_key_alias (:obj:`str`): A public/private key pair for signing the SAML messages and the assertion.
            sign_arti_request (`bool`, optional): A setting that specifies whether to sign the artifact request.
            sign_arti_rsp (`bool`, optional): A setting that specifies whether to sign the artifact response.
            sign_assertion (`bool`, optional): A setting that specifies whether to sign the assertion.
            sign_authn_rsp (`bool`, optional): A setting that specifies whether to sign the authentication responses.
            sign_logout_req (`bool`, optional): A setting that specifies whether to sign the logout request.
            sign_logout_rsp (`bool`, optional): A setting that specifies whether to sign the logout response.
            sign_name_id_req (`bool`, optional): A setting that specifies whether to sign the name ID management request.
            sign_name_id_rsp (`bool`, optional): A setting that specifies whether to sign the name ID management response.
            transform_include_namespace (`bool`, optional): A setting that specifies whether to include the 
                            InclusiveNamespaces element in the digital signature. 
            validate_assertion (`bool`, optional): A setting that specifies whether to validate the digital signature 
                            of an assertion.
            validate_authn_req (`bool`, optional): A setting that specifies whether to validate the digital signature 
                            of an authentication request.
            validate_arti_req (`bool`, optional): A setting that specifies whether to validate the digital signature of 
                            an artifact request.
            validate_arti_rsp (`bool`, optional): A setting that specifies whether to validate the digital signature of 
                            an artifact response.
            validate_logout_req (`bool`, optional): A setting that specifies whether to validate the digital signature 
                            of a logout request.
            validate_logout_rsp (`bool`, optional): A setting that specifies whether to validate the digital signature 
                            of a logout response.
            validate_name_id_req (`bool`, optional): A setting that specifies whether to validate the digital signature 
                            of a name ID management request.
            validate_name_id_rsp (`bool`, optional): A setting that specifies whether to validate the digital signature 
                            of a name ID management response.
            sign_alg (:obj:`str`): The signature algorithm to sign and validate SAML messages and assertions.
            sign_digest_alg (:obj:`str`): The hash algorithm to apply to the transformed resources and validate its 
                            integrity.
            validation_key_store (:obj:`str`, optional): The certificate dabase which contains the validation public key.
            validation_key_alias (:obj:`str`, optional): The certificate to use to validate the signatures on the 
                            incoming SAML assertions and messages.
            slo_svc (:obj:`list` of :obj:`dict`): Partner's endpoints that accept SAML logout requests or responses. Format
                            of dictionary is `{"binding":"post","url":"https://my.idp.com"}`.
            soap_key_store (:obj:`str`, optional): The certificate database name to verify TLS connections.
            soap_key_alias (:obj:`str`, optional): The server certificate validation certificate.
            soap_client_auth_method (:obj:`str`, optional): The authentication method.
            soap_client_auth_ba_user (:obj:`str`, optional): The basic authentication username.
            soap_client_auth_ba_pasword (:obj:`str`): The basic authentication password.
            soap_client_auth_key_store (:obj:`str`, optional): The certificate database name which contains the client 
                            private key.
            soap_client_auth_key_alias (:obj:`str`, optional): The private key to use for the client.
            anon_user_name (:obj:`str`, optional): This is a one-time name identifier that allows a user to access a 
                            service through an anonymous identity.
            force_authn_to_federate (`bool`, optional): A setting that specifies whether to force user to authenticate 
                            before linking the account.
            authn_req_delegate_id (:obj:`str`): The active mapping module instance. Valid values are "skip-authn-request-map",
                            "federation-config" and "default-map".
            authn_req_mr (:obj:`str`): A reference to an ID of an authentication request rule.
            map_unknown_alias (`bool`, optional): A setting that specifies whether to map non-linked persistent name ID 
                            to one-time username.
            sso_svc (:obj:`list` of :obj:`dict`): Partner's endpoints that accept SAML authentication requests. Format of
                            dictionary is `{"binding":"post","url":"https://my.idp.com"}`.
            default_target_url (:obj:`str`, optional): Default URL where end-user will be redirected after the completion 
                            of single sign-on.



        Returns:
            :obj:`~requests.Response`: The response from verify access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the id of the created obligation can be acess from the
            response.id_from_location attribute
        """
        #TODO
        data = DataObject()
        data.add_value_string("name", name)
        data.add_value("enabled", enabled)
        data.add_value_string("role", role)
        data.add_value_string("templateName", template_name)

        attributeMapping = DataObject()
        attributeMapping.add_value_not_empty("map", attribute_mapping)

        properties = DataObject()

        clientAuth = DataObject()
        clientAuth.add_value_string("method", client_auth_method)
        clientAuth.add_value_not_empty("properties", properties.data)

        serverCertValidation = DataObject()
        # serverCertValidation.add_value_string("keystore", "")

        soapSettings = DataObject()
        soapSettings.add_value_not_empty("clientAuth", clientAuth.data)
        if clientAuth.data or serverCertValidation.data:
            soapSettings.add_value("serverCertValidation", serverCertValidation.data)

        properties = DataObject()
        properties.add_value_string("identityMappingRule", mapping_rule)

        identityMapping = DataObject()
        identityMapping.add_value_not_empty("properties", properties.data)
        identityMapping.add_value_string("activeDelegateId", active_delegate_id)

        assertionConsumerService = DataObject()
        assertionConsumerService.add_value_string("binding", acs_binding)
        assertionConsumerService.add_value("default", acs_default)
        assertionConsumerService.add_value("index", acs_index)
        assertionConsumerService.add_value_string("url", acs_url)

        encryptionKeyIdentifier = DataObject()
        encryptionKeyIdentifier.add_value("keystore", encryption_keystore)
        encryptionKeyIdentifier.add_value("label", encryption_key_label)

        encryptionSettings = DataObject()
        encryptionSettings.add_value_not_empty("encryptionKeyIdentifier", encryptionKeyIdentifier.data)
        encryptionSettings.add_value_string("blockEncryptionAlgorithm", block_encryption_algorithm)
        encryptionSettings.add_value_string("encryptionKeyTransportAlgorithm", encryption_key_transport_algorithm)

        validationKeyIdentifier = DataObject()
        validationKeyIdentifier.add_value("keystore", validation_keystore)
        validationKeyIdentifier.add_value("label", validation_key_label)

        validationOptions = DataObject()
        validationOptions.add_value("validateAuthnRequest", validate_authn_request)
        validationOptions.add_value("validateLogoutRequest", validate_logout_request)
        validationOptions.add_value("validateLogoutResponse", validate_logout_response)

        signatureSettings = DataObject()
        signatureSettings.add_value_not_empty("validationOptions", validationOptions.data)
        signatureSettings.add_value_not_empty("validationKeyIdentifier", validationKeyIdentifier.data)
        signatureSettings.add_value_string("signatureAlgorithm", signature_algorithm)
        signatureSettings.add_value_string("digestAlgorithm", signature_digest_algorithm)

        configuration = DataObject()
        configuration.add_value_not_empty("identityMapping", identityMapping.data)
        configuration.add_value_not_empty("attributeMapping", attributeMapping.data)
        configuration.add_value_not_empty("assertionConsumerService", [assertionConsumerService.data])
        configuration.add_value_not_empty("assertionConsumerService", acs)
        configuration.add_value_not_empty("singleLogoutService", single_logout_service)
        configuration.add_value_not_empty("signatureSettings", signatureSettings.data)
        configuration.add_value_not_empty("encryptionSettings", encryptionSettings.data)
        configuration.add_value_not_empty("soapSettings", soapSettings.data)
        configuration.add_value_not_empty("providerId", provider_id)

        data.add_value_not_empty("configuration", configuration.data)

        endpoint = "%s%s/partners" % (FEDERATIONS, federation_id)

        print(json.dumps(data.data))

        response = self.client.post_json(endpoint, data.data)
        response.success = response.status_code == 201

        return response


    def get_federation(self, federation_id=None):
        """
        Get a federation configuration.

        Args:
            federation_id (:obj:`str`): The unique id of the federation

        Returns:
            :obj:`~requests.Response`: The response from verify access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the federation configuration is returned as JSON and can be accessed from
            the response.json attribute

        """
        endpoint = "%s/%s" % (FEDERATIONS, federation_id)
        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200
        return response


    def list_federations(self):
        """
        List the configured federations.

        Returns:
            :obj:`~requests.Response`: The response from verify access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the federation configuration list is returned as JSON and can be accessed from
            the response.json attribute
        """
        response = self.client.get_json(FEDERATIONS)
        response.success = response.status_code == 200
        return response


    def list_partners(self, federation_id):
        """
        List the partners configured for a given federation.

        Args:
            federation_id (:obj:`str`): Unique ID of the federation to get partner configuration for.

        Returns:
            :obj:`~requests.Response`: The response from verify access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the federation partner configuration is returned as JSON and can be accessed from
            the response.json attribute
        """
        endpoint = "%s/%s/partners" % (FEDERATIONS, federation_id)
        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200
        return response


    def get_partner(self, federation_id, partner_id=None):
        """
        Get a partner configuration from a federation

        Args:
            federation_id (:obj:`str`): The id of the federation.
            partner_id (:obj:`str`): The id of the partner to return.

        Returns:
            :obj:`~requests.Response`: The response from verify access. 

            Success can be checked by examining the response.success boolean attribute

            If the request is successful the federation partner configuration is returned as JSON and can be accessed from
            the response.json attribute

        """
        endpoint = "%s/%s/partners/%s" % (FEDERATIONS, federation_id, partner_id)
        response = self.client.get_json(endpoint)
        response.success = response.status_code == 200
        return response


    def delete_federation(self, federation_id):
        """
        Delete a federation configuration.

        Args:
            federation_id (:obj:`str`): The id of the federation to modify.

        Returns:
            :obj:`~requests.Response`: The response from verify access. 

            Success can be checked by examining the response.success boolean attribute

        """
        endpoint = "%s/%s" % (FEDERATIONS, federation_id)
        response = self.client.delete_json(endpoint)
        response.success = response.status_code == 204
        return response


    def delete_partner(self, federation_id, partner_id):
        """
        Delete a partner configuration from a federation

        Args:
            federation_id (:obj:`str`): The id of the federation to modify.
            partner_id (:obj:`str`): The id of the partner to remove.

        Returns:
            :obj:`~requests.Response`: The response from verify access. 

            Success can be checked by examining the response.success boolean attribute

        """
        endpoint = "%s/%s/partners/%s" % (FEDERATIONS, federation_id, partner_id)
        response = self.client.delete_json(endpoint)
        response.success = response.status_code == 204
        return response


class Federations9040(Federations):

    def create_oidc_federation(self, name=None, role=None, redirect_uri_prefix=None, response_types_supported=None, 
            attribute_mappings=[], identity_delegate_id=None, identity_rule_type="JAVASCRIPT", identity_mapping_rule=None, 
            identity_applies_to=None, identity_auth_type=None, identity_ba_user=None, identity_ba_password=None,
            identity_client_keystore=None, identity_client_key_alias=None, identity_issuer_uri=None, 
            identity_message_format=None, identity_ssl_keystore=None, identity_uri=None, adv_delegate_id=None,
            adv_rule_type="JAVASCRIPT", adv_mapping_rule=None):
        attributeMapping = DataObject()
        attributeMapping.add_value_not_empty("map", attribute_mappings)

        advConfig = DataObject()
        advConfig.add_value_string("activeDelegateId", adv_delegate_id)
        advConfigProps = DataObject()
        advConfigProps.add_value_string("ruleType", adv_rule_type)
        advConfigProps.add_value_string("advanceMappingRuleReference", adv_mapping_rule)
        advConfig.add_value_not_empty("properties", advConfigProps.data)

        identityMapping = DataObject()
        identityMapping.add_value_string("activeDelegateId", identity_delegate_id)
        properties = DataObject()
        if identity_delegate_id == "default-map":
            properties.add_value_string("ruleType", identity_rule_type)
            properties.add_value_string("identityMappingRuleReference", identity_mapping_rule_reference)

        elif identity_delegate_id == "default-http-custom-map":
            properties.add_value_string("appliesTo", identity_applies_to)
            properties.add_value_string("authType", identity_auth_type)
            properties.add_value_string("basicAuthUsername", identity_ba_user)
            properties.add_value_string("basicAuthPassword", identity_ba_password)
            properties.add_value_string("clientKeyStore", identity_client_keystore)
            properties.add_value_string("clientKeyAlias", identity_client_key_alias)
            properties.add_value_string("issuerUri", identity_issuer_uri)
            properties.add_value_string("messageFormat", identity_message_format)
            properties.add_value_string("sslKeyStore", identity_ssl_keystore)
            properties.add_value_string("uri", identity_uri)
        identityMapping.add_value_not_empty("properties", properties.data)

        configuration = DataObject()
        configuration.add_value_not_empty("identityMapping", identityMapping.data)
        configuration.add_value_not_empty("attributeMapping", attributeMapping.data)
        configuration.add_value_not_empty("advancedConfiguration", advConfig.data)
        configuration.add_value_string("redirectUriPrefix", redirect_uri_prefix)
        configuration.add_value_string("responseTypes", response_types_supported)

        data = DataObject()
        data.add_value_string("name", name)
        data.add_value_string("protocol", "OIDC")
        data.add_value_string("role", role)
        data.add_value_not_empty("configuration", configuration.data)

        response = self.client.post_json(FEDERATIONS, data.data)
        response.success = response.status_code == 201

        return response

    def create_oidc_rp_partner(self, federation_id, name=None, role="rp", redirect_uri_prefix=None,
        response_types=[], attribute_mappings=[], identity_delegate_id=None, identity_mapping_rule=None,
        identity_auth_type=None, identity_ba_user=None, identity_ba_password=None, identity_client_keystore=None, 
        identity_client_key_alias=None, identity_issuer_uri=None, identity_msg_fmt=None, identity_ssl_keystore=None,
        identity_uri=None, adv_config_delegate_id=None, adv_config_rule_type="JAVASCRIPT", adv_config_mapping_rule=None):
        data = DataObject()
        data.add_value_string("name", name)
        data.add_value_string("role", role)

        identityMapping = DataObject()
        identityMapping.add_value_string("activeDelegateId", identity_delegate_id)
        identityProps = DataObject()
        if identity_mapping_rule:
            identityProps.add_value_string("identityMappingRuleReference", identity_mapping_rule)
            identityProps.add_value_string("ruleType", "JAVASCRIPT")
        else:
            identityProps.add_value_string("authType", identity_auth_type)
            identityProps.add_value_string("basicAuthUsername", identity_ba_user)
            identityProps.add_value_string("basicAuthPassword", identity_ba_password)
            identityProps.add_value_string("clientKeyStore", identity_client_keystore)
            identityProps.add_value_string("clientKeyAlias", identity_client_key_alias)
            identityProps.add_value_string("issuerUri", identity_issuer_uri)
            identityProps.add_value_string("messageFormat", identity_msg_fmt)
            identityProps.add_value_string("sslKeyStore", identity_ssl_keystore)
            identityProps.add_value_string("uri", identity_uri)
        identityMapping.add_value_not_empty("properties", identityProps.data)

        advConfig = DataObject()
        advConfProps = DataObject()
        advConfProps.add_value_string("ruleType", adv_config_rule_type)
        advConfProps.add_value_string("advanceMappingRuleReference", adv_config_mapping_rule)
        advConfig.add_value_not_empty("properties", advConfProps.data)
        advConfig.add_value_string("activeDelegateId", adv_config_delegate_id)

        configuration = DataObject()
        configuration.add_value_not_empty("advanceConfiguration", advConfig.data)
        configuration.add_value_not_empty("identityMapping", identityMapping.data)
        attributeMapping = DataObject()
        attributeMapping.add_value_not_empty("map", attribute_mappings)
        configuration.add_value_not_empty("attributeMapping", attributeMapping.data)
        configuration.add_value_string("redirect_uri_prefix", redirect_uri_prefix)
        configuration.add_value_not_empty("responseTypes", response_types)

        data.add_value_not_empty("configuration", configuration.data)

        endpoint = "%s/%s/partners" % (FEDERATIONS, federation_id)

        response = self.client.post_json(endpoint, data.data)
        response.success = response.status_code == 201

        return response

class Federations10000(Federations9040):

    def create_saml_federation(self, name=None, role=None, template_name=None, access_policy=None, artifact_lifetime=None, 
            assertion_attr_types=[], assertion_session_not_on_or_after=None, assertion_multi_attr_stmt=None, 
            assertion_valid_before=None, assertion_valid_after=None, artifact_resolution_service=[], attribute_mappings=[], 
            company_name=None, encrypt_block_alg=None, encrypt_key_transport_alg=None, encrypt_key_alias=None, 
            encrypt_key_store=None, encrypt_name_id=None, encrypt_assertions=None, encrypt_assertion_attrs=None, 
            decrypt_key_alias=None, decrypt_key_store=None, identity_delegate_id=None, identity_rule_type='JAVASCRIPT', 
            identity_rule_id=None, identity_applies_to=None, identity_auth_type=None, identity_ba_user=None, 
            identity_ba_password=None, identity_client_keystore=None, identity_client_key_alias=None, identity_issuer_uri=None, 
            identity_msg_fmt=None, identity_ssl_keystore=None, identity_uri=None, ext_delegate_id=None, ext_mapping_rule=None, 
            manage_name_id_services=[], msg_valid_time=None, msg_issuer_fmt=None, msg_issuer_name_qualifier=None, 
            name_id_default=None, name_id_supported=[], consent_to_federate=True, exclude_session_index_logout_request=False, 
            poc_url=None, provider_id=None, session_timeout=None, sign_alg=None, sign_digest_alg=None, sign_valid_key_store=None, 
            sign_valid_key_alias=None, sign_assertion=None, sign_auth_rsp=None, sign_arti_req=None, sign_arti_rsp=None, 
            sign_logout_req=None, sign_logout_rsp=None, sign_name_id_req=None, sign_name_id_rsp=None, validate_auth_req=None,
            validate_assert=None, validate_arti_req=None, validate_arti_rsp=None, validate_logout_req=None, validate_logout_rsp=None,
            validate_name_id_req=None, validate_name_id_rsp=None, transform_include_namespace=None, sign_include_pubkey=None,
            sign_include_cert=None, sign_include_issuer=None, sign_include_ski=None, sign_include_subject=None, sign_keystore=None,
            sign_key_alias=None, sso_svc_data=[], slo_svc_data=[], alias_svc_db_type=None, alias_svc_ldap_con=None,
            alias_svc_ldap_base_dn=None, assertion_consume_svc=[], authn_req_delegate_id=None, authn_req_mr=None):
        data = DataObject()
        data.add_value_string("name", name)
        data.add_value_string("protocol", "SAML2_0")
        data.add_value_string("role", role)
        data.add_value_string("templateName", template_name)

        encryptionSettings = DataObject()
        signatureSettings = DataObject()
        assertionSettings = DataObject()
        nameIdFmt = DataObject()

        identityMapping = None
        if (identity_delegate_id is not None):
            identityMapping = DataObject()
            identityMapping.add_value_string("activeDelegateId", identity_delegate_id)
            if (identity_mapping_rule is not None):
                identityMapping.add_value_not_empty("properties", 
                        {"identityMappingRuleReference": identity_rule_id,
                         "ruleType": identity_rule_type})
            else:
                identProps = DataObject()
                identProps.add_value_string("appliesTo", identity_applies_to)
                identProps.add_value_string("authType", identity_auth_type)
                identProps.add_value_string("basicAuthUsername", identity_ba_user)
                identProps.add_value_string("basicAuthPassword", identity_ba_password)
                identProps.add_value_string("clientKeyStore", identity_client_keystore)
                identProps.add_value_string("clientKeyAlias", identity_client_key_alias)
                identProps.add_value_string("issuerUri", identity_issuer_uri)
                identProps.add_value_string("messageFormat", identity_msg_fmt)
                identProps.add_value_string("sslKeyStore", identity_ssl_keystore)
                identProps.add_value_string("uri", identity_uri)
                identityMapping.add_value_not_empty("properties", identProps.data)

        extensionMapping = None
        if(ext_delegate_id is not None):
            extensionMapping = DataObject()
            extensionMapping.add_value_string("activeDelegateId")
            if ext_mapping_rule is not None:
                extensionMapping.add_value("properties", {"extensionMappingRuleReference", ext_mapping_rule})

        decryptionKeyIdentifier = DataObject()
        decryptionKeyIdentifier.add_value_string("keystore", decrypt_keystore)
        decryptionKeyIdentifier.add_value_string("label", decrypt_key_label)

        encryptionSettings.add_value_not_empty("decryptionKeyIdentifier", decryptionKeyIdentifier.data)
        signatureSettings.add_value_not_empty("signingKeyIdentifier", signingKeyIdentifier.data)
        signatureSettings.add_value_string("signatureAlgorithm", sign_alg)
        signatureSettings.add_value_string("digestAlgorithm", sign_digest_alg)
        signOpts = DataObject()
        signOpts.add_value_boolean("signAssertion", sign_assertion)
        signOpts.add_value_boolean("signAuthnResponse", sign_authn_rsp)
        signOpts.add_value_boolean("signArtifactRequest", sign_arti_req)
        signOpts.add_value_boolean("signArtifactResponse", sign_arti_rsp)
        signOpts.add_value_boolean("signLogoutRequest", sign_logout_req)
        signOpts.add_value_boolean("signLogoutResponse", sign_logout_rsp)
        signOpts.add_value_boolean("signNameIDManagementRequest", sign_name_id_req)
        signOpts.add_value_boolean("signNameIDManagementResponse", sign_name_id_rsp)
        signatureSettings.add_value_not_empty("signingOptions", signOpts.data)

        validOpts = DataObject()
        validOpts.add_value_boolean("validateAuthnRequest", validate_auth_req)
        validOpts.add_value_boolean("validateAssertion", validate_assert)
        validOpts.add_value_boolean("validateArtifactRequest", validate_arti_req)
        validOpts.add_value_boolean("validateArtifactResponse", validate_arti_rsp)
        validOpts.add_value_boolean("validateLogoutRequest", validate_logout_req)
        validOpts.add_value_boolean("validateLogoutResponse", validate_logout_rsp)
        validOpts.add_value_boolean("validateNameIDManagementRequest", validate_name_id_req)
        validOpts.add_value_boolean("validateNameIDManagementResponse", validate_name_id_rsp)
        signatureSettings.add_value_not_empty("validationOptions", validOpts.data)
        if transform_include_namespace is not None:
            signatureSettings.add_value(
                "transformAlgorithmElements", {"includeInclusiveNamespaces": transform_include_namespace})
        keyInfo = DataObject()
        keyInfo.add_value_boolean("includePublicKey", sign_include_pubkey)
        keyInfo.add_value_boolean("includeX509CertificateData", sign_include_cert)
        keyInfo.add_value_boolean("includeX509IssuerDetails", sign_include_issuer)
        keyInfo.add_value_boolean("includeX509SubjectKeyIdentifier", sign_include_ski)
        keyInfo.add_value_boolean("includeX509SubjectName", sign_include_subject)
        keyInfo.add_value_boolean("includeX509SubjectName", sign_include_subject)
        signatureSettings.add_value_not_empty("keyInfoElements", keyInfo.data)
        signingKeyIdentifier = DataObject()
        signingKeyIdentifier.add_value_string("keystore", signing_keystore)
        signingKeyIdentifier.add_value_string("label", signing_key_label)


        if name_id_default is not None or name_id_supported is not None:
            nameIdFmt.add_value_string("default", name_id_default)
            nameIdFmt.add_value_not_empty("supported", name_id_supported)

        aliasSvc = DataObject()
        aliasSvc.add_value_string("aliasServiceDBType", alias_svc_db_type)
        aliasSvc.add_value_string("aliasServiceLDAPConnection", alias_svc_ldap_con)
        aliasSvc.add_value_string("aliasServiceLDAPBaseDN", alias_svc_ldap_base_dn)

        configuration = DataObject()
        configuration.add_value_string("accessPolicy", access_policy)
        configuration.add_value("artifactLifeTime", artifact_lifetime)
        configuration.add_value_not_empty("assertionConsumerService", assertion_consume_svc)
        configuration.add_value_not_empty("assertionSettings", assertionSettings.data)
        configuration.add_value_not_empty("artifactResolutionService", artifact_resolution_service)
        configuration.add_value_not_empty("attributeMapping", {} if not attribute_mappings else {"map": attribute_mappings})
        configuration.add_value_string("companyName", company_name)
        configuration.add_value_not_empty("encryptionSettings", encryptionSettings.data)
        configuration.add_value_not_empty("identityMapping", identityMapping.data)
        configuration.add_value_not_empty("extensionMapping", extensionMapping.data)
        configuration.add_value_not_empty("manageNameIDService", manage_name_id_services)
        configuration.add_value("messageValidTime", msg_valid_time)
        configuration.add_value_string("messageIssuerFormat", msg_issuer_fmt)
        configuration.add_value_string("messageIssuerNameQualifier", msg_issuer_name_qualifier)
        configuration.add_value_not_empty("nameIDFormat", nameIdFmt.data)
        configuration.add_value_boolean("needConsentToFederate", consent_to_federate)
        configuration.add_value_boolean("excludeSessionIndexInSingleLogoutRequest", exclude_session_index_logout_request)
        configuration.add_value_string("pointOfContactUrl", poc_url)
        configuration.add_value_string("providerId", provider_id)
        configuration.add_value("sessionTimeout", session_timeout)
        configuration.add_value_not_empty("signatureSettings", signatureSettings.data)
        configuration.add_value_not_empty("singleSignOnService", sso_svc_data)
        configuration.add_value_not_empty("singleLogoutService", slo_svc_data)
        configuration.add_value_not_empty("aliasServiceSettings", aliasSvc.data)

        data.add_value_not_empty("configuration", configuration.data)
        response = self.client.post_json(FEDERATIONS, data.data)
        response.success = response.status_code == 201

        return response


    def create_saml_partner(self, federation_id, name=None, enabled=False, role=None, template_name=None, access_policy=None,
            arti_resolution_svc=[], assert_consume_svc=[], assert_valid_before=None, assert_valid_after=None, assert_attr_types=[],
            assert_session_not_after=None, assert_multi_attr_stmt=None, attr_mapping=[], decrypt_key_store=None, 
            decrypt_key_alias=None, encrypt_block_alg=None, encrypt_transport_alg=None, encrypt_key_store=None, 
            encrypt_key_alias=None, encrypt_name_id=None, encrypt_assertion=None, encrypt_assertion_attrs=None,
            identity_delegate_id=None, identity_rule_type='JAVASCRIPT', identity_mr=None, identity_applies_to=None,
            identity_auth_type=None, identity_ba_user=None, identity_ba_password=None,
            identity_client_key_store=None, identity_client_key_alias=None, identity_issuer_uri=None, identity_mgs_fmt=None,
            identity_ssl_key_store=None, identity_uri=None, ext_delegate_id=None, ext_mr=None, include_fed_id_in_partner_id=None, 
            logout_req_lifetime=None, manage_name_id_services=[], name_id_default=None, name_id_supported=[],
            provider_id=None, session_timeout=None, sign_include_pub_key=None, sign_include_cert=None, sign_include_issuer=None, 
            sign_include_ski=None, sign_include_subject=None, sign_key_store=None, sign_key_alias=None, sign_arti_request=None, 
            sign_arti_rsp=None, sign_assertion=None, sign_authn_rsp=None, sign_logout_req=None, sign_logout_rsp=None, 
            sign_name_id_req=None, sign_name_id_rsp=None, transform_include_namespace=None, validate_assertion=None, 
            validate_authn_req=None, validate_arti_req=None, validate_arti_rsp=None, validate_logout_req=None, 
            validate_logout_rsp=None, validate_name_id_req=None, validate_name_id_rsp=None, sign_alg=None, sign_digest_alg=None, 
            validation_key_store=None, validation_key_alias=None, slo_svc=[], soap_key_store=None, soap_key_alias=None, 
            soap_client_auth_method=None, soap_client_auth_ba_user=None, soap_client_auth_ba_password=None, 
            soap_client_auth_key_store=None, soap_client_auth_key_alias=None, anon_user_name=None, force_authn_to_federate=None, 
            authn_req_delegate_id=None, authn_req_mr=None, map_unknown_alias=None, sso_svc=[], default_target_url=None):
        
        data = DataObject()
        data.add_value_string("name", name)
        data.add_value("enabled", enabled)
        data.add_value_string("role", role)
        data.add_value_string("templateName", template_name)

        attributeMapping = DataObject()
        attributeMapping.add_value_not_empty("map", attribute_mapping)

        properties = DataObject()
        properties.add_value_string("username", soap_client_auth_ba_user)
        properties.add_value_string("password", soap_client_auth_ba_password)
        properties.add_value_string("keystore", soap_client_auth_key_store)
        properties.add_value_string("label", soap_client_auth_key_alias)
        clientAuth = DataObject()
        clientAuth.add_value_string("method", soap_client_auth_method)
        clientAuth.add_value_not_empty("properties", properties.data)

        serverCertValidation = DataObject()
        serverCertValidation.add_value_string("keystore", soap_key_store)
        serverCertValidation.add_value_string("label", soap_key_alias)

        soapSettings = DataObject()
        soapSettings.add_value_not_empty("clientAuth", clientAuth.data)
        soapSettings.add_value_not_empty("serverCertValidation", serverCertValidation.data)

        properties = DataObject()
        if identity_mr != None:
            properties.add_value_string("identityMappingRuleReference", identity_mr)
            properties.add_value_string("ruleType", identity_rule_type)
        else:
            properties.add_value_string("appliesTo", identity_applies_to)
            properties.add_value_string("authType", identity_auth_type)
            properties.add_value_string("basicAuthUsername", identity_ba_user)
            properties.add_value_string("basicAuthPassword", identity_ba_password)
            properties.add_value_string("clientKeyStore", identity_client_key_store)
            properties.add_value_string("clientKeyAlias", identity_client_key_alias)
            properties.add_value_string("issuerUri",identity_issuer_uri)
            properties.add_value_string("messageFormat", identity_mgs_fmt)
            properties.add_value_string("sslKeyStore", identity_ssl_key_store)
            properties.add_value_string("uri", identity_uri)
        identityMapping = DataObject()
        identityMapping.add_value_not_empty("properties", properties.data)
        identityMapping.add_value_string("activeDelegateId", active_delegate_id)

        encryptionKeyIdentifier = DataObject()
        encryptionKeyIdentifier.add_value("keystore", encrypt_key_store)
        encryptionKeyIdentifier.add_value("label", encrypt_key_alias)

        decryptKeyIdent = DataObject()
        decryptKeyIdent.add_value_string("keystore", decrypt_key_store)
        decryptKeyIdent.add_value_string("label", decrypt_key_alias)

        encryptionOptions = DataObject()
        encryptionOptions.add_value_string("encryptNameId", encrypt_name_id)
        encryptionOptions.add_value_string("encryptAssertion", encrypt_assertion_attrs)
        encryptionOptions.add_value_string("encryptAssertionAttributes", encrypt_assertion)

        encryptionSettings = DataObject()
        encryptionSettings.add_value_not_empty("decryptionKeyIdentifier", decryptKeyIdent.data)
        encryptionSettings.add_value_string("blockEncryptionAlgorithm", block_encryption_algorithm)
        encryptionSettings.add_value_string("encryptionKeyTransportAlgorithm", encryption_key_transport_algorithm)
        encryptionSettings.add_value_not_empty("encryptionKeyIdentifier", encryptionKeyIdentifier.data)
        encryptionSettings.add_value_not_empty("encryptionOptions", encryptionOptions.data)

        validationKeyIdentifier = DataObject()
        validationKeyIdentifier.add_value("keystore", validation_keystore)
        validationKeyIdentifier.add_value("label", validation_key_label)

        validationOptions = DataObject()
        validationOptions.add_value_boolean("validateAssertion", validate_assert)
        validationOptions.add_value_boolean("validateAuthnRequest", validate_authn_request)
        validationOptions.add_value_boolean("validateArtifactRequest", validate_arti_req)
        validationOptions.add_value_boolean("validateArtifactResponse",validate_arti_rsp)
        validationOptions.add_value_boolean("validateLogoutRequest", validate_logout_req)
        validationOptions.add_value_boolean("validateLogoutResponse", validate_logout_rsp)
        validationOptions.add_value_boolean("validateNameIDManagementRequest", validate_name_id_req)
        validationOptions.add_value_boolean("validateNameIDManagementResponse", validate_name_id_rsp)

        transformOptions = DataObject()
        transformOptions.add_value_boolean("includeInclusiveNamespaces", transform_include_namespace)

        keyInfo = DataObject()
        keyInfo.add_value_boolean("includePublicKey", sign_include_pub_key)
        keyInfo.add_value_boolean("includeX509CertificateData", sign_include_cert)
        keyInfo.add_value_boolean("includeX509IssuerDetails", sign_include_issuer)
        keyInfo.add_value_boolean("includeX509SubjectKeyIdentifier", sign_include_ski)
        keyInfo.add_value_boolean("includeX509SubjectName", sign_include_subject)

        signingKeyIdentifier = DataObject()
        signingKeyIdentifier.add_value_string("keystore", sign_key_store)
        signingKeyIdentifier.add_value_string("label", sign_key_alias)

        signingOptions = DataObject()
        signingOptions.add_value_boolean("signArtifactRequest", sign_arti_req)
        signingOptions.add_value_boolean("signArtifactResponse", sign_arti_rsp)
        signingOptions.add_value_boolean("signAssertion", sign_assertion)
        signingOptions.add_value_boolean("signAuthnResponse", sign_authn_rsp)
        signingOptions.add_value_boolean("signLogoutRequest", sign_logout_req)
        signingOptions.add_value_boolean("signLogoutResponse", sign_logout_rsp)
        signingOptions.add_value_boolean("signNameIDManagementRequest", sign_name_id_req)
        signingOptions.add_value_boolean("signNameIDManagementResponse", sign_name_id_rsp)

        signatureSettings = DataObject()
        signatureSettings.add_value_not_empty("keyInfoElements", keyInfo.data)
        signatureSettings.add_value_not_empty("signingKeyIdentifier", signingKeyIdentifier.data)
        signatureSettings.add_value_not_empty("signingOptions", signingOptions.data)
        signatureSettings.add_value_not_empty("transformAlgorithmElements", transformOptions.data)
        signatureSettings.add_value_string("signatureAlgorithm", signature_algorithm)
        signatureSettings.add_value_string("digestAlgorithm", signature_digest_algorithm)
        signatureSettings.add_value_not_empty("validationKeyIdentifier", validationKeyIdentifier.data)
        signatureSettings.add_value_not_empty("validationOptions", validationOptions.data)

        assertionSettings = DataObject()
        assertionSettings.add_value("assertionValidBefore", assert_valid_before)
        assertionSettings.add_value_not_empty("assertionAttributeTypes", assert_attr_types)
        assertionSettings.add_value("sessionNotOnOrAfter", assert_session_not_after)
        assertionSettings.add_value_boolean("createMultipleAttributeStatements", assert_multi_attr_stmt)

        extensionMapping = DataObject()
        extProps = DataObject()
        extProps.add_value_string("extensionMappingRuleReference", ext_mr)
        extensionMapping.add_value_string("activeDelegateId", ext_delegate_id)
        extensionMapping.add_value_not_empty("properties", extProps.data)

        nameIdFmt = DataObject()
        nameIdFmt.add_value_string("default", name_id_default)
        nameIdFmt.add_value_not_empty("supported", name_id_supported)

        authnReqMapping = DataObject()
        authnReqProps = DataObject()
        authnReqProps.add_value_string("authnReqMappingRuleReference", authn_req_mr)
        authnReqMapping.add_value_string("activeDelegateId", authn_req_delegate_id)
        authnReqMapping.add_value_not_empty("properties", authnReqProps.data)

        configuration = DataObject()
        configuration.add_value_string("anonymousUserName", anon_user_name)
        configuration.add_value_string("accessPolicy", access_policy)
        configuration.add_value_not_empty("artifactResolutionService", arti_resolution_svc)
        configuration.add_value_not_empty("assertionConsumerService", assert_consume_svc)
        configuration.add_value_not_empty("assertionSettings", assertionSettings.data)
        configuration.add_value_not_empty("attributeMapping", attributeMapping.data)
        configuration.add_value_not_empty("encryptionSettings", encryptionSettings.data)
        configuration.add_value_boolean("forceAuthnToFederate", force_authn_to_federate)
        configuration.add_value_not_empty("identityMapping", identityMapping.data)
        configuration.add_value_not_empty("extensionMapping", extensionMapping.data)
        configuration.add_value_not_empty("authnReqMapping", authnReqMapping.data)
        configuration.add_value_boolean("includeFedIdInAliasPartnerId", include_fed_id_in_partner_id)
        configuration.add_value("logoutRequestLifeTime", logout_req_lifetime)
        configuration.add_value_not_empty("manageNameIDService", manage_name_id_services)
        configuration.add_value_boolean("mapUnknownAlias", map_unknown_alias)
        configuration.add_value_not_empty("nameIDFormat", nameIdFmt.data)
        configuration.add_value_not_empty("providerId", provider_id)
        configuration.add_value_not_empty("signatureSettings", signatureSettings.data)
        configuration.add_value_not_empty("singleLogoutService", single_logout_service)
        configuration.add_value_not_empty("soapSettings", soapSettings.data)
        configuration.add_value_string("defaultTargetURL", default_target_url)

        data.add_value_not_empty("configuration", configuration.data)
        endpoint = "%s%s/partners" % (FEDERATIONS, federation_id)
        response = self.client.post_json(endpoint, data.data)
        response.success = response.status_code == 201

        return response