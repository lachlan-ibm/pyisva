"""
@copyright: IBM
"""

import logging
import uuid

from pyisam.util.model import DataObject
from pyisam.util.restclient import RESTClient


NET_INTERFACES = "/net/ifaces"

logger = logging.getLogger(__name__)


class Interfaces(object):

    def __init__(self, base_url, username, password):
        super(Interfaces, self).__init__()
        self.client = RESTClient(base_url, username, password)

    def create_address(
            self, interface_label, address=None, mask_or_prefix=None,
            enabled=True, allow_management=False):
        """
        DO NOT USE! This method is scheduled for removal.
        """
        response = self.list_interfaces()

        if response.success:
            found = False
            for entry in response.json.get("interfaces", []):
                if entry.get("label") == interface_label:
                    found = True
                    data = entry

                    address_data = DataObject()
                    address_data.add_value_string("uuid", uuid.uuid4())
                    address_data.add_value_string("address", address)
                    address_data.add_value_string(
                        "maskOrPrefix", mask_or_prefix)
                    address_data.add_value("enabled", enabled)
                    address_data.add_value("allowManagement", allow_management)

                    data["ipv4"]["addresses"].append(address_data.data)

                    endpoint = ("%s/%s" % (NET_INTERFACES, data.get("uuid")))

                    response = self.client.put_json(endpoint, data)
                    response.success = response.status_code == 200
            if not found:
                response.success = False

        return response

    def list_interfaces(self):
        response = self.client.get_json(NET_INTERFACES)
        response.success = response.status_code == 200

        return response
