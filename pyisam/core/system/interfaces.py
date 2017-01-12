"""
@copyright: IBM
"""

import logging
import uuid

from pyisam.util.restclient import RestClient
import pyisam.util.common as Utils


NET_INTERFACES = "/net/ifaces"

logger = logging.getLogger(__name__)


class Interfaces(RestClient):

    def __init__(self, base_url, username, password):
        super(Interfaces, self).__init__(base_url, username, password)

    def create_address(
            self, interface_label, address=None, mask_or_prefix=None,
            enabled=True, allow_management=False):
        #logger.enter()
        result = None

        success, status_code, content = self.list_interfaces()

        if success:
            for entry in content.get("interfaces", []):
                if entry.get("label") == interface_label:
                    data = entry

                    address_data = {}
                    Utils.add_value_string(address_data, "uuid", uuid.uuid4())
                    Utils.add_value_string(address_data, "address", address)
                    Utils.add_value_string(
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

        #logger.exit(result)
        return result

    def list_interfaces(self):
        #logger.enter()

        status_code, content = self.http_get_json(NET_INTERFACES)

        result = (status_code == 200, status_code, content)

        #logger.exit(result)
        return result
