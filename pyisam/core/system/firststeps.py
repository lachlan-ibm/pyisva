"""
@copyright: IBM
"""

import logging

from pyisam.util.common import add_value, add_value_not_empty, add_value_string
from pyisam.util.restclient import RestClient


SETUP_COMPLETE = "/setup_complete"
SERVICE_AGREEMENTS_ACCEPTED = "/setup_service_agreements/accepted"


logger = logging.getLogger(__name__)


class FirstSteps(RestClient):

    def __init__(self, base_url, username, password):
        super(FirstSteps, self).__init__(base_url, username, password)

    # First Steps Setup

    def get_setup_status(self):
        #logger.enter()
        result = None

        statusCode, content = self.http_get_json(SETUP_COMPLETE)

        result = (statusCode == 200, statusCode, content)

        #logger.exit(result)
        return result

    def set_setup_complete(self):
        #logger.enter()
        result = None

        statusCode, content = self.http_put_json(SETUP_COMPLETE)

        result = (statusCode == 200, statusCode, content)

        #logger.exit(result)
        return result

    # Service Agreements

    def get_sla_status(self):
        #logger.enter()
        result = None

        statusCode, content = self.http_get_json(SERVICE_AGREEMENTS_ACCEPTED)

        result = (statusCode == 200, statusCode, content)

        #logger.exit(result)
        return result

    def set_sla_status(self, accept=True):
        #logger.enter()
        result = None

        data = {}
        add_value(data, "accepted", accept)

        statusCode, content = self.http_put_json(
            SERVICE_AGREEMENTS_ACCEPTED, data)

        result = (statusCode == 200, statusCode, content)

        #logger.exit(result)
        return result
