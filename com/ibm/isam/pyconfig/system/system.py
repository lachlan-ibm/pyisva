""""
@copyright: IBM
"""

import logging
import time

from com.ibm.isam.util.logger import Logger
from com.ibm.isam.util.restclient import RestClient
import com.ibm.isam.util.utils as Utils


ADMIN_CONFIG = "/core/admin_cfg"
ADVANCED_PARAMETERS = "/core/adv_params"
LMI = "/lmi"
LMI_RESTART = "/restarts/restart_server"
TIME_CONFIG = "/core/time_cfg"


class _SystemSettings(RestClient):

    logger = Logger("SystemSettings")

    def __init__(self, base_url, username, password, log_level=logging.NOTSET):
        super(_SystemSettings, self).__init__(
            base_url, username, password, log_level)
        _SystemSettings.logger.set_level(log_level)

    #
    # Administrator Settings
    #

    def get_administrator_settings(self):
        method_name = "get_administrator_settings()"
        _SystemSettings.logger.enter_method(method_name)
        result = None

        status_code, content = self.http_get_json(ADMIN_CONFIG)

        result = (status_code == 200, status_code, content)

        _SystemSettings.logger.exit_method(method_name, result)
        return result

    def update_administrator_settings(
            self, old_password=None, new_password=None, confirm_password=None,
            min_heap_size=None, max_heap_size=None, session_timeout=None,
            http_port=None, https_port=None, min_threads=None, max_threads=None,
            max_pool_size=None, lmi_debugging_enabled=None,
            console_log_level=None, accept_client_certs=None,
            validate_client_cert_identity=None, exclude_csrf_checking=None,
            enable_ss_lv3=None):
        method_name = "update_administrator_settings()"
        _SystemSettings.logger.enter_method(method_name)
        result = None

        data = {}
        Utils.add_string_value(data, "oldPassword", old_password)
        Utils.add_string_value(data, "newPassword", new_password)
        Utils.add_string_value(data, "confirmPassword", confirm_password)
        Utils.add_string_value(data, "consoleLogLevel", console_log_level)
        Utils.add_string_value(data, "excludeCsrfChecking", exclude_csrf_checking)
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

        _SystemSettings.logger.exit_method(method_name, result)
        return result

    def update_administrator_password(self, password):
        method_name = "update_administrator_password()"
        _SystemSettings.logger.enter_method(method_name)
        result = None

        success, status_code, content = self.get_administrator_settings()

        if success:
            session_timeout = content.get("sessionTimeout", -1)

            if session_timeout > 0:
                result = self.update_administrator_settings(
                    session_timeout=session_timeout,
                    old_password=self._password, new_password=password,
                    confirm_password=password)
            else:
                _SystemSettings.logger.error(
                    method_name, "An invalid session timeout was retrieved.")
                result = (False, status_code, content)
        else:
            result = (success, status_code, content)

        _SystemSettings.logger.exit_method(method_name, result)
        return result

    #
    # Advanced Tuning Parameters
    #

    def create_advanced_tuning_parameter(
            self, key=None, value=None, comment=None):
        method_name = "create_advanced_tuning_parameter()"
        _SystemSettings.logger.enter_method(method_name)
        result = None

        data = {}
        Utils.add_string_value(data, "key", key)
        Utils.add_string_value(data, "value", value)
        Utils.add_string_value(data, "comment", comment)
        Utils.add_value(data, "_isNew", True)

        status_code, content = self.http_post_json(ADVANCED_PARAMETERS, data)

        result = (status_code == 201, status_code, content)

        _SystemSettings.logger.exit_method(method_name, result)
        return result

    def get_advanced_tuning_parameters(self):
        method_name = "get_advanced_tuning_parameters()"
        _SystemSettings.logger.enter_method(method_name)
        result = None

        status_code, content = self.http_get_json(ADVANCED_PARAMETERS)

        if status_code == 200:
            result = (True, status_code, content.get("tuningParameters", []))
        else:
            result = (False, status_code, content)

        _SystemSettings.logger.exit_method(method_name, result)
        return result

    def get_advanced_tuning_parameter(self, key):
        method_name = "get_advanced_tuning_parameter()"
        _SystemSettings.logger.enter_method(method_name)
        result = None

        success, status_code, content = self.get_advanced_tuning_parameters()

        if success:
            for entry in content:
                if entry.get("key", "") == key:
                    result = (success, status_code, entry)

            if not result:
                result = (False, 404, content)
        else:
            result = (success, status_code, content)

        _SystemSettings.logger.exit_method(method_name, result)
        return result

    #
    # Date/Time
    #

    def update_date_time(
            self, enable_ntp=True, ntp_servers=None, time_zone=None,
            date_time="0000-00-00 00:00:00"):
        method_name = "update_date_time()"
        _SystemSettings.logger.enter_method(method_name)
        result = None

        data = {}
        Utils.add_string_value(data, "dateTime", date_time)
        Utils.add_string_value(data, "ntpServers", ntp_servers)
        Utils.add_string_value(data, "timeZone", time_zone)
        Utils.add_value(data, "enableNtp", enable_ntp)

        status_code, content = self.http_put_json(TIME_CONFIG, data)

        result = (status_code == 200, status_code, content)

        _SystemSettings.logger.exit_method(method_name, result)
        return result

    #
    # Restart or Shutdown
    #

    def get_lmi_status(self):
        method_name = "get_lmi_status()"
        _SystemSettings.logger.enter_method(method_name)
        result = None

        status_code, content = self.http_get_json(LMI)

        result = (status_code == 200, status_code, content)

        _SystemSettings.logger.exit_method(method_name, result)
        return result

    def restart_lmi(self):
        method_name = "restart_lmi()"
        _SystemSettings.logger.enter_method(method_name)
        result = None

        last_start_time = -1

        success, status_code, content = self.get_lmi_status()

        if success:
            last_start_time = content[0].get("start_time", -1)

        if last_start_time > 0:
            status_code, content = self.http_post_json(LMI_RESTART)

            if status_code == 200 and content.get("restart", False) == True:
                _SystemSettings.logger.log(
                    method_name, "Waiting for LMI to restart...")
                self._wait_for_lmi(last_start_time)
                result = (True, status_code, content)
            else:
                result = (False, status_code, content)
        else:
            message = ("An invalid start time was retrieved: %s"
                       % last_start_time)
            _SystemSettings.logger.error(method_name, message)
            result = (False, status_code, content)

        _SystemSettings.logger.exit_method(method_name, result)
        return result

    def _wait_for_lmi(self, last_start_time, sleep_interval=3):
        method_name = "_wait_for_lmi()"
        _SystemSettings.logger.enter_method(method_name)

        if last_start_time > 0:
            restart_time = last_start_time

            while (restart_time <= 0 or restart_time == last_start_time):
                message = ("last_start_time: %s, restart_time: %s"
                           % (last_start_time, restart_time))
                _SystemSettings.logger.trace(method_name, message)
                time.sleep(sleep_interval)

                try:
                    success, status_code, content = self.get_lmi_status()

                    if success:
                        restart_time = content[0].get("start_time", -1)
                except:
                    restart_time = -1

            time.sleep(sleep_interval)
        else:
            message = "Invalid last start time: %s" % last_start_time
            _SystemSettings.logger.error(method_name, message)

        _SystemSettings.logger.exit_method(method_name)


class SystemSettings9020(_SystemSettings):

    logger = Logger("SystemSettings9020")

    def __init__(self, base_url, username, password, log_level=logging.NOTSET):
        super(SystemSettings9020, self).__init__(
            base_url, username, password, log_level)
        SystemSettings9020.logger.set_level(log_level)
