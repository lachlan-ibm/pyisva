"""
Created on Nov 22, 2016

@copyright: IBM
"""

import logging
import uuid

from com.ibm.isam.util.logger import Logger
from com.ibm.isam.util.restclient import RestClient
import com.ibm.isam.util.utils as Utils


class _NetworkSettings(RestClient):

    HOST_RECORDS = "/isam/host_records"
    NET_DNS = "/net/dns"
    NET_INTERFACES = "/net/ifaces/"

    logger = Logger("NetworkSettings")

    def __init__(self, baseUrl, username, password, logLevel=logging.NOTSET):
        super(_NetworkSettings, self).__init__(baseUrl, username, password, logLevel)
        _NetworkSettings.logger.setLevel(logLevel)

    #
    # DNS
    #

    def getDns(self):
        methodName = "getDns()"
        _NetworkSettings.logger.enterMethod(methodName)
        result = None

        statusCode, content = self.httpGetJson(_NetworkSettings.NET_DNS)

        result = (statusCode == 200, statusCode, content)

        _NetworkSettings.logger.exitMethod(methodName, str(result))
        return result

    def updateDns(self, auto=True, autoFromInterface=None, primaryServer=None, secondaryServer=None,
                  tertiaryServer=None, searchDomains=None):
        methodName = "updateDns()"
        _NetworkSettings.logger.enterMethod(methodName)
        result = None

        content = self.getDns()

        jsonObj = {} if content is None else content
        Utils.addOnValue(jsonObj, "auto", auto)
        if auto is False:
            Utils.addOnStringValue(jsonObj, "autoFromInterface", autoFromInterface)
            Utils.addOnStringValue(jsonObj, "primaryServer", primaryServer)
            Utils.addOnStringValue(jsonObj, "secondaryServer", secondaryServer)
            Utils.addOnStringValue(jsonObj, "tertiaryServer", tertiaryServer)
            Utils.addOnStringValue(jsonObj, "searchDomains", searchDomains)

        statusCode, content = self.httpPutJson(_NetworkSettings.NET_DNS, jsonObj)

        result = (statusCode == 200, statusCode, content)

        _NetworkSettings.logger.exitMethod(methodName, str(result))
        return result

    #
    # Hosts File
    #

    def addHostsFileHostname(self, address, hostname):
        methodName = "addHostsFileHostname()"
        _NetworkSettings.logger.enterMethod(methodName)
        result = None

        jsonObj = {}
        Utils.addOnStringValue(jsonObj, "name", hostname)

        endpoint = "%s/%s/hostnames" % (_NetworkSettings.HOST_RECORDS, address)
        statusCode, content = self.httpPostJson(endpoint, jsonObj)

        result = (statusCode == 200, statusCode, content)

        _NetworkSettings.logger.exitMethod(methodName, str(result))
        return result

    def createHostsFileRecord(self, address, hostnames):
        methodName = "createHostsFileRecord()"
        _NetworkSettings.logger.enterMethod(methodName)
        result = None

        jsonObj = {}
        Utils.addOnStringValue(jsonObj, "addr", address)
        jsonObj["hostnames"] = []
        for index in range(len(hostnames)):
            jsonObj["hostnames"].append({"name":str(hostnames[index])})

        statusCode, content = self.httpPostJson(_NetworkSettings.HOST_RECORDS, jsonObj)

        result = (statusCode == 200, statusCode, content)

        _NetworkSettings.logger.exitMethod(methodName, str(result))
        return result

    def getHostsFileRecord(self, address):
        methodName = "getHostsFileRecord()"
        _NetworkSettings.logger.enterMethod(methodName)
        result = None

        endpoint = "%s/%s/hostnames" % (_NetworkSettings.HOST_RECORDS, address)
        statusCode, content = self.httpGetJson(endpoint)

        result = (statusCode == 200, statusCode, content)

        _NetworkSettings.logger.exitMethod(methodName, str(result))
        return result

    #
    # Interfaces
    #

    def createInterfaceIpAddress(self, ipv4Address, netmask, interfaceLabel="1.1", enabled=True, management=False):
        methodName = "createInterfaceIpAddress()"
        _NetworkSettings.logger.enterMethod(methodName)
        result = None

        success, statusCode, content = self.getInterfaces()

        if success:
            for index in range(len(content.get("interfaces", []))):
                if content["interfaces"][index].get("label") == str(interfaceLabel):
                    jsonObj = content["interfaces"][index]

                    addressObj = {}
                    Utils.addOnStringValue(addressObj, "maskOrPrefix", netmask)
                    Utils.addOnStringValue(addressObj, "address", ipv4Address)
                    Utils.addOnStringValue(addressObj, "uuid", uuid.uuid4())
                    Utils.addOnValue(addressObj, "enabled", enabled)
                    Utils.addOnValue(addressObj, "allowManagement", management)

                    jsonObj["ipv4"]["addresses"].append(addressObj)

                    endpoint = "%s/%s" % (_NetworkSettings.NET_INTERFACES, str(jsonObj.get("uuid")))
                    statusCode, content = self.httpPutJson(endpoint, jsonObj)

                    result = (statusCode == 200, statusCode, content)

            if result is None:
                result = (False, statusCode, content)
        else:
            result = (success, statusCode, content)

        _NetworkSettings.logger.exitMethod(methodName, str(result))
        return result

    def getInterfaces(self):
        methodName = "getInterfaces()"
        _NetworkSettings.logger.enterMethod(methodName)
        result = None

        statusCode, content = self.httpGetJson(_NetworkSettings.NET_INTERFACES)

        result = (statusCode == 200, statusCode, content)

        _NetworkSettings.logger.exitMethod(methodName, str(result))
        return result


class NetworkSettings9020(_NetworkSettings):

    logger = Logger("NetworkSettings9020")

    def __init__(self, baseUrl, username, password, logLevel=logging.NOTSET):
        super(NetworkSettings9020, self).__init__(baseUrl, username, password, logLevel)
        NetworkSettings9020.logger.setLevel(logLevel)
