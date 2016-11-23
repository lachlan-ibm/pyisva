"""
Created on Nov 22, 2016

@copyright: IBM
"""
from com.ibm.isam.pyconfig.Base import Base
import logging, time, uuid

class NetworkSettings(Base):

    HOST_RECORDS = "/isam/host_records"
    NET_DNS = "/net/dns"
    NET_INTERFACES = "/net/ifaces/"

    def __init__(self, baseUrl, username, password, logLevel=logging.ERROR):
        super(NetworkSettings, self).__init__(baseUrl, username, password)

        self.logger = logging.getLogger("NetworkSettings")
        self.logger.setLevel(logLevel)

    #
    # DNS
    #

    def getDNS(self):
        description = "Retrieving DNS configuration"
        self.logEntry(description)

        statusCode, content = self.getJSON("DNS configuration", NetworkSettings.NET_DNS)

        if statusCode == 200 and content is not None:
            self.logSuccess(description)
            return content

        self.logFailed(description)

    def updateDNS(self, auto=True, autoFromInterface=None, primaryServer=None, secondaryServer=None, tertiaryServer=None, searchDomains=None):
        description = "Updating DNS configuration"
        self.logEntry(description)

        jsonObj = {}

        content = self.getDNS()

        if content is not None:
            jsonObj = content

        self.addOnValue(jsonObj, "auto", auto)
        if auto is False:
            self.addOnStringValue(jsonObj, "autoFromInterface", autoFromInterface)
            self.addOnStringValue(jsonObj, "primaryServer", primaryServer)
            self.addOnStringValue(jsonObj, "secondaryServer", secondaryServer)
            self.addOnStringValue(jsonObj, "tertiaryServer", tertiaryServer)
            self.addOnStringValue(jsonObj, "searchDomains", searchDomains)

        statusCode, content = self.putJSON("DNS configuration", NetworkSettings.NET_DNS, jsonObj)

        if statusCode == 200:
            self.logSuccess(description)
            return (content or True)

        self.logFailed(description)

    #
    # Hosts File
    #

    def addToHostRecord(self, ipv4Address, hostname):
        description = "Adding hostname to Host record"
        self.logEntry(description)

        jsonObj = {}
        self.addOnStringValue(jsonObj, "name", hostname)

        ipv4HostEndpoint = NetworkSettings.HOST_RECORDS + "/" + ipv4Address + "/hostnames"
        statusCode, content = self.postJSON("Host records", ipv4HostEndpoint, jsonObj)

        if statusCode == 200:
            self.logSuccess(description)
            return (content or True)

        self.logFailed(description)

    def createHostRecord(self, ipv4Address, hostNames):
        description = "Creating Host record"
        self.logEntry(description)

        hostNameList = str(hostNames).split(",")

        if self.getHostRecord(ipv4Address) is not None:
            success = False

            for index in range(len(hostNameList)):
                if self.addToHostRecord(ipv4Address, hostNameList[index]) is not None:
                    success = True

            if success:
                self.logSuccess(description)
                return True
        else:
            jsonObj = {}
            self.addOnStringValue(jsonObj, "addr", ipv4Address)
            self.addOnValue(jsonObj, "hostnames", [])
            for index in range(len(hostNameList)):
                jsonObj["hostnames"].append({"name":str(hostNameList[index])})

            statusCode, content = self.postJSON("Host records", NetworkSettings.HOST_RECORDS, jsonObj)

            if statusCode == 200:
                self.logSuccess(description)
                return (content or True)

        self.logFailed(description)

    def getHostRecord(self, ipv4Address):
        description = "Retrieving Host record"
        self.logEntry(description)

        ipv4HostEndpoint = NetworkSettings.HOST_RECORDS + "/" + ipv4Address + "/hostnames"
        statusCode, content = self.getJSON("Host records", ipv4HostEndpoint)

        if statusCode == 200 and content is not None:
            self.logSuccess(description)
            return content

        self.logFailed(description)

    #
    # Interfaces
    #

    def createIPAddress(self, ipv4Address, netmask, interfaceLabel="1.1", enabled=True, management=False):
        description = "Creating IP address"
        self.logEntry(description)

        content = self.getInterfaces()

        if content is not None:
            for index in range(len(content.get("interfaces", []))):
                if content["interfaces"][index].get("label") == str(interfaceLabel):
                    jsonObj = content["interfaces"][index]

                    addresses = jsonObj.get("ipv4", {}).get("addresses", [])
                    for i in range(len(addresses)):
                        if addresses[i].get("address") == str(ipv4Address):
                            self.logSuccess("The IP address is already configured [%s]" % ipv4Address)
                            return True

                    addressObj = {}
                    self.addOnValue(addressObj, "enabled", enabled)
                    self.addOnStringValue(addressObj, "maskOrPrefix", netmask)
                    self.addOnStringValue(addressObj, "address", ipv4Address)
                    self.addOnValue(addressObj, "allowManagement", management)
                    self.addOnStringValue(addressObj, "uuid", uuid.uuid4())

                    jsonObj["ipv4"]["addresses"].append(addressObj)
                    statusCode, content = self.putJSON("Single Interface", self.NET_INTERFACES + "/" + str(jsonObj['uuid']), jsonObj)
                    if statusCode == 200:
                        self.logSuccess(description)
                        return (content or True)

        self.logFailed(description)

    def getInterfaces(self):
        description = "Retrieving Interfaces"
        self.logEntry(description)

        statusCode, content = self.getJSON("Interfaces", self.NET_INTERFACES)

        if statusCode == 200 and content is not None:
            self.logSuccess(description)
            return content

        self.logFailed(description)
