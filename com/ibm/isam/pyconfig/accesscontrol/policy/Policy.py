"""
Created on Nov 22, 2016

@copyright: IBM
"""
from com.ibm.isam.pyconfig.Factory import Factory
from com.ibm.isam.util.RestClient import RestClient
from com.ibm.isam.util.Logger import Logger
import com.ibm.isam.util.Utils as Utils
import abc, logging

class Policy(RestClient):
    __metaclass__ = abc.ABCMeta

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
        super(Policy, self).__init__(baseUrl, username, password, logLevel)
        Policy.logger.setLevel(logLevel)

    @abc.abstractmethod
    def getIsamVersion(self):
        pass

    #
    # Access Control
    #

    # Policies

    def createPolicy(self, name=None, description=None, dialect=None, policy=None, attributesrequired=None):
        methodName = "createPolicy()"
        Policy.logger.enterMethod(methodName)
        result = None

        jsonObj = {}
        Utils.addOnStringValue(jsonObj, "name", name)
        Utils.addOnStringValue(jsonObj, "description", description)
        Utils.addOnStringValue(jsonObj, "dialect", dialect)
        Utils.addOnStringValue(jsonObj, "policy", policy)
        Utils.addOnValue(jsonObj, "attributesrequired", attributesrequired)
        Utils.addOnValue(jsonObj, "predefined", False)

        statusCode, content = self.httpPostJson(Policy.POLICIES, jsonObj)

        if statusCode == 201:
            result = True if content is None else content

        Policy.logger.exitMethod(methodName, str(result))
        return result

    def getPolicies(self, sortBy=None, filter=None):
        methodName = "getPolicies()"
        Policy.logger.enterMethod(methodName)
        result = None

        parameters = {}
        Utils.addOnStringValue(parameters, "sortBy", sortBy)
        Utils.addOnStringValue(parameters, "filter", filter)

        statusCode, content = self.httpGetJson(Policy.POLICIES, parameters=parameters)

        if statusCode == 200 and content is not None:
            result = content

        Policy.logger.exitMethod(methodName, str(result))
        return result

    # Policy Attachments

    def authenticateSecurityAccessManager(self, username, password, domain=""):
        methodName = "authenticateSecurityAccessManager()"
        Policy.logger.enterMethod(methodName)
        result = None

        jsonObj = {}
        Utils.addOnStringValue(jsonObj, "username", username)
        Utils.addOnStringValue(jsonObj, "password", password)
        Utils.addOnStringValue(jsonObj, "domain", domain)
        Utils.addOnStringValue(jsonObj, "command", "setCredential")

        statusCode, content = self.httpPostJson(Policy.POLICY_ATTACHMENTS_PDADMIN, jsonObj)

        if statusCode == 200:
            result = True if content is None else content

        Policy.logger.exitMethod(methodName, str(result))
        return result

    def createPolicyAttachment(self, server=None, resourceUri=None, policyCombiningAlgorithm=None, policies=None):
        methodName = "createPolicyAttachment()"
        Policy.logger.enterMethod(methodName)
        result = None

        jsonObj = {}
        Utils.addOnStringValue(jsonObj, "server", server)
        Utils.addOnStringValue(jsonObj, "resourceUri", resourceUri)
        Utils.addOnStringValue(jsonObj, "policyCombiningAlgorithm", policyCombiningAlgorithm)
        Utils.addOnValue(jsonObj, "policies", policies)

        statusCode, content = self.httpPostJson(Policy.POLICY_ATTACHEMENTS, jsonObj)

        if statusCode == 201:
            result = True if content is None else content

        Policy.logger.exitMethod(methodName, str(result))
        return result

    def getPolicyAttachment(self, sortBy=None, filter=None):
        methodName = "getPolicyAttachment()"
        Policy.logger.enterMethod(methodName)
        result = None

        parameters = {}
        Utils.addOnStringValue(parameters, "sortBy", sortBy)
        Utils.addOnStringValue(parameters, "filter", filter)

        statusCode, content = self.httpGetJson(Policy.POLICY_ATTACHEMENTS, parameters=parameters)

        if statusCode == 200 and content is not None:
            result = content

        Policy.logger.exitMethod(methodName, str(result))
        return result

    def publishPolicyAttachment(self, id):
        methodName = "publishPolicyAttachment()"
        Policy.logger.enterMethod(methodName)
        result = None

        endpoint = "%s/deployment/%s" % (Policy.POLICY_ATTACHEMENTS, str(id))
        statusCode, content = self.httpPutJson(endpoint)

        if statusCode == 204:
            result = True if content is None else content

        Policy.logger.exitMethod(methodName, str(result))
        return result

    #
    # API Protection
    #

    # Mapping Rules

    def createMappingRule(self, name, category, fileName, content=""):
        methodName = "createMappingRule()"
        Policy.logger.enterMethod(methodName)
        result = None

        jsonObj = {}
        Utils.addOnStringValue(jsonObj, "name", name)
        Utils.addOnStringValue(jsonObj, "category", category)
        Utils.addOnStringValue(jsonObj, "fileName", fileName)
        Utils.addOnStringValue(jsonObj, "content", content)

        statusCode, content = self.httpPostJson(Policy.MAPPING_RULES, jsonObj)

        if statusCode == 200:
            result = True if content is None else content

        Policy.logger.exitMethod(methodName, str(result))
        return result

    def getMappingRules(self, sortBy=None, count=None, start=None, filter=None):
        methodName = "getMappingRules()"
        Policy.logger.enterMethod(methodName)
        result = None

        parameters = {}
        Utils.addOnStringValue(parameters, "sortBy", sortBy)
        Utils.addOnStringValue(parameters, "count", count)
        Utils.addOnStringValue(parameters, "start", start)
        Utils.addOnStringValue(parameters, "filter", filter)

        statusCode, content = self.httpGetJson(Policy.MAPPING_RULES, parameters=parameters)

        if statusCode == 200 and content is not None:
            result = content

        Policy.logger.exitMethod(methodName, str(result))
        return result

    def updateMappingRule(self, id, content=""):
        methodName = "updateMappingRule()"
        Policy.logger.enterMethod(methodName)
        result = None

        jsonObj = {}
        Utils.addOnStringValue(jsonObj, "content", content)

        endpoint = "%s/%s" % (Policy.MAPPING_RULES, str(id))
        statusCode, content = self.httpPutJson(endpoint, jsonObj)

        if statusCode == 204:
            result = True if content is None else content

        Policy.logger.exitMethod(methodName, str(result))
        return result

    # OAuth 2.0 Support

    def createApiProtectionClient(self, name=None, redirectUri=None, companyName=None, companyUrl=None, \
            contactPerson=None, contactType=None, email=None, phone=None, otherInfo=None, definition=None, \
            clientId=None, clientSecret=None):
        methodName = "createApiProtectionClient()"
        Policy.logger.enterMethod(methodName)
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

        statusCode, content = self.httpPostJson(Policy.CLIENTS, jsonObj)

        if statusCode == 201:
            result = True if content is None else content

        Policy.logger.exitMethod(methodName, str(result))
        return result

    def createApiProtectionDefinition(self, name=None, description=None, tcmBehavior=None, tokenCharSet=None, \
            accessTokenLifetime=None, accessTokenLength=None, authorizationCodeLifetime=None, \
            authorizationCodeLength=None, refreshTokenLength=None, maxAuthorizationGrantLifetime=None, pinLength=None, \
            enforceSingleUseAuthorizationGrant=None, issueRefreshToken=None, enforceSingleAccessTokenPerGrant=None, \
            enableMultipleRefreshTokensForFaultTolerance=None, pinPolicyEnabled=None, grantTypes=[]):
        methodName = "createApiProtectionDefinition()"
        Policy.logger.enterMethod(methodName)
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
        Utils.addOnValue(jsonObj, "enforceSingleUseAuthorizationGrant", enforceSingleUseAuthorizationGrant)
        Utils.addOnValue(jsonObj, "issueRefreshToken", issueRefreshToken)
        Utils.addOnValue(jsonObj, "enforceSingleAccessTokenPerGrant", enforceSingleAccessTokenPerGrant)
        Utils.addOnValue(jsonObj, "enableMultipleRefreshTokensForFaultTolerance", enableMultipleRefreshTokensForFaultTolerance)
        Utils.addOnValue(jsonObj, "pinPolicyEnabled", pinPolicyEnabled)
        Utils.addOnValue(jsonObj, "grantTypes", grantTypes)

        statusCode, content = self.httpPostJson(Policy.DEFINITIONS, jsonObj)

        if statusCode == 201:
            result = True if content is None else content

        Policy.logger.exitMethod(methodName, str(result))
        return result

    def getApiProtectionDefinitions(self, sortBy=None, count=None, start=None, filter=None):
        methodName = "getApiProtectionDefinitions()"
        Policy.logger.enterMethod(methodName)
        result = None

        parameters = {}
        Utils.addOnStringValue(parameters, "sortBy", sortBy)
        Utils.addOnStringValue(parameters, "count", count)
        Utils.addOnStringValue(parameters, "start", start)
        Utils.addOnStringValue(parameters, "filter", filter)

        statusCode, content = self.httpGetJson(Policy.DEFINITIONS, parameters=parameters)

        if statusCode == 200 and content is not None:
            result = content

        Policy.logger.exitMethod(methodName, str(result))
        return result

    #
    # Attributes
    #

    # Attribute Matchers

    def getAttributeMatcherByUri(self, uri):
        methodName = "getAttributeMatcherByUri()"
        Policy.logger.enterMethod(methodName)
        result = None

        uriEquals = "uri equals %s" % str(uri)
        matchers = self.getAttributeMatchers(filter=uriEquals)

        if matchers is not None and len(matchers) > 0:
            result = matchers[0]

        return result

    def getAttributeMatchers(self, sortBy=None, filter=None):
        methodName = "getAttributeMatchers()"
        Policy.logger.enterMethod(methodName)
        result = None

        parameters = {}
        Utils.addOnStringValue(parameters, "sortBy", sortBy)
        Utils.addOnStringValue(parameters, "filter", filter)

        statusCode, content = self.httpGetJson(Policy.ATTRIBUTE_MATCHERS, parameters=parameters)

        if statusCode == 200 and content is not None:
            result = content

        Policy.logger.exitMethod(methodName, str(result))
        return result

    # Attributes

    def createAttribute(self, category=None, matcher=None, issuer=None, description=None, name=None, datatype=None, \
            uri=None, sessionStorage=None, behaviorStorage=None, deviceStorage=None, riskType=None, policyType=None):
        methodName = "createAttribute()"
        Policy.logger.enterMethod(methodName)
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

        statusCode, content = self.httpPostJson(Policy.ATTRIBUTES, jsonObj)

        if statusCode == 201:
            result = True if content is None else content

        Policy.logger.exitMethod(methodName, str(result))
        return result

    def getAttributeByUri(self, uri):
        methodName = "getAttributeByUri()"
        Policy.logger.enterMethod(methodName)
        result = None

        uriEquals = "uri equals %s" % str(uri)
        attributes = self.getAttributes(filter=uriEquals)

        if attributes is not None and len(attributes) > 0:
            result = attributes[0]

        Policy.logger.exitMethod(methodName, str(result))
        return result

    def getAttributes(self, sortBy=None, count=None, start=None, filter=None):
        methodName = "getAttributes()"
        Policy.logger.enterMethod(methodName)
        result = None

        parameters = {}
        Utils.addOnStringValue(parameters, "sortBy", sortBy)
        Utils.addOnStringValue(parameters, "count", count)
        Utils.addOnStringValue(parameters, "start", start)
        Utils.addOnStringValue(parameters, "filter", filter)

        statusCode, content = self.httpGetJson(Policy.ATTRIBUTES, parameters=parameters)

        if statusCode == 200 and content is not None:
            result = content

        Policy.logger.exitMethod(methodName, str(result))
        return result

    #
    # Authentication
    #

    # Authentication Mechanism Types

    def getAuthenticationMechanismTypes(self, sortBy=None, count=None, start=None, filter=None):
        methodName = "getAuthenticationMechanismTypes()"
        Policy.logger.enterMethod(methodName)
        result = None

        parameters = {}
        Utils.addOnStringValue(parameters, "sortBy", sortBy)
        Utils.addOnStringValue(parameters, "count", count)
        Utils.addOnStringValue(parameters, "start", start)
        Utils.addOnStringValue(parameters, "filter", filter)

        statusCode, content = self.httpGetJson(Policy.AUTHENTICATION_MECHANISM_TYPES, parameters=parameters)

        if statusCode == 200 and content is not None:
            result = content

        Policy.logger.exitMethod(methodName, str(result))
        return result

    # Authentication Mechanisms

    def createAuthenticationMechanism(self, description=None, name=None, uri=None, typeId=None, properties=None, attributes=None, jsonObj=None):
        methodName = "createAuthenticationMechanism()"
        Policy.logger.enterMethod(methodName)
        result = None

        if jsonObj is None:
            jsonObj = {}
            Utils.addOnStringValue(jsonObj, "description", description)
            Utils.addOnStringValue(jsonObj, "name", name)
            Utils.addOnStringValue(jsonObj, "uri", uri)
            Utils.addOnStringValue(jsonObj, "typeId", typeId)
            Utils.addOnValue(jsonObj, "properties", properties)
            Utils.addOnValue(jsonObj, "attributes", attributes)

        statusCode, content = self.httpPostJson(Policy.AUTHENTICATION_MECHANISMS, jsonObj)

        if statusCode == 201:
            result = True if content is None else content

        Policy.logger.exitMethod(methodName, str(result))
        return result

    def getAuthenticationMechanismByUri(self, uri):
        methodName = "getAuthenticationMechanismByUri()"
        Policy.logger.enterMethod(methodName)
        result = None

        uriEquals = "uri equals %s" % str(uri)
        mechanisms = self.getAuthenticationMechanisms(filter=uriEquals)

        if mechanisms is not None and len(mechanisms) > 0:
            result = mechanisms[0]

        Policy.logger.exitMethod(methodName, str(result))
        return result

    def getAuthenticationMechanisms(self, sortBy=None, count=None, start=None, filter=None):
        methodName = "getAuthenticationMechanisms()"
        Policy.logger.enterMethod(methodName)
        result = None

        parameters = {}
        Utils.addOnStringValue(parameters, "sortBy", sortBy)
        Utils.addOnStringValue(parameters, "count", count)
        Utils.addOnStringValue(parameters, "start", start)
        Utils.addOnStringValue(parameters, "filter", filter)

        statusCode, content = self.httpGetJson(Policy.AUTHENTICATION_MECHANISMS, parameters=parameters)

        if statusCode == 200 and content is not None:
            result = content

        Policy.logger.exitMethod(methodName, str(result))
        return result

    def updateAuthenticationMechanism(self, id, description=None, name=None, uri=None, typeId=None, predefined=None, properties=None, attributes=None, jsonObj=None):
        methodName = "updateAuthenticationMechanism()"
        Policy.logger.enterMethod(methodName)
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

        endpoint = "%s/%s" % (Policy.AUTHENTICATION_MECHANISMS, str(id))
        statusCode, content = self.httpPutJson(endpoint, jsonObj)

        if statusCode == 204:
            result = True if content is None else content

        Policy.logger.exitMethod(methodName, str(result))
        return result

    # Authentication Policies

    def createAuthenticationPolicies(self, name=None, policy=None, uri=None, description=None, dialect=None, id=None, \
            userlastmodified=None, lastmodified=None, datecreated=None, jsonObj=None):
        methodName = "createAuthenticationPolicies()"
        Policy.logger.enterMethod(methodName)
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

        statusCode, content = self.httpPostJson(Policy.AUTHENTICATION_POLICIES, jsonObj)

        if statusCode == 201:
            result = True if content is None else content

        Policy.logger.exitMethod(methodName, str(result))
        return result

    #
    # Risk Profiles
    #

    def createRiskProfile(self, description=None, name=None, active=None, attributes=None, jsonObj=None):
        methodName = "createRiskProfile()"
        Policy.logger.enterMethod(methodName)
        result = None

        if jsonObj is None:
            jsonObj = {}
            Utils.addOnStringValue(jsonObj, "description", description)
            Utils.addOnStringValue(jsonObj, "name", name)
            Utils.addOnValue(jsonObj, "active", active)
            Utils.addOnValue(jsonObj, "attributes", attributes)
            Utils.addOnValue(jsonObj, "predefined", False)

        statusCode, content = self.httpPostJson(Policy.RISK_PROFILES, jsonObj)

        if statusCode == 201:
            result = True if content is None else content

        Policy.logger.exitMethod(methodName, str(result))
        return result
