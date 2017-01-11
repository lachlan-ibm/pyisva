"""
@copyright: IBM
"""

import logging

from pyisam.util.restclient import RestClient
import pyisam.util.common as Utils


PDADMIN = "/isam/pdadmin"


logger = logging.getLogger(__name__)


class PolicyAdmin(RestClient):

    def __init__(self, base_url, username, password):
        super(PolicyAdmin, self).__init__(base_url, username, password)

    def do_commands(self, admin_id, admin_pwd, commands):
        #logger.enter()
        result = None

        data = {}
        Utils.add_value_string(data, "admin_id", admin_id)
        Utils.add_value_string(data, "admin_pwd", admin_pwd)
        Utils.add_value(data, "commands", commands)

        status_code, content = self.http_post_json(PDADMIN, data)

        result = (status_code == 200, status_code, content)

        #logger.exit(result)
        return result
