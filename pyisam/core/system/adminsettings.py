""""
@copyright: IBM
"""

import logging

from pyisam.util.model import DataObject
from pyisam.util.restclient import RESTClient


ADMIN_CONFIG = "/core/admin_cfg"

logger = logging.getLogger(__name__)


class AdminSettings(object):

    def __init__(self, base_url, username, password):
        super(AdminSettings, self).__init__()
        self.client = RESTClient(base_url, username, password)

    def get(self):
        response = self.client.get_json(ADMIN_CONFIG)
        response.success = response.status_code == 200

        return response

    def update(
            self, old_password=None, new_password=None, confirm_password=None,
            min_heap_size=None, max_heap_size=None, session_timeout=None,
            http_port=None, https_port=None, min_threads=None, max_threads=None,
            max_pool_size=None, lmi_debugging_enabled=None,
            console_log_level=None, accept_client_certs=None,
            validate_client_cert_identity=None, exclude_csrf_checking=None,
            enable_ss_lv3=None):
        data = DataObject()
        data.add_value_string("oldPassword", old_password)
        data.add_value_string("newPassword", new_password)
        data.add_value_string("confirmPassword", confirm_password)
        data.add_value_string("consoleLogLevel", console_log_level)
        data.add_value_string("excludeCsrfChecking", exclude_csrf_checking)
        data.add_value("minHeapSize", min_heap_size)
        data.add_value("maxHeapSize", max_heap_size)
        data.add_value("sessionTimeout", session_timeout)
        data.add_value("httpPort", http_port)
        data.add_value("httpsPort", https_port)
        data.add_value("minThreads", min_threads)
        data.add_value("maxThreads", max_threads)
        data.add_value("maxPoolSize", max_pool_size)
        data.add_value("lmiDebuggingEnabled", lmi_debugging_enabled)
        data.add_value("acceptClientCerts", accept_client_certs)
        data.add_value(
            "validateClientCertIdentity", validate_client_cert_identity)
        data.add_value("enableSSLv3", enable_ss_lv3)
        
        response = self.client.put_json(ADMIN_CONFIG, data.data)
        response.success = response.status_code == 200

        return response
