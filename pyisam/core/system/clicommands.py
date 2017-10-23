""""
@copyright: IBM
"""

import logging

from pyisam.util.model import DataObject
from pyisam.util.restclient import RESTClient


CLI_COMMAND = "/core/cli"

logger = logging.getLogger(__name__)


class CLICommands(object):

    def __init__(self, base_url, username, password):
        super(CLICommands, self).__init__()
        self.client = RESTClient(base_url, username, password)

    def run(
            self, command=None,input_array=None):
        data = DataObject()
        data.add_value_string("command", command)
        data.add_value("input", input_array)
        
        response = self.client.post_json(CLI_COMMAND, data.data)
        response.success = response.status_code == 200

        return response
