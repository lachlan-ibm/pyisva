"""
@copyright: IBM
"""

import logging
import uuid

from com.ibm.isam.util.logger import Logger
from com.ibm.isam.util.restclient import RestClient
import com.ibm.isam.util.utils as Utils


HOST_RECORDS = "/isam/host_records"
NET_DNS = "/net/dns"
NET_INTERFACES = "/net/ifaces"


class _NetworkSettings(RestClient):

    logger = Logger("NetworkSettings")

    def __init__(self, base_url, username, password, log_level=logging.NOTSET):
        super(_NetworkSettings, self).__init__(
            base_url, username, password, log_level)
        _NetworkSettings.logger.set_level(log_level)

    #
    # DNS
    #

    def get_dns(self):
        method_name = "get_dns()"
        _NetworkSettings.logger.enter_method(method_name)
        result = None

        status_code, content = self.http_get_json(NET_DNS)

        result = (status_code == 200, status_code, content)

        _NetworkSettings.logger.exit_method(method_name, result)
        return result

    def update_dns(
            self, auto=True, auto_from_interface=None, primary_server=None,
            secondary_server=None, tertiary_server=None, search_domains=None):
        method_name = "update_dns()"
        _NetworkSettings.logger.enter_method(method_name)
        result = None

        data = {}

        success, status_code, content = self.get_dns()

        if success:
            data = content

        Utils.add_value(data, "auto", auto)
        if not auto:
            Utils.add_string_value(
                data, "autoFromInterface", auto_from_interface)
            Utils.add_string_value(data, "primaryServer", primary_server)
            Utils.add_string_value(data, "secondaryServer", secondary_server)
            Utils.add_string_value(data, "tertiaryServer", tertiary_server)
            Utils.add_string_value(data, "searchDomains", search_domains)

        status_code, content = self.http_put_json(NET_DNS, data)

        result = (status_code == 200, status_code, content)

        _NetworkSettings.logger.exit_method(method_name, result)
        return result

    #
    # Hosts File
    #

    def add_hosts_file_hostname(self, address, hostname=None):
        method_name = "add_hosts_file_hostname()"
        _NetworkSettings.logger.enter_method(method_name)
        result = None

        data = {}
        Utils.add_string_value(data, "name", hostname)

        endpoint = "%s/%s/hostnames" % (HOST_RECORDS, address)
        status_code, content = self.http_post_json(endpoint, data)

        result = (status_code == 200, status_code, content)

        _NetworkSettings.logger.exit_method(method_name, result)
        return result

    def create_hosts_file_record(self, address, hostnames):
        method_name = "create_hosts_file_record()"
        _NetworkSettings.logger.enter_method(method_name)
        result = None

        data = {}
        Utils.add_string_value(data, "addr", address)
        data["hostnames"] = []
        for entry in hostnames:
            data["hostnames"].append({"name":str(entry)})

        status_code, content = self.http_post_json(HOST_RECORDS, data)

        result = (status_code == 200, status_code, content)

        _NetworkSettings.logger.exit_method(method_name, result)
        return result

    def get_hosts_file_record(self, address):
        method_name = "get_hosts_file_record()"
        _NetworkSettings.logger.enter_method(method_name)
        result = None

        endpoint = "%s/%s/hostnames" % (HOST_RECORDS, address)
        status_code, content = self.http_get_json(endpoint)

        result = (status_code == 200, status_code, content)

        _NetworkSettings.logger.exit_method(method_name, result)
        return result

    #
    # Interfaces
    #

    def create_interface_ip_address(
            self, interface_label, address=None, mask_or_prefix=None,
            enabled=True, allow_management=False):
        method_name = "create_interface_ip_address()"
        _NetworkSettings.logger.enter_method(method_name)
        result = None

        success, status_code, content = self.get_interfaces()

        if success:
            for entry in content.get("interfaces", []):
                if entry.get("label") == interface_label:
                    data = entry

                    address_data = {}
                    Utils.add_string_value(address_data, "uuid", uuid.uuid4())
                    Utils.add_string_value(address_data, "address", address)
                    Utils.add_string_value(
                        address_data, "maskOrPrefix", mask_or_prefix)
                    Utils.add_value(address_data, "enabled", enabled)
                    Utils.add_value(
                        address_data, "allowManagement", allow_management)

                    data["ipv4"]["addresses"].append(address_data)

                    endpoint = ("%s/%s" % (NET_INTERFACES, data.get("uuid")))
                    status_code, content = self.http_put_json(endpoint, data)

                    result = (status_code == 200, status_code, content)

            if not result:
                result = (False, status_code, content)
        else:
            result = (success, status_code, content)

        _NetworkSettings.logger.exit_method(method_name, result)
        return result

    def get_interfaces(self):
        method_name = "get_interfaces()"
        _NetworkSettings.logger.enter_method(method_name)
        result = None

        status_code, content = self.http_get_json(NET_INTERFACES)

        result = (status_code == 200, status_code, content)

        _NetworkSettings.logger.exit_method(method_name, result)
        return result


class NetworkSettings9020(_NetworkSettings):

    logger = Logger("NetworkSettings9020")

    def __init__(self, base_url, username, password, log_level=logging.NOTSET):
        super(NetworkSettings9020, self).__init__(
            base_url, username, password, log_level)
        NetworkSettings9020.logger.set_level(log_level)
