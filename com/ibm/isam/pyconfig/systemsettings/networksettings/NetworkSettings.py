"""
Created on Nov 22, 2016

@copyright: IBM
"""
from com.ibm.isam.util.RestClient import RestClient
from com.ibm.isam.util.Logger import Logger
import com.ibm.isam.util.Utils as Utils
import abc, logging, uuid

class NetworkSettings(RestClient):
    __metaclass__ = abc.ABCMeta

    HOST_RECORDS = "/isam/host_records"
    NET_DNS = "/net/dns"
    NET_INTERFACES = "/net/ifaces/"

    logger = Logger("NetworkSettings")

    def __init__(self, baseUrl, username, password, logLevel=logging.NOTSET):
        super(NetworkSettings, self).__init__(baseUrl, username, password, logLevel)
        NetworkSettings.logger.setLevel(logLevel)

    @abc.abstractmethod
    def getIsamVersion(self):
        pass

    #
    # DNS
    #

    def getDNS(self):
        methodName = "getDNS()"
        NetworkSettings.logger.enterMethod(methodName)
        result = None

        statusCode, content = self.httpGetJson(NetworkSettings.NET_DNS)

        if statusCode == 200 and content is not None:
            result = content

        NetworkSettings.logger.exitMethod(methodName, str(result))
        return result

    def updateDNS(self, auto=True, autoFromInterface=None, primaryServer=None, secondaryServer=None, tertiaryServer=None, searchDomains=None):
        methodName = "updateDNS()"
        NetworkSettings.logger.enterMethod(methodName)
        result = None

        jsonObj = (self.getDNS() or {})

        Utils.addOnValue(jsonObj, "auto", auto)
        if auto is False:
            Utils.addOnStringValue(jsonObj, "autoFromInterface", autoFromInterface)
            Utils.addOnStringValue(jsonObj, "primaryServer", primaryServer)
            Utils.addOnStringValue(jsonObj, "secondaryServer", secondaryServer)
            Utils.addOnStringValue(jsonObj, "tertiaryServer", tertiaryServer)
            Utils.addOnStringValue(jsonObj, "searchDomains", searchDomains)

        statusCode, content = self.httpPutJson(NetworkSettings.NET_DNS, jsonObj)

        if statusCode == 200:
            result = (content or True)

        NetworkSettings.logger.exitMethod(methodName, str(result))
        return result

    #
    # Hosts File
    #

    def addToHostRecord(self, ipv4Address, hostname):
        methodName = "addToHostRecord()"
        NetworkSettings.logger.enterMethod(methodName)
        result = None

        jsonObj = {}
        Utils.addOnStringValue(jsonObj, "name", hostname)

        ipv4HostEndpoint = NetworkSettings.HOST_RECORDS + "/" + ipv4Address + "/hostnames"
        statusCode, content = self.httpPostJson(ipv4HostEndpoint, jsonObj)

        if statusCode == 200:
            result = (content or True)

        NetworkSettings.logger.exitMethod(methodName, str(result))
        return result

    def createHostRecord(self, ipv4Address, hostNames):
        methodName = "createHostRecord()"
        NetworkSettings.logger.enterMethod(methodName)
        result = None

        hostNameList = str(hostNames).split(",")

        if self.getHostRecord(ipv4Address) is not None:
            for index in range(len(hostNameList)):
                if self.addToHostRecord(ipv4Address, hostNameList[index]) is not None:
                    result = True
        else:
            jsonObj = {}
            Utils.addOnStringValue(jsonObj, "addr", ipv4Address)
            jsonObj["hostnames"] = []
            for index in range(len(hostNameList)):
                jsonObj["hostnames"].append({"name":str(hostNameList[index])})

            statusCode, content = self.httpPostJson(NetworkSettings.HOST_RECORDS, jsonObj)

            if statusCode == 200:
                result = True

        NetworkSettings.logger.exitMethod(methodName, str(result))
        return result

    def getHostRecord(self, ipv4Address):
        methodName = "getHostRecord()"
        NetworkSettings.logger.enterMethod(methodName)
        result = None

        ipv4HostEndpoint = NetworkSettings.HOST_RECORDS + "/" + ipv4Address + "/hostnames"
        statusCode, content = self.httpGetJson(ipv4HostEndpoint)

        if statusCode == 200 and content is not None:
            result = content

        NetworkSettings.logger.exitMethod(methodName, str(result))
        return result

    #
    # Interfaces
    #

    def createIPAddress(self, ipv4Address, netmask, interfaceLabel="1.1", enabled=True, management=False):
        methodName = "createIPAddress()"
        NetworkSettings.logger.enterMethod(methodName)
        result = None

        content = self.getInterfaces()

        if content is not None:
            for index in range(len(content.get("interfaces", []))):
                if content["interfaces"][index].get("label") == str(interfaceLabel):
                    jsonObj = content["interfaces"][index]

                    addresses = jsonObj.get("ipv4", {}).get("addresses", [])
                    for i in range(len(addresses)):
                        if addresses[i].get("address") == str(ipv4Address):
                            NetworkSettings.logger.log(methodName, "The IP address is already configured [%s]" % ipv4Address)
                            NetworkSettings.logger.exitMethod(methodName, str(True))
                            return True

                    addressObj = {}
                    Utils.addOnStringValue(addressObj, "maskOrPrefix", netmask)
                    Utils.addOnStringValue(addressObj, "address", ipv4Address)
                    Utils.addOnStringValue(addressObj, "uuid", uuid.uuid4())
                    Utils.addOnValue(addressObj, "enabled", enabled)
                    Utils.addOnValue(addressObj, "allowManagement", management)

                    jsonObj["ipv4"]["addresses"].append(addressObj)

                    interfaceEndpoint = NetworkSettings.NET_INTERFACES + "/" + str(jsonObj['uuid'])
                    statusCode, content = self.httpPutJson(interfaceEndpoint, jsonObj)

                    if statusCode == 200:
                        result = (content or True)

        NetworkSettings.logger.exitMethod(methodName, str(result))
        return result

    def getInterfaces(self):
        methodName = "getInterfaces()"
        NetworkSettings.logger.enterMethod(methodName)
        result = None

        statusCode, content = self.httpGetJson(NetworkSettings.NET_INTERFACES)

        if statusCode == 200 and content is not None:
            result = content

        NetworkSettings.logger.exitMethod(methodName, str(result))
        return result
