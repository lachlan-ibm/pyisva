"""
@copyright: IBM
"""

import logging

from pyisam.util.restclient import RESTClient
from .restartshutdown import RestartShutdown


PENDING_CHANGES = "/isam/pending_changes"
PENDING_CHANGES_DEPLOY = "/isam/pending_changes/deploy"

logger = logging.getLogger(__name__)


class Configuration(object):

    def __init__(self, base_url, username, password):
        super(Configuration, self).__init__()
        self.client = RESTClient(base_url, username, password)
        self._base_url = base_url
        self._username = username
        self._password = password

    def deploy_pending_changes(self):
        response = self.get_pending_changes()

        if response.success:
            if response.json.get("changes", []):
                response = self._deploy_pending_changes()
            else:
                logger.info("No pending changes to be deployed.")

        return response

    def reverte_pending_changes(self):
        response = self.client.delete_json_json(PENDING_CHANGES)
        response.success = response.status_code == 200

        return response

    def get_pending_changes(self):
        response = self.client.get_json(PENDING_CHANGES)
        response.success = response.status_code == 200

        return response

    def _deploy_pending_changes(self):
        response = self.client.get_json(PENDING_CHANGES_DEPLOY)
        response.success = (response.status_code == 200
            and response.json.get("result", -1) == 0)

        if response.success:
            status = response.json.get("status")

            if status == 0:
                logger.info("Successful operation. No further action needed.")
            else:
                if (status & 1) != 0:
                    logger.error(
                        "Deployment of changes resulted in good result but failure status: %i",
                        status)
                    response.success = False
                if (status & 2) != 0:
                    logger.error(
                        "Appliance restart required - halting: %i", status)
                    response.success = False
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

        return response

    def _restart_lmi(self):
        restart_shutdown = RestartShutdown(
            self._base_url, self._username, self._password)
        restart_shutdown.restart_lmi()
