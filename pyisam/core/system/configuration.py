"""
@copyright: IBM
"""

import logging

from pyisam.util.restclient import RESTClient
from .restartshutdown import RestartShutdown
from pyisam.core.system.dockermanagement import DockerManagement

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
                if (status & 256) != 0:
                    logger.info(
                        "Runtime reload was performed for status: %i", status)
        return response

    def _restart_lmi(self):
        restart_shutdown = RestartShutdown(
            self._base_url, self._username, self._password)
        restart_shutdown.restart_lmi()


class DockerContainer(object):
    def __init__(self, base_url, username, password, container_name):
        self._rest_client = RESTClient(base_url, username, password)
        self._container_name = container_name

    def rest_client(self):
        return self._rest_client

    def container_name(self):
        return self._container_name


class DockerConfiguration(Configuration):
    webseal_containers = {}
    runtime_container = {}

    def __init__(self, base_url, username, password):
        Configuration.__init__(self, base_url, username, password)
        self._is_docker = True
        self.docker = DockerManagement(base_url, username, password)

    def deploy_pending_changes(self):
        response = super(DockerConfiguration, self).deploy_pending_changes()
        if response.success:
            self.docker.publish_changes()
            status = response.json.get("status")

            if status is None or status == 0:
                logger.info("No container actions required")
            else:
                logger.info("Some container actions required")
                if (status & 16) != 0:
                    for container in DockerConfiguration.webseal_containers.items():
                        self.docker.reload_all(container)
                if (status & 32) != 0:
                    self.docker.reload_all(self.runtime_container)
                if (status & 256) != 0:
                    self.docker.reload_runtime(self.runtime_container)

        return response

    @staticmethod
    def register_webseal_container(instance, container_name, base_url, username, password):
        DockerConfiguration.webseal_containers[instance] = DockerContainer(base_url, username, password, container_name)

    @staticmethod
    def register_aac_container(container_name, base_url, username, password):
        DockerConfiguration.runtime_container = DockerContainer(base_url, username, password, container_name)

    @staticmethod
    def restart_runtime_service_container():
        DockerConfiguration.docker.restart_container(DockerConfiguration.runtime_container)

    @staticmethod
    def restart_webseal_container(instance):
        DockerConfiguration.docker.restart_container(DockerConfiguration.webseal_containers[instance])
