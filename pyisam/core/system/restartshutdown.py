""""
@copyright: IBM
"""

import logging
import time

from pyisam.util.restclient import RestClient
import pyisam.util.common as Utils


LMI = "/lmi"
LMI_RESTART = "/restarts/restart_server"

logger = logging.getLogger(__name__)


class RestartShutdown(RestClient):

    def __init__(self, base_url, username, password):
        super(RestartShutdown, self).__init__(base_url, username, password)

    def get_lmi_status(self):
        #logger.enter()

        status_code, content = self.http_get_json(LMI)

        result = (status_code == 200, status_code, content)

        #logger.exit(result)
        return result

    def restart_lmi(self):
        #logger.enter()

        last_start = -1

        success, status_code, content = self.get_lmi_status()

        if success:
            last_start = content[0].get("start_time", -1)

        if last_start > 0:
            status_code, content = self.http_post_json(LMI_RESTART)

            if status_code == 200 and content.get("restart", False) == True:
                logger.info("Waiting for LMI to restart...")
                self._wait_on_lmi(last_start)
                result = (True, status_code, content)
            else:
                result = (False, status_code, content)
        else:
            logger.error("Invalid start time was retrieved: %i", last_start)
            result = (False, status_code, content)

        #logger.exit(result)
        return result

    def _wait_on_lmi(self, last_start, sleep_interval=3):
        #logger.enter()

        if last_start > 0:
            restart_time = last_start

            while (restart_time <= 0 or restart_time == last_start):
                logger.debug(
                    "last_start: %i, restart_time: %i", last_start,
                    restart_time)
                time.sleep(sleep_interval)

                try:
                    success, status_code, content = self.get_lmi_status()

                    if success:
                        restart_time = content[0].get("start_time", -1)
                except:
                    restart_time = -1

            time.sleep(sleep_interval)
        else:
            logger.error("Invalid last start time: %i", last_start)

        #logger.exit()
