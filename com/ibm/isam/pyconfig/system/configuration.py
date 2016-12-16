"""
@copyright: IBM
"""

import logging

from com.ibm.isam.util.logger import Logger
from com.ibm.isam.util.restclient import RestClient

from .system import SystemSettings


PENDING_CHANGES = "/isam/pending_changes"
PENDING_CHANGES_DEPLOY = "/isam/pending_changes/deploy"


class Configuration(RestClient):

    logger = Logger("Configuration")

    def __init__(self, base_url, username, password, log_level=logging.NOTSET):
        super(Configuration, self).__init__(
            base_url, username, password, log_level)
        Configuration.logger.set_level(log_level)

    #
    # Pending Changes
    #

    def deploy_pending_changes(self):
        Configuration.logger.enter()
        result = None

        success, status_code, content = self.get_pending_changes()

        if success:
            if content.get("changes", []):
                result = self.deploy_pending_changes()
            else:
                Configuration.logger.info("No pending changes to be deployed.")
                result = (True, status_code, content)
        else:
            result = (False, status_code, content)

        Configuration.logger.exit(result)
        return result

    def get_pending_changes(self):
        Configuration.logger.enter()
        result = None

        status_code, content = self.http_get_json(PENDING_CHANGES)

        result = (status_code == 200, status_code, content)

        Configuration.logger.exit(result)
        return result

    def deploy_pending_changes(self):
        Configuration.logger.enter()
        result = None

        status_code, content = self.http_get_json(PENDING_CHANGES_DEPLOY)

        if status_code == 200 and content and content.get("result", -1) == 0:
            status = content.get("status")
            result = (True, status_code, content)

            if status == 0:
                Configuration.logger.info(
                    "Successful operation. No further action needed.")
            else:
                if (status & 1) != 0:
                    Configuration.logger.error(
                        "Deployment of changes resulted in good result but failure status: %i",
                        status)
                    result = (False, status_code, content)
                if (status & 2) != 0:
                    Configuration.logger.error(
                        "Appliance restart required - halting: %i", status)
                    result = (False, status_code, content)
                if (status & 4) != 0 or (status & 8) != 0:
                    Configuration.logger.info(
                        "Restarting LMI as required for status: %i", status)
                    self._restart_lmi()
                if (status & 16) != 0:
                    Configuration.logger.info(
                        "Deployment of changes indicates a server needs restarting: %i",
                        status)
                if (status & 32) != 0:
                    Configuration.logger.info(
                        "Runtime restart was performed for status: %i", status)
                    # TODO: Wait for Runtime to restart...
        else:
            result = (False, status_code, content)

        Configuration.logger.exit(result)
        return result

    def _restart_lmi(self):
        systemSettings = SystemSettings(
            self._base_url, self._username, self._password,
            Configuration.logger.get_level())
        systemSettings.restart_lmi()
