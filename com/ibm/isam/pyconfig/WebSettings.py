"""
Created on Nov 21, 2016

@copyright: IBM
"""
from com.ibm.isam.pyconfig.Common import Common
import logging

class WebSettings(Common):

    RUNTIME_COMPONENT = "/isam/runtime_components"

    def __init__(self, baseUrl, username, password, logLevel=logging.INFO):
        super(WebSettings, self).__init__(baseUrl, username, password)

        self.logger = logging.getLogger("WebSettings")
        self.logger.setLevel(logLevel)

    def configureRuntimeComponent(self, psMode, userRegistry, adminPassword, ldapPassword=None, adminCertLiftime=None, \
            sslCompliance=None, ldapHost=None, ldapPort=None, isamDomain=None, ldapDn=None, ldapSuffix=None, \
            ldapSslDb=None, ldapSslLabel=None, isamHost=None, isamPort=None):
        description = "Configuring Runtime Component"
        self.logger.info(description)

        jsonObj = {}
        self.addOnValue(jsonObj, "ps_mode", psMode)
        self.addOnValue(jsonObj, "user_registry", userRegistry)
        self.addOnValue(jsonObj, "admin_cert_lifetime", adminCertLiftime)
        self.addOnValue(jsonObj, "ssl_compliance", sslCompliance)
        self.addOnValue(jsonObj, "admin_pwd", adminPassword)
        self.addOnValue(jsonObj, "ldap_pwd", ldapPassword)
        self.addOnValue(jsonObj, "ldap_host", ldapHost)
        self.addOnValue(jsonObj, "ldap_port", ldapPort)
        self.addOnValue(jsonObj, "domain", isamDomain)
        self.addOnValue(jsonObj, "ldap_dn", ldapDn)
        self.addOnValue(jsonObj, "ldap_suffix", ldapSuffix)
        self.addOnValue(jsonObj, "ldap_ssl_db", ldapSslDb)
        self.addOnValue(jsonObj, "ldap_ssl_label", ldapSslLabel)
        self.addOnValue(jsonObj, "isam_host", isamHost)
        self.addOnValue(jsonObj, "isam_port", isamPort)
        statusCode, content = self.postJSON("Runtime Components", self.RUNTIME_COMPONENT, jsonObj)

        if statusCode == 200:
            self.logSuccess(description)
            return True
        elif statusCode == 500 and content.get("message", "") == "Error: WGAWA0262E   The runtime environment has already been configured.":
            self.logSuccess("The runtime environment has already been configured.")
            return True

        self.logFailed(description)
