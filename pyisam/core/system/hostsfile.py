"""
@copyright: IBM
"""

import logging

from pyisam.util.restclient import RestClient
import pyisam.util.common as Utils


HOST_RECORDS = "/isam/host_records"

logger = logging.getLogger(__name__)


class HostsFile(RestClient):

    def __init__(self, base_url, username, password):
        super(HostsFile, self).__init__(base_url, username, password)

    def add_hostname(self, address, hostname=None):
        #logger.enter()

        data = {}
        Utils.add_value_string(data, "name", hostname)

        endpoint = "%s/%s/hostnames" % (HOST_RECORDS, address)
        status_code, content = self.http_post_json(endpoint, data)

        result = (status_code == 200, status_code, content)

        #logger.exit(result)
        return result

    def create_record(self, address, hostnames):
        #logger.enter()

        data = {}
        Utils.add_value_string(data, "addr", address)
        data["hostnames"] = []
        for entry in hostnames:
            data["hostnames"].append({"name":str(entry)})

        status_code, content = self.http_post_json(HOST_RECORDS, data)

        result = (status_code == 200, status_code, content)

        #logger.exit(result)
        return result

    def get_record(self, address):
        #logger.enter()

        endpoint = "%s/%s/hostnames" % (HOST_RECORDS, address)
        status_code, content = self.http_get_json(endpoint)

        result = (status_code == 200, status_code, content)

        #logger.exit(result)
        return result
