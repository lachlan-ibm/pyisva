""""
@copyright: IBM
"""

import logging

from pyisam.util.restclient import RestClient
import pyisam.util.common as Utils


ADMIN_CONFIG = "/core/admin_cfg"

logger = logging.getLogger(__name__)


class AdminSettings(RestClient):

    def __init__(self, base_url, username, password):
        super(AdminSettings, self).__init__(base_url, username, password)

    def get(self):
        #logger.enter()

        status_code, content = self.http_get_json(ADMIN_CONFIG)

        result = (status_code == 200, status_code, content)

        #logger.exit(result)
        return result

    def update(
            self, old_password=None, new_password=None, confirm_password=None,
            min_heap_size=None, max_heap_size=None, session_timeout=None,
            http_port=None, https_port=None, min_threads=None, max_threads=None,
            max_pool_size=None, lmi_debugging_enabled=None,
            console_log_level=None, accept_client_certs=None,
            validate_client_cert_identity=None, exclude_csrf_checking=None,
            enable_ss_lv3=None):
        #logger.enter()

        data = {}
        Utils.add_value_string(data, "oldPassword", old_password)
        Utils.add_value_string(data, "newPassword", new_password)
        Utils.add_value_string(data, "confirmPassword", confirm_password)
        Utils.add_value_string(data, "consoleLogLevel", console_log_level)
        Utils.add_value_string(
            data, "excludeCsrfChecking", exclude_csrf_checking)
        Utils.add_value(data, "minHeapSize", min_heap_size)
        Utils.add_value(data, "maxHeapSize", max_heap_size)
        Utils.add_value(data, "sessionTimeout", session_timeout)
        Utils.add_value(data, "httpPort", http_port)
        Utils.add_value(data, "httpsPort", https_port)
        Utils.add_value(data, "minThreads", min_threads)
        Utils.add_value(data, "maxThreads", max_threads)
        Utils.add_value(data, "maxPoolSize", max_pool_size)
        Utils.add_value(data, "lmiDebuggingEnabled", lmi_debugging_enabled)
        Utils.add_value(data, "acceptClientCerts", accept_client_certs)
        Utils.add_value(
            data, "validateClientCertIdentity", validate_client_cert_identity)
        Utils.add_value(data, "enableSSLv3", enable_ss_lv3)

        status_code, content = self.http_put_json(ADMIN_CONFIG, data)

        result = (status_code == 200, status_code, content)

        #logger.exit(result)
        return result
