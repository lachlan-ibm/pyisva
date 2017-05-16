"""
@copyright: IBM
"""

from .system.adminsettings import AdminSettings
from .system.advancedtuning import AdvancedTuning
from .system.configuration import Configuration
from .system.datetime import DateTime
from .system.dns import DNS
from .system.filedownloads import FileDownloads
from .system.firststeps import FirstSteps
from .system.hostsfile import HostsFile
from .system.interfaces import Interfaces
from .system.licensing import Licensing
from .system.restartshutdown import RestartShutdown
from .system.sslcertificates import SSLCertificates


class SystemSettings9020(object):

    def __init__(self, base_url, username, password):
        super(SystemSettings9020, self).__init__()
        self.advanced_tuning = AdvancedTuning(base_url, username, password)
        self.admin_settings = AdminSettings(base_url, username, password)
        self.configuration = Configuration(base_url, username, password)
        self.date_time = DateTime(base_url, username, password)
        self.dns = DNS(base_url, username, password)
        self.file_downloads = FileDownloads(base_url, username, password)
        self.first_steps = FirstSteps(base_url, username, password)
        self.hosts_file = HostsFile(base_url, username, password)
        self.interfaces = Interfaces(base_url, username, password)
        self.licensing = Licensing(base_url, username, password)
        self.restartshutdown = RestartShutdown(base_url, username, password)
        self.ssl_certificates = SSLCertificates(base_url, username, password)


class SystemSettings9021(SystemSettings9020):

    def __init__(self, base_url, username, password):
        super(SystemSettings9021, self).__init__(base_url, username, password)


class SystemSettings9030(SystemSettings9021):

    def __init__(self, base_url, username, password):
        super(SystemSettings9030, self).__init__(base_url, username, password)
