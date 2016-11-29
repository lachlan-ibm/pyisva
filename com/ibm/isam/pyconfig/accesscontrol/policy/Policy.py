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

    AUTHENTICATION_MECHANISMS = "/iam/access/v8/authentication/mechanisms"
    AUTHENTICATION_MECHANISM_TYPES = "/iam/access/v8/authentication/mechanism/types"
    AUTHENTICATION_POLICIES = "/iam/access/v8/authentication/policies"
    CLIENTS = "/iam/access/v8/clients"
    DEFINITIONS = "/iam/access/v8/definitions"
    MAPPING_RULES = "/iam/access/v8/mapping-rules"
    POLICY_ATTACHMENTS_PDADMIN = "/iam/access/v8/policyattachments/pdadmin"

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
    # Common Use Case Functionality
    #
    # Note: All the following methods will start with the character 'x' to
    # represent extra functionality.
    #

    def xgetAuthenticationMechanismByUri(self, uri):
        methodName = "xgetAuthenticationMechanismByUri()"
        Policy.logger.enterMethod(methodName)
        result = None

        uriEquals = "uri equals %s" % str(uri)
        content = self.getAuthenticationMechanisms(filter=uriEquals)

        if content is not None and len(content) > 0:
            result = content[0]

        Policy.logger.exitMethod(methodName, str(result))
        return result
