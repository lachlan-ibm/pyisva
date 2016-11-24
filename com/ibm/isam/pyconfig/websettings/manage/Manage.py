"""
Created on Nov 22, 2016

@copyright: IBM
"""
from com.ibm.isam.util.RestClient import RestClient
from com.ibm.isam.util.Logger import Logger
import com.ibm.isam.util.Utils as Utils
import abc, logging

class Manage(RestClient):
    __metaclass__ = abc.ABCMeta

    RUNTIME_COMPONENT = "/isam/runtime_components"

    logger = Logger("Manage")

    def __init__(self, baseUrl, username, password, logLevel=logging.NOTSET):
        super(Manage, self).__init__(baseUrl, username, password, logLevel)
        Manage.logger.setLevel(logLevel)

    @abc.abstractmethod
    def getIsamVersion(self):
        pass

    #
    # Runtime Components
    #

    def configureRuntimeEnvironment(self, psMode, userRegistry, adminPassword, ldapPassword=None, adminCertLiftime=None, \
            sslCompliance=None, ldapHost=None, ldapPort=None, isamDomain=None, ldapDn=None, ldapSuffix=None, \
            ldapSslDb=None, ldapSslLabel=None, isamHost=None, isamPort=None):
        methodName = "configureRuntimeEnvironment()"
        Manage.logger.enterMethod(methodName)
        result = None

        jsonObj = {}
        Utils.addOnStringValue(jsonObj, "ps_mode", psMode)
        Utils.addOnStringValue(jsonObj, "user_registry", userRegistry)
        Utils.addOnStringValue(jsonObj, "admin_cert_lifetime", adminCertLiftime)
        Utils.addOnStringValue(jsonObj, "ssl_compliance", sslCompliance)
        Utils.addOnStringValue(jsonObj, "admin_pwd", adminPassword)
        Utils.addOnStringValue(jsonObj, "ldap_pwd", ldapPassword)
        Utils.addOnStringValue(jsonObj, "ldap_host", ldapHost)
        Utils.addOnStringValue(jsonObj, "domain", isamDomain)
        Utils.addOnStringValue(jsonObj, "ldap_dn", ldapDn)
        Utils.addOnStringValue(jsonObj, "ldap_suffix", ldapSuffix)
        Utils.addOnStringValue(jsonObj, "ldap_ssl_db", ldapSslDb)
        Utils.addOnStringValue(jsonObj, "ldap_ssl_label", ldapSslLabel)
        Utils.addOnStringValue(jsonObj, "isam_host", isamHost)
        Utils.addOnValue(jsonObj, "ldap_port", ldapPort)
        Utils.addOnValue(jsonObj, "isam_port", isamPort)

        statusCode, content = self.httpPostJson(Manage.RUNTIME_COMPONENT, jsonObj)

        if statusCode == 200:
            result = (content or True)
        elif statusCode == 500 and content.get("message", "") == "Error: WGAWA0262E   The runtime environment has already been configured.":
            Manage.logger.log(methodName, "The runtime environment has already been configured.")
            result = (content or True)

        Manage.logger.exitMethod(methodName, str(result))
        return result
