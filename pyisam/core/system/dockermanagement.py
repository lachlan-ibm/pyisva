""""
@copyright: IBM
"""

import logging
import docker

from pyisam.util.restclient import RESTClient

PUBLISH_URL = "/docker/publish"
CLI_URL = "/core/cli"

logger = logging.getLogger(__name__)


class DockerManagement(object):

    def __init__(self, base_url, username, password):
        super(DockerManagement, self).__init__()
        self.client = RESTClient(base_url, username, password)
        self.docker_client = docker.from_env()

    def publish_changes(self):
        response = self.client.put_json(PUBLISH_URL)
        if response.status_code == 201:
            logger.debug("New snapshot published: {0}".format(response.json.get("filename")))
        else:
            logger.error("An error occurred while publishing the snapshot")
            response.success = False

        return response

    def restart_container(self, container):
        logger.info("Restarting container {0}".format(container.container_name()))

        container = self.docker_client.containers.get(container.container_name())
        container.restart()

    def check_container_state(self, container):
        docker_container = self.docker_client.containers.get(container.container_name())
        if docker_container.status == "running":
            return True
        else:
            docker_container.start()

    def reload_all(self, container):
        if self.check_container_state(container):
            container.rest_client().post_json(CLI_URL, self.get_json(["reload", "all"]))

    def reload_policy(self, container):
        if self.check_container_state(container):
            container.rest_client().post_json(CLI_URL, self.get_json(["reload", "policy"]))

    def reload_runtime(self, container):
        if self.check_container_state(container):
            container.rest_client().post_json(CLI_URL, self.get_json(["reload", "runtime"]))

    def get_json(self, command):
        return {
            "command": command,
            "input": ""
        }