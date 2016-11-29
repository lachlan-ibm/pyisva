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

    PDADMIN = "/isam/pdadmin"
    REVERSEPROXY = "/wga/reverseproxy"
    RUNTIME_COMPONENT = "/isam/runtime_components"
    USER_REGISTRY = "/mga/user_registry"
    WGA_DEFAULTS = "/isam/wga_templates/defaults"

    logger = Logger("Manage")

    def __init__(self, baseUrl, username, password, logLevel=logging.NOTSET):
        super(Manage, self).__init__(baseUrl, username, password, logLevel)
        Manage.logger.setLevel(logLevel)

    @abc.abstractmethod
    def getIsamVersion(self):
        pass

    #
    # Reverse Proxy
    #

    def getWGADefaults(self):
        methodName = "getWGADefaults()"
        Manage.logger.enterMethod(methodName)
        result = None

        statusCode, content = self.httpGetJson(Manage.WGA_DEFAULTS)

        if statusCode == 200 and content is not None:
            result = content

        Manage.logger.exitMethod(methodName, str(result))
        return result

    # Administration pages management

    def updateAdministrationPagesRootFile(self, websealId, pageId, contents=""):
        methodName = "updateAdministrationPage()"
        Manage.logger.enterMethod(methodName)
        result = None

        jsonObj = {}
        Utils.addOnStringValue(jsonObj, "type", "file")
        Utils.addOnStringValue(jsonObj, "contents", contents)

        endpoint = "%s/%s/management_root/%s" % (Manage.REVERSEPROXY, str(websealId), str(pageId))
        statusCode, content = self.httpPutJson(endpoint, jsonObj)

        if statusCode == 200:
            result = True if content is None else content

        Manage.logger.exitMethod(methodName, str(result))
        return result

    # Configuration entry and file management

    def addConfigurationStanzaEntry(self, websealId, stanzaId, entryName, value):
        methodName = "addConfigurationStanzaEntry()"
        Manage.logger.enterMethod(methodName)
        result = None

        jsonObj = {"entries": [[str(entryName), str(value)]]}

        endpoint = "%s/%s/configuration/stanza/%s/entry_name" % (Manage.REVERSEPROXY, str(websealId), str(stanzaId))
        statusCode, content = self.httpPostJson(endpoint, jsonObj)

        if statusCode == 200:
            result = True if content is None else content

        Manage.logger.exitMethod(methodName, str(result))
        return result

    def deleteConfigurationStanzaEntry(self, websealId, stanzaId, entryName, value=None):
        methodName = "deleteConfigurationStanzaEntry()"
        Manage.logger.enterMethod(methodName)
        result = None

        endpoint = "%s/%s/configuration/stanza/%s/entry_name/%s" % (Manage.REVERSEPROXY, str(websealId), str(stanzaId), str(entryName))
        if value is not None:
            endpoint = "%s/value/%s" % (endpoint, str(value))
        statusCode, content = self.httpDeleteJson(endpoint)

        if statusCode == 200:
            result = True if content is None else content

        Manage.logger.exitMethod(methodName, str(result))
        return result

    def updateConfigurationStanzaEntry(self, websealId, stanzaId, entryName, value):
        methodName = "updateConfigurationStanzaEntry()"
        Manage.logger.enterMethod(methodName)
        result = None

        jsonObj = {}
        Utils.addOnStringValue(jsonObj, "value", value)

        endpoint = "%s/%s/configuration/stanza/%s/entry_name/%s" % (Manage.REVERSEPROXY, str(websealId), str(stanzaId), str(entryName))
        statusCode, content = self.httpPutJson(endpoint, jsonObj)

        if statusCode == 200:
            result = True if content is None else content

        Manage.logger.exitMethod(methodName, str(result))
        return result

    # Junctions

    def createJunction(self, websealId, serverHostname=None, junctionPoint=None, junctionType=None, basicAuthMode=None, \
            tfimSso=None, statefulJunction=None, preserveCookie=None, cookieIncludePath=None, transparentPathJunction=None, \
            mutualAuth=None, insertLtpaCookies=None, insertSessionCookies=None, requestEncoding=None, enableBasicAuth=None, \
            keyLabel=None, gsoResourceGroup=None, junctionCookieJavascriptBlock=None, clientIpHttp=None, versionTwoCookies=None, \
            ltpaKeyfile=None, authzRules=None, fssoConfigFile=None, username=None, password=None, serverUuid=None, virtualHostname=None, \
            serverDn=None, localIp=None, queryContents=None, caseSensitiveUrl=None, windowsStyleUrl=None, ltpaKeyfilePassword=None, \
            proxyHostname=None, smsEnvironment=None, vhostLabel=None, force=None, delegationSupport=None, scriptingSupport=None, \
            junctionHardLimit=None, junctionSoftLimit=None, serverPort=None, httpsPort=None, httpPort=None, proxyPort=None, \
            remoteHttpHeader=[]):
        methodName = "createJunction()"
        Manage.logger.enterMethod(methodName)
        result = None

        jsonObj = {}
        Utils.addOnStringValue(jsonObj, "server_hostname", serverHostname)
        Utils.addOnStringValue(jsonObj, "junction_point", junctionPoint)
        Utils.addOnStringValue(jsonObj, "junction_type", junctionType)
        Utils.addOnStringValue(jsonObj, "basic_auth_mode", basicAuthMode)
        Utils.addOnStringValue(jsonObj, "tfim_sso", tfimSso)
        Utils.addOnStringValue(jsonObj, "stateful_junction", statefulJunction)
        Utils.addOnStringValue(jsonObj, "preserve_cookie", preserveCookie)
        Utils.addOnStringValue(jsonObj, "cookie_include_path", cookieIncludePath)
        Utils.addOnStringValue(jsonObj, "transparent_path_junction", transparentPathJunction)
        Utils.addOnStringValue(jsonObj, "mutual_auth", mutualAuth)
        Utils.addOnStringValue(jsonObj, "insert_ltpa_cookies", insertLtpaCookies)
        Utils.addOnStringValue(jsonObj, "insert_session_cookies", insertSessionCookies)
        Utils.addOnStringValue(jsonObj, "request_encoding", requestEncoding)
        Utils.addOnStringValue(jsonObj, "enable_basic_auth", enableBasicAuth)
        Utils.addOnStringValue(jsonObj, "key_label", keyLabel)
        Utils.addOnStringValue(jsonObj, "gso_resource_group", gsoResourceGroup)
        Utils.addOnStringValue(jsonObj, "junction_cookie_javascript_block", junctionCookieJavascriptBlock)
        Utils.addOnStringValue(jsonObj, "client_ip_http", clientIpHttp)
        Utils.addOnStringValue(jsonObj, "version_two_cookies", versionTwoCookies)
        Utils.addOnStringValue(jsonObj, "ltpa_keyfile", ltpaKeyfile)
        Utils.addOnStringValue(jsonObj, "authz_rules", authzRules)
        Utils.addOnStringValue(jsonObj, "fsso_config_file", fssoConfigFile)
        Utils.addOnStringValue(jsonObj, "username", username)
        Utils.addOnStringValue(jsonObj, "password", password)
        Utils.addOnStringValue(jsonObj, "server_uuid", serverUuid)
        Utils.addOnStringValue(jsonObj, "virtual_hostname", virtualHostname)
        Utils.addOnStringValue(jsonObj, "server_dn", serverDn)
        Utils.addOnStringValue(jsonObj, "local_ip", localIp)
        Utils.addOnStringValue(jsonObj, "query_contents", queryContents)
        Utils.addOnStringValue(jsonObj, "case_sensitive_url", caseSensitiveUrl)
        Utils.addOnStringValue(jsonObj, "windows_style_url", windowsStyleUrl)
        Utils.addOnStringValue(jsonObj, "ltpa_keyfile_password", ltpaKeyfilePassword)
        Utils.addOnStringValue(jsonObj, "proxy_hostname", proxyHostname)
        Utils.addOnStringValue(jsonObj, "sms_environment", smsEnvironment)
        Utils.addOnStringValue(jsonObj, "vhost_label", vhostLabel)
        Utils.addOnStringValue(jsonObj, "force", force)
        Utils.addOnStringValue(jsonObj, "delegation_support", delegationSupport)
        Utils.addOnStringValue(jsonObj, "scripting_support", scriptingSupport)
        Utils.addOnValue(jsonObj, "junction_hard_limit", junctionHardLimit)
        Utils.addOnValue(jsonObj, "junction_soft_limit", junctionSoftLimit)
        Utils.addOnValue(jsonObj, "server_port", serverPort)
        Utils.addOnValue(jsonObj, "https_port", httpsPort)
        Utils.addOnValue(jsonObj, "http_port", httpPort)
        Utils.addOnValue(jsonObj, "proxy_port", proxyPort)
        Utils.addOnValue(jsonObj, "remote_http_header", remoteHttpHeader)

        endpoint = "%s/%s/junctions" % (Manage.REVERSEPROXY, str(websealId))
        statusCode, content = self.httpPostJson(endpoint, jsonObj)

        if statusCode == 200:
            result = True if content is None else content

        Manage.logger.exitMethod(methodName, str(result))
        return result

    def getJunctions(self, websealId):
        methodName = "getJunctions()"
        Manage.logger.enterMethod(methodName)
        result = None

        endpoint = "%s/%s/junctions" % (Manage.REVERSEPROXY, str(websealId))
        statusCode, content = self.httpGetJson(endpoint)

        if statusCode == 200 and content is not None:
            result = content

        Manage.logger.exitMethod(methodName, str(result))
        return result

    # Management of interfaces

    def getWebSEALInstances(self):
        methodName = "getWebSEALInstances()"
        Manage.logger.enterMethod(methodName)
        result = None

        statusCode, content = self.httpGetJson(Manage.REVERSEPROXY)

        if statusCode == 200 and content is not None:
            result = content

        Manage.logger.exitMethod(methodName, str(result))
        return result

    def configureWebSEALInstance(self, instName=None, host=None, adminId=None, adminPwd=None, \
            sslYn=None, keyFile=None, certLabel=None, sslPort=None, httpYn=None, httpPort=None, \
            httpsYn=None, httpsPort=None, nwInterfaceYn=None, ipAddress=None):
        methodName = "configureWebSEALInstance()"
        Manage.logger.enterMethod(methodName)
        result = None

        defaults = self.getWGADefaults()

        if defaults is not None:
            listeningPort = defaults.get("listening_port")
            domain = defaults.get("domain")

            jsonObj = {}
            Utils.addOnStringValue(jsonObj, "inst_name", instName)
            Utils.addOnStringValue(jsonObj, "host", host)
            Utils.addOnStringValue(jsonObj, "listening_port", listeningPort)
            Utils.addOnStringValue(jsonObj, "domain", domain)
            Utils.addOnStringValue(jsonObj, "admin_id", adminId)
            Utils.addOnStringValue(jsonObj, "admin_pwd", adminPwd)
            Utils.addOnStringValue(jsonObj, "ssl_yn", sslYn)
            Utils.addOnStringValue(jsonObj, "key_file", keyFile)
            Utils.addOnStringValue(jsonObj, "cert_label", certLabel)
            Utils.addOnStringValue(jsonObj, "ssl_port", sslPort)
            Utils.addOnStringValue(jsonObj, "http_yn", httpYn)
            Utils.addOnStringValue(jsonObj, "http_port", httpPort)
            Utils.addOnStringValue(jsonObj, "https_yn", httpsYn)
            Utils.addOnStringValue(jsonObj, "https_port", httpsPort)
            Utils.addOnStringValue(jsonObj, "nw_interface_yn", nwInterfaceYn)
            Utils.addOnStringValue(jsonObj, "ip_address", ipAddress)

            statusCode, content = self.httpPostJson(Manage.REVERSEPROXY, jsonObj)

            if statusCode == 200:
                result = True if content is None else content

        Manage.logger.exitMethod(methodName, str(result))
        return result

    #
    # Runtime Components
    #

    # Administering the Security Access Manager Base

    def doPdadminCommands(self, adminId, adminPwd, commands=[]):
        methodName = "doPdadminCommands()"
        Manage.logger.enterMethod(methodName)
        result = None

        jsonObj = {}
        Utils.addOnStringValue(jsonObj, "admin_id", adminId)
        Utils.addOnStringValue(jsonObj, "admin_pwd", adminPwd)
        Utils.addOnValue(jsonObj, "commands", commands)

        statusCode, content = self.httpPostJson(Manage.PDADMIN, jsonObj)

        if statusCode == 200:
            result = True if content is None else content

        Manage.logger.exitMethod(methodName, str(result))
        return result

    def updateUserPasswordInRegistry(self, username, password):
        methodName = "updateUserPasswordInRegistry()"
        Manage.logger.enterMethod(methodName)
        result = None

        jsonObj = {}
        Utils.addOnStringValue(jsonObj, "password", password)

        endpoint = "%s/users/%s/v1" % (Manage.USER_REGISTRY, str(username))
        statusCode, content = self.httpPutJson(endpoint, jsonObj)

        if statusCode == 204:
            result = True if content is None else content

        Manage.logger.exitMethod(methodName, str(result))
        return result

    # Managing the Security Access Manager Runtime

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
            result = True if content is None else content
        elif statusCode == 500 and content.get("message", "") == "Error: WGAWA0262E   The runtime environment has already been configured.":
            Manage.logger.log(methodName, "The runtime environment has already been configured.")
            result = True if content is None else content

        Manage.logger.exitMethod(methodName, str(result))
        return result
