"""
@copyright: IBM
"""


from pyisam.core.systemsettings import SystemSettings9020, SystemSettings9021
from pyisam.core.websettings import WebSettings9020, WebSettings9021


class WebAuxiliary9020(object):

    def __init__(self, base_url, username, password):
        self._system_settings = SystemSettings9020(base_url, username, password)
        self._web_settings = WebSettings9020(base_url, username, password)

    def example(self):
        success, status, content = self._system_settings.first_steps\
            .get_setup_status()
        if success and content.get("configured", False):
            self._web_settings.reverse_proxy.restart_instance("default")


class WebAuxiliary9021(WebAuxiliary9020):

    def __init__(self, base_url, username, password):
        super(WebAuxiliary9021, self).__init__(base_url, username, password)
        self._web_settings = WebSettings9021(base_url, username, password)
