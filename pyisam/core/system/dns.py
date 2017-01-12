"""
@copyright: IBM
"""

import logging

from pyisam.util.restclient import RestClient
import pyisam.util.common as Utils


NET_DNS = "/net/dns"

logger = logging.getLogger(__name__)


class DNS(RestClient):

    def __init__(self, base_url, username, password):
        super(DNS, self).__init__(base_url, username, password)

    def get(self):
        #logger.enter()

        status_code, content = self.http_get_json(NET_DNS)

        result = (status_code == 200, status_code, content)

        #logger.exit(result)
        return result

    def update(
            self, auto=True, auto_from_interface=None, primary_server=None,
            secondary_server=None, tertiary_server=None, search_domains=None):
        #logger.enter()

        data = {}

        success, status_code, content = self.get()

        if success:
            data = content

        Utils.add_value(data, "auto", auto)
        if not auto:
            Utils.add_value_string(
                data, "autoFromInterface", auto_from_interface)
            Utils.add_value_string(data, "primaryServer", primary_server)
            Utils.add_value_string(data, "secondaryServer", secondary_server)
            Utils.add_value_string(data, "tertiaryServer", tertiary_server)
            Utils.add_value_string(data, "searchDomains", search_domains)

        status_code, content = self.http_put_json(NET_DNS, data)

        result = (status_code == 200, status_code, content)

        #logger.exit(result)
        return result
