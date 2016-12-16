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


class SystemSettings(RestClient):

    logger = Logger("SystemSettings")

    def __init__(self, base_url, username, password, log_level=logging.NOTSET):
        super(SystemSettings, self).__init__(
            base_url, username, password, log_level)
        SystemSettings.logger.set_level(log_level)

    #
    # Administrator Settings
    #

    def get_administrator_settings(self):
        SystemSettings.logger.enter()
        result = None

        status_code, content = self.http_get_json(ADMIN_CONFIG)

        result = (status_code == 200, status_code, content)

        SystemSettings.logger.exit(result)
        return result

    def update_administrator_settings(
            self, old_password=None, new_password=None, confirm_password=None,
            min_heap_size=None, max_heap_size=None, session_timeout=None,
            http_port=None, https_port=None, min_threads=None, max_threads=None,
            max_pool_size=None, lmi_debugging_enabled=None,
            console_log_level=None, accept_client_certs=None,
            validate_client_cert_identity=None, exclude_csrf_checking=None,
            enable_ss_lv3=None):
        SystemSettings.logger.enter()
        result = None

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

        SystemSettings.logger.exit(result)
        return result

    def update_administrator_password(self, password):
        SystemSettings.logger.enter()
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
                SystemSettings.logger.error(
                    "An invalid session timeout was retrieved.")
                result = (False, status_code, content)
        else:
            result = (success, status_code, content)

        SystemSettings.logger.exit(result)
        return result

    #
    # Advanced Tuning Parameters
    #

    def create_advanced_tuning_parameter(
            self, key=None, value=None, comment=None):
        SystemSettings.logger.enter()
        result = None

        data = {}
        Utils.add_value_string(data, "key", key)
        Utils.add_value_string(data, "value", value)
        Utils.add_value_string(data, "comment", comment)
        Utils.add_value(data, "_isNew", True)

        status_code, content = self.http_post_json(ADVANCED_PARAMETERS, data)

        result = (status_code == 201, status_code, content)

        SystemSettings.logger.exit(result)
        return result

    def get_advanced_tuning_parameters(self):
        SystemSettings.logger.enter()
        result = None

        status_code, content = self.http_get_json(ADVANCED_PARAMETERS)

        if status_code == 200:
            result = (True, status_code, content.get("tuningParameters", []))
        else:
            result = (False, status_code, content)

        SystemSettings.logger.exit(result)
        return result

    def get_advanced_tuning_parameter(self, key):
        SystemSettings.logger.enter()
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

        SystemSettings.logger.exit(result)
        return result

    #
    # Date/Time
    #

    def update_date_time(
            self, enable_ntp=True, ntp_servers=None, time_zone=None,
            date_time="0000-00-00 00:00:00"):
        SystemSettings.logger.enter()
        result = None

        data = {}
        Utils.add_value_string(data, "dateTime", date_time)
        Utils.add_value_string(data, "ntpServers", ntp_servers)
        Utils.add_value_string(data, "timeZone", time_zone)
        Utils.add_value(data, "enableNtp", enable_ntp)

        status_code, content = self.http_put_json(TIME_CONFIG, data)

        result = (status_code == 200, status_code, content)

        SystemSettings.logger.exit(result)
        return result

    #
    # Restart or Shutdown
    #

    def get_lmi_status(self):
        SystemSettings.logger.enter()
        result = None

        status_code, content = self.http_get_json(LMI)

        result = (status_code == 200, status_code, content)

        SystemSettings.logger.exit(result)
        return result

    def restart_lmi(self):
        SystemSettings.logger.enter()
        result = None

        last_start_time = -1

        success, status_code, content = self.get_lmi_status()

        if success:
            last_start_time = content[0].get("start_time", -1)

        if last_start_time > 0:
            status_code, content = self.http_post_json(LMI_RESTART)

            if status_code == 200 and content.get("restart", False) == True:
                SystemSettings.logger.info("Waiting for LMI to restart...")
                self._wait_for_lmi(last_start_time)
                result = (True, status_code, content)
            else:
                result = (False, status_code, content)
        else:
            SystemSettings.logger.error(
                "An invalid start time was retrieved: %i", last_start_time)
            result = (False, status_code, content)

        SystemSettings.logger.exit(result)
        return result

    def _wait_for_lmi(self, last_start_time, sleep_interval=3):
        SystemSettings.logger.enter()

        if last_start_time > 0:
            restart_time = last_start_time

            while (restart_time <= 0 or restart_time == last_start_time):
                SystemSettings.logger.debug(
                    "last_start_time: %i, restart_time: %i", last_start_time,
                    restart_time)
                time.sleep(sleep_interval)

                try:
                    success, status_code, content = self.get_lmi_status()

                    if success:
                        restart_time = content[0].get("start_time", -1)
                except:
                    restart_time = -1

            time.sleep(sleep_interval)
        else:
            SystemSettings.logger.error("Invalid last start time: %i", last_start_time)

        SystemSettings.logger.exit()
