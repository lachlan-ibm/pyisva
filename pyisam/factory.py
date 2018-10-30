"""
@copyright: IBM
"""

import importlib

from pyisam.util.restclient import RESTClient


DEVELOPMENT_VERSION = "IBM Security Access Manager Development"
VERSIONS = {
    DEVELOPMENT_VERSION: "9060",
    "IBM Security Access Manager 9.0.6.0_b2": "9060",
    "IBM Security Access Manager 9.0.6.0_b1": "9060",
    "IBM Security Access Manager 9.0.6.0": "9060",
    "IBM Security Access Manager 9.0.5.0": "9050",
    "IBM Security Access Manager 9.0.4.0": "9040",
    "IBM Security Access Manager 9.0.3.0": "9030",
    "IBM Security Access Manager 9.0.2.1": "9021",
    "IBM Security Access Manager 9.0.2.0": "9020"
}


class AuthenticationError(Exception):
    pass


class Factory(object):

    def __init__(self, base_url, username, password):
        super(Factory, self).__init__()
        self._base_url = base_url
        self._username = username
        self._password = password
        self._version = None
        self._deployment_model = "Appliance"

        self._discover_version_and_deployment()
        self._get_version()

    def get_federation(self):
        class_name = "Federation" + self._get_version()
        module_name = "pyisam.core.federationsettings"
        return self._class_loader(module_name, class_name)

    def get_access_control(self):
        class_name = "AccessControl" + self._get_version()
        module_name = "pyisam.core.accesscontrol"
        return self._class_loader(module_name, class_name)

    def get_analysis_diagnostics(self):
        class_name = "AnalysisDiagnostics" + self._get_version()
        module_name = "pyisam.core.analysisdiagnostics"
        return self._class_loader(module_name, class_name)

    def get_system_settings(self):
        class_name = "SystemSettings" + self._get_version()
        module_name = "pyisam.core.systemsettings"
        return self._class_loader(module_name, class_name)

    def get_version(self):
        return self._version

    def get_web_settings(self):
        class_name = "WebSettings" + self._get_version()
        module_name = "pyisam.core.websettings"
        return self._class_loader(module_name, class_name)

    def get_deployment_utility(self):
        class_name = "WebSettings" + self._get_version()
        module_name = "pyisam.core.websettings"
        return self._class_loader(module_name, class_name)

    def set_password(self, password):
        self._password = password

    def _class_loader(self, module_name, class_name):
        Klass = getattr(importlib.import_module(module_name), class_name)
        return Klass(self._base_url, self._username, self._password)

    def is_docker(self):
        return self._deployment_model == "Docker"

    def get_deployment_model(self):
        return self._deployment_model

    def _discover_version_and_deployment(self):
        client = RESTClient(self._base_url, self._username, self._password)

        response = client.get_json("/core/sys/versions")
        if response.status_code == 200:
            self._version          = "{0} {1}".format(response.json.get("product_description"), response.json.get("firmware_version"))
            self._deployment_model = response.json.get("deployment_model")
        elif response.status_code == 403:
            raise AuthenticationError("Authentication failed.")
        else:
            response = client.get_json("/firmware_settings")
            if response.status_code == 200:
                for entry in response.json:
                    if entry.get("active", False):
                        if entry.get("name", "").endswith("_nonproduction_dev"):
                            self._version = DEVELOPMENT_VERSION
                        else:
                            self._version = entry.get("firmware_version")
            elif response.status_code == 403:
                raise AuthenticationError("Authentication failed.")

        if not self._version:
            raise Exception("Failed to retrieve the ISAM firmware version.")

    def _get_version(self):
        if self._version in VERSIONS:
            return VERSIONS.get(self._version)
        else:
            raise Exception(self._version + " is not supported.")
