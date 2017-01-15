"""
@copyright: IBM
"""

import logging

from pyisam.util.model import DataObject
from pyisam.util.restclient import RESTClient


PDADMIN = "/isam/pdadmin"

logger = logging.getLogger(__name__)


class PolicyAdmin(object):

    def __init__(self, base_url, username, password):
        super(PolicyAdmin, self).__init__()
        self.client = RESTClient(base_url, username, password)

    def execute(self, admin_id, admin_pwd, commands):
        data = DataObject()
        data.add_value_string("admin_id", admin_id)
        data.add_value_string("admin_pwd", admin_pwd)
        data.add_value("commands", commands)

        response = self.client.post_json(PDADMIN, data.data)
        response.success = response.status_code == 200

        return response
