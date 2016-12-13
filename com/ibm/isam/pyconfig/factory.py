"""
@copyright: IBM
"""

import importlib
import logging

from com.ibm.isam.util.restclient import RestClient


VERSIONS = {
    "IBM Security Access Manager 9.0.2.0": "9020"
}


class AuthenticationError(Exception):
    pass


class Factory(object):

    def __init__(self, base_url, username, password, log_level=logging.NOTSET):
        self._base_url = base_url
        self._username = username
        self._password = password
        self._log_level = log_level
        self._version = None

        self._discover_version()
        self._get_version()

    def get_access_control(self):
        class_name = "AccessControl" + self._get_version()
        module_name = "com.ibm.isam.pyconfig.access.accesscontrol"
        return self._class_loader(module_name, class_name)

    def get_first_steps(self):
        class_name = "FirstSteps" + self._get_version()
        module_name = "com.ibm.isam.pyconfig.firststeps.firststeps"
        return self._class_loader(module_name, class_name)

    def get_system_settings(self):
        class_name = "SystemSettings" + self._get_version()
        module_name = "com.ibm.isam.pyconfig.system.systemsettings"
        return self._class_loader(module_name, class_name)

    def get_web_settings(self):
        class_name = "WebSettings" + self._get_version()
        module_name = "com.ibm.isam.pyconfig.web.websettings"
        return self._class_loader(module_name, class_name)

    def set_password(self, password):
        self._password = password

    def _class_loader(self, module_name, class_name):
        Klass = getattr(importlib.import_module(module_name), class_name)
        return Klass(
            self._base_url, self._username, self._password, self._log_level)

    def _discover_version(self):
        client = RestClient(
            self._base_url, self._username, self._password, self._log_level)
        status_code, content = client.http_get_json("/firmware_settings")

        if status_code == 200:
            for entry in content:
                if entry.get("active", False):
                    self._version = entry.get("firmware_version")
        elif status_code == 403:
            raise AuthenticationError("Authentication failed.")

        if not self._version:
            raise Exception("Failed to retrieve the ISAM firmware version.")

    def _get_version(self):
        if self._version in VERSIONS:
            return VERSIONS.get(self._version)
        else:
            raise Exception(self._version + " is not supported.")
