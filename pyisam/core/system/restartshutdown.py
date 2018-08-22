""""
@copyright: IBM
"""

import logging
import time

from pyisam.util.model import DataObject, Response
from pyisam.util.restclient import RESTClient


LMI = "/lmi"
LMI_RESTART = "/restarts/restart_server"
APPLIANCE_RESTART = "/diagnostics/restart_shutdown/reboot"

logger = logging.getLogger(__name__)


class RestartShutdown(object):

    def __init__(self, base_url, username, password):
        super(RestartShutdown, self).__init__()
        self.client = RESTClient(base_url, username, password)

    def get_lmi_status(self):
        response = self.client.get_json(LMI)
        response.success = response.status_code == 200

        return response

    def restart_lmi(self):
        last_start = -1

        response = self.get_lmi_status()
        if response.success:
            last_start = response.json[0].get("start_time", -1)

        if last_start > 0:
            response = self.client.post_json(LMI_RESTART)
            response.success = (response.status_code == 200
                and response.json.get("restart", False) == True)

            if response.success:
                logger.info("Waiting for LMI to restart...")
                self._wait_on_lmi(last_start)
        else:
            logger.error("Invalid start time was retrieved: %i", last_start)
            response.success = False

        return response

    def _wait_on_lmi(self, last_start, sleep_interval=3):
        if last_start > 0:
            restart_time = last_start

            while (restart_time <= 0 or restart_time == last_start):
                logger.debug(
                    "last_start: %i, restart_time: %i", last_start,
                    restart_time)
                time.sleep(sleep_interval)

                try:
                    response = self.get_lmi_status()

                    if response.success:
                        restart_time = response.json[0].get("start_time", -1)
                except:
                    restart_time = -1

            time.sleep(sleep_interval)
        else:
            logger.error("Invalid last start time: %i", last_start)

    def restart_appliance(self):
        last_start = -1

        response = self.get_lmi_status()
        if response.success:
            last_start = response.json[0].get("start_time", -1)

        if last_start > 0:
            response = self.client.post_json(APPLIANCE_RESTART)
            response.success = (response.status_code == 200
                and response.json.get("status", False) == True)

            if response.success:
                logger.info("Waiting for LMI to restart...")
                self._wait_on_lmi(last_start)
        else:
            logger.error("Invalid start time was retrieved: %i", last_start)
            response.success = False

        return response