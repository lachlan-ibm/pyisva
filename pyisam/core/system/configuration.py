"""
@copyright: IBM
"""

import logging

from pyisam.util.restclient import RestClient
from .restartshutdown import RestartShutdown


PENDING_CHANGES = "/isam/pending_changes"
PENDING_CHANGES_DEPLOY = "/isam/pending_changes/deploy"

logger = logging.getLogger(__name__)


class Configuration(RestClient):

    def __init__(self, base_url, username, password):
        super(Configuration, self).__init__(base_url, username, password)

    def deploy_pending_changes(self):
        #logger.enter()

        success, status_code, content = self.get_pending_changes()

        if success:
            if content.get("changes", []):
                result = self._deploy_pending_changes()
            else:
                logger.info("No pending changes to be deployed.")
                result = (True, status_code, content)
        else:
            result = (False, status_code, content)

        #logger.exit(result)
        return result

    def get_pending_changes(self):
        #logger.enter()

        status_code, content = self.http_get_json(PENDING_CHANGES)

        result = (status_code == 200, status_code, content)

        #logger.exit(result)
        return result

    def _deploy_pending_changes(self):
        #logger.enter()

        status_code, content = self.http_get_json(PENDING_CHANGES_DEPLOY)

        if status_code == 200 and content and content.get("result", -1) == 0:
            status = content.get("status")
            result = (True, status_code, content)

            if status == 0:
                logger.info("Successful operation. No further action needed.")
            else:
                if (status & 1) != 0:
                    logger.error(
                        "Deployment of changes resulted in good result but failure status: %i",
                        status)
                    result = (False, status_code, content)
                if (status & 2) != 0:
                    logger.error(
                        "Appliance restart required - halting: %i", status)
                    result = (False, status_code, content)
                if (status & 4) != 0 or (status & 8) != 0:
                    logger.info(
                        "Restarting LMI as required for status: %i", status)
                    self._restart_lmi()
                if (status & 16) != 0:
                    logger.info(
                        "Deployment of changes indicates a server needs restarting: %i",
                        status)
                if (status & 32) != 0:
                    logger.info(
                        "Runtime restart was performed for status: %i", status)
                    # TODO: Wait for Runtime to restart...
        else:
            result = (False, status_code, content)

        #logger.exit(result)
        return result

    def _restart_lmi(self):
        restart_shutdown = RestartShutdown(
            self._base_url, self._username, self._password)
        restart_shutdown.restart_lmi()
