"""
Created on Nov 22, 2016

@copyright: IBM
"""

import logging

from com.ibm.isam.util.logger import Logger
from com.ibm.isam.util.restclient import RestClient
import com.ibm.isam.util.utils as Utils


class _Policy(RestClient):

    ATTRIBUTE_MATCHERS = "/iam/access/v8/attribute-matchers"
    ATTRIBUTES = "/iam/access/v8/attributes"
    AUTHENTICATION_MECHANISMS = "/iam/access/v8/authentication/mechanisms"
    AUTHENTICATION_MECHANISM_TYPES = "/iam/access/v8/authentication/mechanism/types"
    AUTHENTICATION_POLICIES = "/iam/access/v8/authentication/policies"
    CLIENTS = "/iam/access/v8/clients"
    DEFINITIONS = "/iam/access/v8/definitions"
    MAPPING_RULES = "/iam/access/v8/mapping-rules"
    POLICIES = "/iam/access/v8/policies"
    POLICY_ATTACHEMENTS = "/iam/access/v8/policyattachments"
    POLICY_ATTACHMENTS_PDADMIN = "/iam/access/v8/policyattachments/pdadmin"
    RISK_PROFILES = "/iam/access/v8/risk/profiles"

    logger = Logger("Policy")

    def __init__(self, baseUrl, username, password, logLevel=logging.NOTSET):
        super(_Policy, self).__init__(baseUrl, username, password, logLevel)
        _Policy.logger.setLevel(logLevel)

    #
    # Access Control
    #

    # Policies

    def createAccessControlPolicy(self, name=None, description=None, dialect=None, policy=None,
                     attributesrequired=None):
        methodName = "createAccessControlPolicy()"
        _Policy.logger.enterMethod(methodName)
        result = None

        jsonObj = {}
        Utils.addOnStringValue(jsonObj, "name", name)
        Utils.addOnStringValue(jsonObj, "description", description)
        Utils.addOnStringValue(jsonObj, "dialect", dialect)
        Utils.addOnStringValue(jsonObj, "policy", policy)
        Utils.addOnValue(jsonObj, "attributesrequired", attributesrequired)
        Utils.addOnValue(jsonObj, "predefined", False)

        statusCode, content = self.httpPostJson(_Policy.POLICIES, data=jsonObj)

        result = (statusCode == 201, statusCode, content)

        _Policy.logger.exitMethod(methodName, str(result))
        return result

    def getAccessControlPolicies(self, sortBy=None, filter=None):
        methodName = "getAccessControlPolicies()"
        _Policy.logger.enterMethod(methodName)
        result = None

        parameters = {}
        Utils.addOnStringValue(parameters, "sortBy", sortBy)
        Utils.addOnStringValue(parameters, "filter", filter)

        statusCode, content = self.httpGetJson(_Policy.POLICIES, parameters=parameters)

        result = (statusCode == 200, statusCode, content)

        _Policy.logger.exitMethod(methodName, str(result))
        return result

    # Policy Attachments

    def authenticateSecurityAccessManager(self, username, password, domain=""):
        methodName = "authenticateSecurityAccessManager()"
        _Policy.logger.enterMethod(methodName)
        result = None

        jsonObj = {}
        Utils.addOnStringValue(jsonObj, "username", username)
        Utils.addOnStringValue(jsonObj, "password", password)
        Utils.addOnStringValue(jsonObj, "domain", domain)
        Utils.addOnStringValue(jsonObj, "command", "setCredential")

        statusCode, content = self.httpPostJson(_Policy.POLICY_ATTACHMENTS_PDADMIN, data=jsonObj)

        result = (statusCode == 200, statusCode, content)

        _Policy.logger.exitMethod(methodName, str(result))
        return result

    def createAccessControlPolicyAttachment(self, server=None, resourceUri=None, policyCombiningAlgorithm=None,
                               policies=None):
        methodName = "createAccessControlPolicyAttachment()"
        _Policy.logger.enterMethod(methodName)
        result = None

        jsonObj = {}
        Utils.addOnStringValue(jsonObj, "server", server)
        Utils.addOnStringValue(jsonObj, "resourceUri", resourceUri)
        Utils.addOnStringValue(jsonObj, "policyCombiningAlgorithm", policyCombiningAlgorithm)
        Utils.addOnValue(jsonObj, "policies", policies)

        statusCode, content = self.httpPostJson(_Policy.POLICY_ATTACHEMENTS, data=jsonObj)

        result = (statusCode == 201, statusCode, content)

        _Policy.logger.exitMethod(methodName, str(result))
        return result

    def getAccessControlPolicyAttachment(self, sortBy=None, filter=None):
        methodName = "getAccessControlPolicyAttachment()"
        _Policy.logger.enterMethod(methodName)
        result = None

        parameters = {}
        Utils.addOnStringValue(parameters, "sortBy", sortBy)
        Utils.addOnStringValue(parameters, "filter", filter)

        statusCode, content = self.httpGetJson(_Policy.POLICY_ATTACHEMENTS, parameters=parameters)

        result = (statusCode == 200, statusCode, content)

        _Policy.logger.exitMethod(methodName, str(result))
        return result

    def publishAccessControlPolicyAttachment(self, id):
        methodName = "publishAccessControlPolicyAttachment()"
        _Policy.logger.enterMethod(methodName)
        result = None

        endpoint = "%s/deployment/%s" % (_Policy.POLICY_ATTACHEMENTS, str(id))
        statusCode, content = self.httpPutJson(endpoint)

        result = (statusCode == 204, statusCode, content)

        _Policy.logger.exitMethod(methodName, str(result))
        return result

    #
    # API Protection
    #

    # Clients

    def createApiProtectionClient(self, name=None, redirectUri=None, companyName=None,
                                  companyUrl=None, contactPerson=None, contactType=None,
                                  email=None, phone=None, otherInfo=None, definition=None,
                                  clientId=None, clientSecret=None):
        methodName = "createApiProtectionClient()"
        _Policy.logger.enterMethod(methodName)
        result = None

        jsonObj = {}
        Utils.addOnStringValue(jsonObj, "name", name)
        Utils.addOnStringValue(jsonObj, "redirectUri", redirectUri)
        Utils.addOnStringValue(jsonObj, "companyName", companyName)
        Utils.addOnStringValue(jsonObj, "companyUrl", companyUrl)
        Utils.addOnStringValue(jsonObj, "contactPerson", contactPerson)
        Utils.addOnStringValue(jsonObj, "contactType", contactType)
        Utils.addOnStringValue(jsonObj, "email", email)
        Utils.addOnStringValue(jsonObj, "phone", phone)
        Utils.addOnStringValue(jsonObj, "otherInfo", otherInfo)
        Utils.addOnStringValue(jsonObj, "definition", definition)
        Utils.addOnStringValue(jsonObj, "clientId", clientId)
        Utils.addOnStringValue(jsonObj, "clientSecret", clientSecret)

        statusCode, content = self.httpPostJson(_Policy.CLIENTS, data=jsonObj)

        result = (statusCode == 201, statusCode, content)

        _Policy.logger.exitMethod(methodName, str(result))
        return result

    def deleteApiProtectionClient(self, id):
        methodName = "deleteApiProtectionClient()"
        _Policy.logger.enterMethod(methodName)
        result = None

        endpoint = "%s/%s" % (_Policy.CLIENTS, str(id))
        statusCode, content = self.httpDeleteJson(endpoint)

        result = (statusCode == 204, statusCode, content)

        _Policy.logger.exitMethod(methodName, str(result))
        return result

    def getApiProtectionClientByClientId(self, clientId):
        methodName = "getApiProtectionClientByClientId()"
        _Policy.logger.enterMethod(methodName)
        result = None

        clientIdEquals = "clientId equals " + str(clientId)
        success, statusCode, content = self.getApiProtectionClients(filter=clientIdEquals)

        if success and len(content) > 0:
            result = (success, statusCode, content[0])
        else:
            result = (False, statusCode, content)

        _Policy.logger.exitMethod(methodName, str(result))
        return result

    def getApiProtectionClients(self, sortBy=None, count=None, start=None, filter=None):
        methodName = "getApiProtectionClients()"
        _Policy.logger.enterMethod(methodName)
        result = None

        parameters = {}
        Utils.addOnStringValue(parameters, "sortBy", sortBy)
        Utils.addOnStringValue(parameters, "count", count)
        Utils.addOnStringValue(parameters, "start", start)
        Utils.addOnStringValue(parameters, "filter", filter)

        statusCode, content = self.httpGetJson(_Policy.CLIENTS, parameters=parameters)

        result = (statusCode == 200, statusCode, content)

        _Policy.logger.exitMethod(methodName, str(result))
        return result

    # Definitions

    def createApiProtectionDefinition(self, name=None, description=None, tcmBehavior=None,
                                      tokenCharSet=None, accessTokenLifetime=None,
                                      accessTokenLength=None, authorizationCodeLifetime=None,
                                      authorizationCodeLength=None, refreshTokenLength=None,
                                      maxAuthorizationGrantLifetime=None, pinLength=None,
                                      enforceSingleUseAuthorizationGrant=None, issueRefreshToken=None,
                                      enforceSingleAccessTokenPerGrant=None,
                                      enableMultipleRefreshTokensForFaultTolerance=None,
                                      pinPolicyEnabled=None, grantTypes=[]):
        methodName = "createApiProtectionDefinition()"
        _Policy.logger.enterMethod(methodName)
        result = None

        jsonObj = {}
        Utils.addOnStringValue(jsonObj, "name", name)
        Utils.addOnStringValue(jsonObj, "description", description)
        Utils.addOnStringValue(jsonObj, "tcmBehavior", tcmBehavior)
        Utils.addOnStringValue(jsonObj, "tokenCharSet", tokenCharSet)
        Utils.addOnValue(jsonObj, "accessTokenLifetime", accessTokenLifetime)
        Utils.addOnValue(jsonObj, "accessTokenLength", accessTokenLength)
        Utils.addOnValue(jsonObj, "authorizationCodeLifetime", authorizationCodeLifetime)
        Utils.addOnValue(jsonObj, "authorizationCodeLength", authorizationCodeLength)
        Utils.addOnValue(jsonObj, "refreshTokenLength", refreshTokenLength)
        Utils.addOnValue(jsonObj, "maxAuthorizationGrantLifetime", maxAuthorizationGrantLifetime)
        Utils.addOnValue(jsonObj, "pinLength", pinLength)
        Utils.addOnValue(jsonObj, "enforceSingleUseAuthorizationGrant",
                         enforceSingleUseAuthorizationGrant)
        Utils.addOnValue(jsonObj, "issueRefreshToken", issueRefreshToken)
        Utils.addOnValue(jsonObj, "enforceSingleAccessTokenPerGrant",
                         enforceSingleAccessTokenPerGrant)
        Utils.addOnValue(jsonObj, "enableMultipleRefreshTokensForFaultTolerance",
                         enableMultipleRefreshTokensForFaultTolerance)
        Utils.addOnValue(jsonObj, "pinPolicyEnabled", pinPolicyEnabled)
        Utils.addOnValue(jsonObj, "grantTypes", grantTypes)

        statusCode, content = self.httpPostJson(_Policy.DEFINITIONS, data=jsonObj)

        result = (statusCode == 201, statusCode, content)

        _Policy.logger.exitMethod(methodName, str(result))
        return result

    def deleteApiProtectionDefinition(self, id):
        methodName = "deleteApiProtectionDefinition()"
        _Policy.logger.enterMethod(methodName)
        result = None

        endpoint = "%s/%s" % (_Policy.DEFINITIONS, str(id))
        statusCode, content = self.httpDeleteJson(endpoint)

        result = (statusCode == 204, statusCode, content)

        _Policy.logger.exitMethod(methodName, str(result))
        return result

    def getApiProtectionDefinitionByName(self, name):
        methodName = "getApiProtectionDefinitionByName()"
        _Policy.logger.enterMethod(methodName)
        result = None

        nameEquals = "name equals " + str(name)
        success, statusCode, content = self.getApiProtectionDefinitions(filter=nameEquals)

        if success and len(content) > 0:
            result = (success, statusCode, content[0])
        else:
            result = (False, statusCode, content)

        _Policy.logger.exitMethod(methodName, str(result))
        return result

    def getApiProtectionDefinitions(self, sortBy=None, count=None, start=None, filter=None):
        methodName = "getApiProtectionDefinitions()"
        _Policy.logger.enterMethod(methodName)
        result = None

        parameters = {}
        Utils.addOnStringValue(parameters, "sortBy", sortBy)
        Utils.addOnStringValue(parameters, "count", count)
        Utils.addOnStringValue(parameters, "start", start)
        Utils.addOnStringValue(parameters, "filter", filter)

        statusCode, content = self.httpGetJson(_Policy.DEFINITIONS, parameters=parameters)

        result = (statusCode == 200, statusCode, content)

        _Policy.logger.exitMethod(methodName, str(result))
        return result

    # Mapping Rules

    def createApiProtectionMappingRule(self, name, category, fileName, content=""):
        methodName = "createApiProtectionMappingRule()"
        _Policy.logger.enterMethod(methodName)
        result = None

        jsonObj = {}
        Utils.addOnStringValue(jsonObj, "name", name)
        Utils.addOnStringValue(jsonObj, "category", category)
        Utils.addOnStringValue(jsonObj, "fileName", fileName)
        Utils.addOnStringValue(jsonObj, "content", content)

        statusCode, content = self.httpPostJson(_Policy.MAPPING_RULES, data=jsonObj)

        result = (statusCode == 200, statusCode, content)

        _Policy.logger.exitMethod(methodName, str(result))
        return result

    def getApiProtectionMappingRules(self, sortBy=None, count=None, start=None, filter=None):
        methodName = "getApiProtectionMappingRules()"
        _Policy.logger.enterMethod(methodName)
        result = None

        parameters = {}
        Utils.addOnStringValue(parameters, "sortBy", sortBy)
        Utils.addOnStringValue(parameters, "count", count)
        Utils.addOnStringValue(parameters, "start", start)
        Utils.addOnStringValue(parameters, "filter", filter)

        statusCode, content = self.httpGetJson(_Policy.MAPPING_RULES, parameters=parameters)

        result = (statusCode == 200, statusCode, content)

        _Policy.logger.exitMethod(methodName, str(result))
        return result

    def updateApiProtectionMappingRule(self, id, content=""):
        methodName = "updateApiProtectionMappingRule()"
        _Policy.logger.enterMethod(methodName)
        result = None

        jsonObj = {}
        Utils.addOnStringValue(jsonObj, "content", content)

        endpoint = "%s/%s" % (_Policy.MAPPING_RULES, str(id))
        statusCode, content = self.httpPutJson(endpoint, data=jsonObj)

        result = (statusCode == 204, statusCode, content)

        _Policy.logger.exitMethod(methodName, str(result))
        return result

    #
    # Attributes
    #

    # Attributes

    def createAttribute(self, category=None, matcher=None, issuer=None, description=None, name=None,
                        datatype=None, uri=None, sessionStorage=None, behaviorStorage=None,
                        deviceStorage=None, riskType=None, policyType=None):
        methodName = "createAttribute()"
        _Policy.logger.enterMethod(methodName)
        result = None

        storageObj = {}
        Utils.addOnValue(storageObj, "session", sessionStorage)
        Utils.addOnValue(storageObj, "behavior", behaviorStorage)
        Utils.addOnValue(storageObj, "device", deviceStorage)

        typeObj = {}
        Utils.addOnValue(typeObj, "risk", riskType)
        Utils.addOnValue(typeObj, "policy", policyType)

        jsonObj = {}
        Utils.addOnStringValue(jsonObj, "category", category)
        Utils.addOnStringValue(jsonObj, "matcher", matcher)
        Utils.addOnStringValue(jsonObj, "issuer", issuer)
        Utils.addOnStringValue(jsonObj, "description", description)
        Utils.addOnStringValue(jsonObj, "name", name)
        Utils.addOnStringValue(jsonObj, "datatype", datatype)
        Utils.addOnStringValue(jsonObj, "uri", uri)
        Utils.addOnValue(jsonObj, "predefined", False)
        Utils.addOnValue(jsonObj, "storageDomain", storageObj)
        Utils.addOnValue(jsonObj, "type", typeObj)

        statusCode, content = self.httpPostJson(_Policy.ATTRIBUTES, data=jsonObj)

        result = (statusCode == 201, statusCode, content)

        _Policy.logger.exitMethod(methodName, str(result))
        return result

    def getAttributeByUri(self, uri):
        methodName = "getAttributeByUri()"
        _Policy.logger.enterMethod(methodName)
        result = None

        uriEquals = "uri equals %s" % str(uri)
        success, statusCode, content = self.getAttributes(filter=uriEquals)

        if success and len(content) > 0:
            result = (success, statusCode, content[0])
        else:
            result = (success, statusCode, content)

        _Policy.logger.exitMethod(methodName, str(result))
        return result

    def getAttributes(self, sortBy=None, count=None, start=None, filter=None):
        methodName = "getAttributes()"
        _Policy.logger.enterMethod(methodName)
        result = None

        parameters = {}
        Utils.addOnStringValue(parameters, "sortBy", sortBy)
        Utils.addOnStringValue(parameters, "count", count)
        Utils.addOnStringValue(parameters, "start", start)
        Utils.addOnStringValue(parameters, "filter", filter)

        statusCode, content = self.httpGetJson(_Policy.ATTRIBUTES, parameters=parameters)

        result = (statusCode == 200, statusCode, content)

        _Policy.logger.exitMethod(methodName, str(result))
        return result

    # Matchers

    def getAttributeMatcherByUri(self, uri):
        methodName = "getAttributeMatcherByUri()"
        _Policy.logger.enterMethod(methodName)
        result = None

        uriEquals = "uri equals %s" % str(uri)
        success, statusCode, content = self.getAttributeMatchers(filter=uriEquals)

        if success and len(content) > 0:
            result = (success, statusCode, content[0])
        else:
            result = (success, statusCode, content)

        _Policy.logger.exitMethod(methodName, str(result))
        return result

    def getAttributeMatchers(self, sortBy=None, filter=None):
        methodName = "getAttributeMatchers()"
        _Policy.logger.enterMethod(methodName)
        result = None

        parameters = {}
        Utils.addOnStringValue(parameters, "sortBy", sortBy)
        Utils.addOnStringValue(parameters, "filter", filter)

        statusCode, content = self.httpGetJson(_Policy.ATTRIBUTE_MATCHERS, parameters=parameters)

        result = (statusCode == 200, statusCode, content)

        _Policy.logger.exitMethod(methodName, str(result))
        return result

    #
    # Authentication
    #

    # Mechanisms

    def createAuthenticationMechanism(self, description=None, name=None, uri=None, typeId=None,
                                      properties=None, attributes=None, jsonObj=None):
        methodName = "createAuthenticationMechanism()"
        _Policy.logger.enterMethod(methodName)
        result = None

        if jsonObj is None:
            jsonObj = {}
            Utils.addOnStringValue(jsonObj, "description", description)
            Utils.addOnStringValue(jsonObj, "name", name)
            Utils.addOnStringValue(jsonObj, "uri", uri)
            Utils.addOnStringValue(jsonObj, "typeId", typeId)
            Utils.addOnValue(jsonObj, "properties", properties)
            Utils.addOnValue(jsonObj, "attributes", attributes)

        statusCode, content = self.httpPostJson(_Policy.AUTHENTICATION_MECHANISMS, data=jsonObj)

        result = (statusCode == 201, statusCode, content)

        _Policy.logger.exitMethod(methodName, str(result))
        return result

    def getAuthenticationMechanismByUri(self, uri):
        methodName = "getAuthenticationMechanismByUri()"
        _Policy.logger.enterMethod(methodName)
        result = None

        uriEquals = "uri equals %s" % str(uri)
        success, statusCode, content = self.getAuthenticationMechanisms(filter=uriEquals)

        if success and len(content) > 0:
            result = (success, statusCode, content[0])
        else:
            result = (success, statusCode, content)

        _Policy.logger.exitMethod(methodName, str(result))
        return result

    def getAuthenticationMechanismTypes(self, sortBy=None, count=None, start=None, filter=None):
        methodName = "getAuthenticationMechanismTypes()"
        _Policy.logger.enterMethod(methodName)
        result = None

        parameters = {}
        Utils.addOnStringValue(parameters, "sortBy", sortBy)
        Utils.addOnStringValue(parameters, "count", count)
        Utils.addOnStringValue(parameters, "start", start)
        Utils.addOnStringValue(parameters, "filter", filter)

        statusCode, content = self.httpGetJson(_Policy.AUTHENTICATION_MECHANISM_TYPES,
                                               parameters=parameters)

        result = (statusCode == 200, statusCode, content)

        _Policy.logger.exitMethod(methodName, str(result))
        return result

    def getAuthenticationMechanisms(self, sortBy=None, count=None, start=None, filter=None):
        methodName = "getAuthenticationMechanisms()"
        _Policy.logger.enterMethod(methodName)
        result = None

        parameters = {}
        Utils.addOnStringValue(parameters, "sortBy", sortBy)
        Utils.addOnStringValue(parameters, "count", count)
        Utils.addOnStringValue(parameters, "start", start)
        Utils.addOnStringValue(parameters, "filter", filter)

        statusCode, content = self.httpGetJson(_Policy.AUTHENTICATION_MECHANISMS,
                                               parameters=parameters)

        result = (statusCode == 200, statusCode, content)

        _Policy.logger.exitMethod(methodName, str(result))
        return result

    def updateAuthenticationMechanism(self, id, description=None, name=None, uri=None, typeId=None,
                                      predefined=None, properties=None, attributes=None, jsonObj=None):
        methodName = "updateAuthenticationMechanism()"
        _Policy.logger.enterMethod(methodName)
        result = None

        if jsonObj is None:
            jsonObj = {}
            Utils.addOnStringValue(jsonObj, "id", id)
            Utils.addOnStringValue(jsonObj, "description", description)
            Utils.addOnStringValue(jsonObj, "name", name)
            Utils.addOnStringValue(jsonObj, "uri", uri)
            Utils.addOnStringValue(jsonObj, "typeId", typeId)
            Utils.addOnValue(jsonObj, "predefined", predefined)
            Utils.addOnValue(jsonObj, "properties", properties)
            Utils.addOnValue(jsonObj, "attributes", attributes)

        endpoint = "%s/%s" % (_Policy.AUTHENTICATION_MECHANISMS, str(id))
        statusCode, content = self.httpPutJson(endpoint, data=jsonObj)

        result = (statusCode == 204, statusCode, content)

        _Policy.logger.exitMethod(methodName, str(result))
        return result

    # Policies

    def createAuthenticationPolicies(self, name=None, policy=None, uri=None, description=None,
                                     dialect=None, id=None, userlastmodified=None, lastmodified=None,
                                     datecreated=None, jsonObj=None):
        methodName = "createAuthenticationPolicies()"
        _Policy.logger.enterMethod(methodName)
        result = None

        if jsonObj is None:
            jsonObj = {}
            Utils.addOnStringValue(jsonObj, "name", name)
            Utils.addOnStringValue(jsonObj, "policy", policy)
            Utils.addOnStringValue(jsonObj, "uri", uri)
            Utils.addOnStringValue(jsonObj, "description", description)
            Utils.addOnStringValue(jsonObj, "dialect", dialect)
            Utils.addOnStringValue(jsonObj, "id", id)
            Utils.addOnStringValue(jsonObj, "userlastmodified", userlastmodified)
            Utils.addOnStringValue(jsonObj, "lastmodified", lastmodified)
            Utils.addOnStringValue(jsonObj, "datecreated", datecreated)

        statusCode, content = self.httpPostJson(_Policy.AUTHENTICATION_POLICIES, data=jsonObj)

        result = (statusCode == 201, statusCode, content)

        _Policy.logger.exitMethod(methodName, str(result))
        return result

    #
    # Risk Profiles
    #

    def createRiskProfile(self, description=None, name=None, active=None, attributes=None, jsonObj=None):
        methodName = "createRiskProfile()"
        _Policy.logger.enterMethod(methodName)
        result = None

        if jsonObj is None:
            jsonObj = {}
            Utils.addOnStringValue(jsonObj, "description", description)
            Utils.addOnStringValue(jsonObj, "name", name)
            Utils.addOnValue(jsonObj, "active", active)
            Utils.addOnValue(jsonObj, "attributes", attributes)
            Utils.addOnValue(jsonObj, "predefined", False)

        statusCode, content = self.httpPostJson(_Policy.RISK_PROFILES, data=jsonObj)

        result = (statusCode == 201, statusCode, content)

        _Policy.logger.exitMethod(methodName, str(result))
        return result


class Policy9020(_Policy):

    logger = Logger("Policy9020")

    def __init__(self, baseUrl, username, password, logLevel=logging.NOTSET):
        super(Policy9020, self).__init__(baseUrl, username, password, logLevel)
        Policy9020.logger.setLevel(logLevel)
