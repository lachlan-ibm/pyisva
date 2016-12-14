"""
@copyright: IBM
"""

import logging

from com.ibm.isam.util.logger import Logger
from com.ibm.isam.util.restclient import RestClient
import com.ibm.isam.util.utils as Utils


SETUP_COMPLETE = "/setup_complete"
SERVICE_AGREEMENTS_ACCEPTED = "/setup_service_agreements/accepted"


class FirstSteps(RestClient):

    logger = Logger("FirstSteps")

    def __init__(self, base_url, username, password, log_level=logging.NOTSET):
        super(FirstSteps, self).__init__(
            base_url, username, password, log_level)
        FirstSteps.logger.set_level(log_level)

    #
    # First Steps Setup
    #

    def get_setup_status(self):
        method_name = "get_setup_status()"
        FirstSteps.logger.enter_method(method_name)
        result = None

        statusCode, content = self.http_get_json(SETUP_COMPLETE)

        result = (statusCode == 200, statusCode, content)

        FirstSteps.logger.exit_method(method_name, result)
        return result

    def set_setup_complete(self):
        method_name = "set_setup_complete()"
        FirstSteps.logger.enter_method(method_name)
        result = None

        statusCode, content = self.http_put_json(SETUP_COMPLETE)

        result = (statusCode == 200, statusCode, content)

        FirstSteps.logger.exit_method(method_name, result)
        return result

    #
    # Service Agreements
    #

    def get_sla_status(self):
        method_name = "get_sla_status()"
        FirstSteps.logger.enter_method(method_name)
        result = None

        statusCode, content = self.http_get_json(SERVICE_AGREEMENTS_ACCEPTED)

        result = (statusCode == 200, statusCode, content)

        FirstSteps.logger.exit_method(method_name, result)
        return result

    def set_sla_status(self, accept=True):
        method_name = "set_sla_status(accept)"
        FirstSteps.logger.enter_method(method_name)
        result = None

        data = {}
        Utils.add_value(data, "accepted", accept)

        statusCode, content = self.http_put_json(
            SERVICE_AGREEMENTS_ACCEPTED, data)

        result = (statusCode == 200, statusCode, content)

        FirstSteps.logger.exit_method(method_name, result)
        return result


class FirstSteps9020(FirstSteps):

    logger = Logger("FirstSteps9020")

    def __init__(self, base_url, username, password, log_level=logging.NOTSET):
        super(FirstSteps9020, self).__init__(
            base_url, username, password, log_level)
        FirstSteps9020.logger.set_level(log_level)


class FirstSteps9021(FirstSteps9020):

    logger = Logger("FirstSteps9021")

    def __init__(self, base_url, username, password, log_level=logging.NOTSET):
        super(FirstSteps9021, self).__init__(
            base_url, username, password, log_level)
        FirstSteps9021.logger.set_level(log_level)
