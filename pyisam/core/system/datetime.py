""""
@copyright: IBM
"""

import logging

from pyisam.util.restclient import RestClient
import pyisam.util.common as Utils


TIME_CONFIG = "/core/time_cfg"

logger = logging.getLogger(__name__)


class DateTime(RestClient):

    def __init__(self, base_url, username, password):
        super(DateTime, self).__init__(base_url, username, password)

    def update(
            self, enable_ntp=True, ntp_servers=None, time_zone=None,
            date_time="0000-00-00 00:00:00"):
        #logger.enter()

        data = {}
        Utils.add_value_string(data, "dateTime", date_time)
        Utils.add_value_string(data, "ntpServers", ntp_servers)
        Utils.add_value_string(data, "timeZone", time_zone)
        Utils.add_value(data, "enableNtp", enable_ntp)

        status_code, content = self.http_put_json(TIME_CONFIG, data)

        result = (status_code == 200, status_code, content)

        #logger.exit(result)
        return result
