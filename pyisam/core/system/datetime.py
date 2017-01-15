""""
@copyright: IBM
"""

import logging

from pyisam.util.model import DataObject
from pyisam.util.restclient import RESTClient


TIME_CONFIG = "/core/time_cfg"

logger = logging.getLogger(__name__)


class DateTime(object):

    def __init__(self, base_url, username, password):
        super(DateTime, self).__init__()
        self.client = RESTClient(base_url, username, password)

    def update(
            self, enable_ntp=True, ntp_servers=None, time_zone=None,
            date_time="0000-00-00 00:00:00"):
        data = DataObject()
        data.add_value_string("dateTime", date_time)
        data.add_value_string("ntpServers", ntp_servers)
        data.add_value_string("timeZone", time_zone)
        data.add_value("enableNtp", enable_ntp)

        response = self.client.put_json(TIME_CONFIG, data.data)
        response.success = response.status_code == 200

        return response
