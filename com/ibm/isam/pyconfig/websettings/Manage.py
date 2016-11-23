"""
Created on Nov 22, 2016

@copyright: IBM
"""
from com.ibm.isam.pyconfig.Base import Base
import logging

class Manage(Base):

    RUNTIME_COMPONENT = "/isam/runtime_components"

    def __init__(self, baseUrl, username, password, logLevel=logging.ERROR):
        super(Manage, self).__init__(baseUrl, username, password)

        self.logger = logging.getLogger("Manage")
        self.logger.setLevel(logLevel)

    #
    # Runtime Components
    #

    def configureRuntimeEnvironment(self, psMode, userRegistry, adminPassword, ldapPassword=None, adminCertLiftime=None, \
            sslCompliance=None, ldapHost=None, ldapPort=None, isamDomain=None, ldapDn=None, ldapSuffix=None, \
            ldapSslDb=None, ldapSslLabel=None, isamHost=None, isamPort=None):
        description = "Configuring Runtime Environment"
        self.logEntry(description)

        jsonObj = {}
        self.addOnStringValue(jsonObj, "ps_mode", psMode)
        self.addOnStringValue(jsonObj, "user_registry", userRegistry)
        self.addOnStringValue(jsonObj, "admin_cert_lifetime", adminCertLiftime)
        self.addOnStringValue(jsonObj, "ssl_compliance", sslCompliance)
        self.addOnStringValue(jsonObj, "admin_pwd", adminPassword)
        self.addOnStringValue(jsonObj, "ldap_pwd", ldapPassword)
        self.addOnStringValue(jsonObj, "ldap_host", ldapHost)
        self.addOnValue(jsonObj, "ldap_port", ldapPort)
        self.addOnStringValue(jsonObj, "domain", isamDomain)
        self.addOnStringValue(jsonObj, "ldap_dn", ldapDn)
        self.addOnStringValue(jsonObj, "ldap_suffix", ldapSuffix)
        self.addOnStringValue(jsonObj, "ldap_ssl_db", ldapSslDb)
        self.addOnStringValue(jsonObj, "ldap_ssl_label", ldapSslLabel)
        self.addOnStringValue(jsonObj, "isam_host", isamHost)
        self.addOnValue(jsonObj, "isam_port", isamPort)

        statusCode, content = self.postJSON("Runtime Components", self.RUNTIME_COMPONENT, jsonObj)

        if statusCode == 200:
            self.logSuccess(description)
            return (content or True)
        elif statusCode == 500 and content.get("message", "") == "Error: WGAWA0262E   The runtime environment has already been configured.":
            self.logSuccess("The runtime environment has already been configured.")
            return (content or True)

        self.logFailed(description)
