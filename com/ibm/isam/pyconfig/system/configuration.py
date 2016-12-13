"""
@copyright: IBM
"""

import logging

from com.ibm.isam.util.logger import Logger
from com.ibm.isam.util.restclient import RestClient

from .system import SystemSettings9020


PENDING_CHANGES = "/isam/pending_changes"
PENDING_CHANGES_DEPLOY = "/isam/pending_changes/deploy"


class _Configuration(RestClient):

    logger = Logger("Configuration")

    def __init__(self, base_url, username, password, log_level=logging.NOTSET):
        super(_Configuration, self).__init__(
            base_url, username, password, log_level)
        _Configuration.logger.set_level(log_level)

    #
    # Pending Changes
    #

    def deploy_pending_changes(self):
        method_name = "deploy_pending_changes()"
        _Configuration.logger.enter_method(method_name)
        result = None

        success, status_code, content = self.get_pending_changes()

        if success:
            if content.get("changes", []):
                result = self.deploy_pending_changes()
            else:
                _Configuration.logger.log(
                    method_name, "No pending changes to be deployed.")
                result = (True, status_code, content)
        else:
            result = (False, status_code, content)

        _Configuration.logger.exit_method(method_name, result)
        return result

    def get_pending_changes(self):
        method_name = "get_pending_changes()"
        _Configuration.logger.enter_method(method_name)
        result = None

        status_code, content = self.http_get_json(PENDING_CHANGES)

        result = (status_code == 200, status_code, content)

        _Configuration.logger.exit_method(method_name, result)
        return result

    def deploy_pending_changes(self):
        method_name = "deploy_pending_changes()"
        _Configuration.logger.enter_method(method_name)
        result = None

        status_code, content = self.http_get_json(PENDING_CHANGES_DEPLOY)

        if status_code == 200 and content and content.get("result", -1) == 0:
            status = content.get("status")
            result = (True, status_code, content)

            if status == 0:
                _Configuration.logger.log(
                    method_name,
                    "Successful operation. No further action needed.")
            else:
                if (status & 1) != 0:
                    _Configuration.logger.error(
                        method_name,
                        "Deployment of changes resulted in good result but failure status: " + str(status))
                    result = (False, status_code, content)
                if (status & 2) != 0:
                    _Configuration.logger.error(
                        method_name,
                        "Appliance restart required - halting: " + str(status))
                    result = (False, status_code, content)
                if (status & 4) != 0 or (status & 8) != 0:
                    _Configuration.logger.log(
                        method_name,
                        "Restarting LMI as required for status: " + str(status))
                    self._restart_lmi()
                if (status & 16) != 0:
                    _Configuration.logger.log(
                        method_name,
                        "Deployment of changes indicates a server needs restarting: " + str(status))
                if (status & 32) != 0:
                    _Configuration.logger.log(
                        method_name,
                        "Runtime restart was performed for status: " + str(status))
                    # TODO: Wait for Runtime to restart...
        else:
            result = (False, status_code, content)

        _Configuration.logger.exit_method(method_name, result)
        return result

    def _restart_lmi(self):
        pass


class Configuration9020(_Configuration):

    logger = Logger("Configuration9020")

    def __init__(self, base_url, username, password, log_level=logging.NOTSET):
        super(Configuration9020, self).__init__(
            base_url, username, password, log_level)
        Configuration9020.logger.set_level(log_level)

    def _restart_lmi(self):
        systemSettings = SystemSettings9020(
            self._base_url, self._username, self._password,
            Configuration9020.logger.get_level())
        systemSettings.restart_lmi()
