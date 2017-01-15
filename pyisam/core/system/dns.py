"""
@copyright: IBM
"""

import logging

from pyisam.util.model import DataObject
from pyisam.util.restclient import RESTClient


NET_DNS = "/net/dns"

logger = logging.getLogger(__name__)


class DNS(object):

    def __init__(self, base_url, username, password):
        super(DNS, self).__init__()
        self.client = RESTClient(base_url, username, password)

    def get(self):
        response = self.client.get_json(NET_DNS)
        response.success = response.status_code == 200

        return response

    def update(
            self, auto=True, auto_from_interface=None, primary_server=None,
            secondary_server=None, tertiary_server=None, search_domains=None):
        data = DataObject()
        data.add_value("auto", auto)
        data.add_value_string("autoFromInterface", auto_from_interface)
        data.add_value_string("primaryServer", primary_server)
        data.add_value_string("secondaryServer", secondary_server)
        data.add_value_string("tertiaryServer", tertiary_server)
        data.add_value_string("searchDomains", search_domains)

        response = self.client.put_json(NET_DNS, data.data)
        response.success = response.status_code == 200

        return response
