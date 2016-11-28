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

        if statusCode == 200:
            result = True if content is None else content

        Policy.logger.exitMethod(methodName, str(result))
        return result
