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
from .system.interfaces import Interfaces, Interfaces10000
from .system.staticroutes import StaticRoutes, StaticRoutes10000
from .system.licensing import Licensing
from .system.restartshutdown import RestartShutdown
from .system.sslcertificates import SSLCertificates
from .system.clicommands import CLICommands
from .system.runtimedb import RuntimeDb
from .system.configdb import ConfigDb
from .system.docker import Docker
from .system.fixpacks import Fixpacks
from .system.sysaccount import SysAccount
from .system.managementauthroization import ManagementAuthorization


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
        self.static_routes = StaticRoutes(base_url, username, password)
        self.fixpacks = Fixpacks(base_url, username, password)
        self.licensing = Licensing(base_url, username, password)
        self.restartshutdown = RestartShutdown(base_url, username, password)
        self.ssl_certificates = SSLCertificates(base_url, username, password)
        self.cli_commands = CLICommands(base_url, username, password)
        self.sysaccount = SysAccount(base_url, username, password)
        self.runtime_db = RuntimeDb(base_url, username, password)
        self.config_db = ConfigDb(base_url, username, password)


class SystemSettings9021(SystemSettings9020):

    def __init__(self, base_url, username, password):
        super(SystemSettings9021, self).__init__(base_url, username, password)


class SystemSettings9030(SystemSettings9021):

    def __init__(self, base_url, username, password):
        super(SystemSettings9030, self).__init__(base_url, username, password)


class SystemSettings9040(SystemSettings9030):

    def __init__(self, base_url, username, password):
        super(SystemSettings9040, self).__init__(base_url, username, password)
        
        self.docker = Docker(base_url, username, password)


class SystemSettings9050(SystemSettings9040):

    def __init__(self, base_url, username, password):
        super(SystemSettings9050, self).__init__(base_url, username, password)


class SystemSettings9060(SystemSettings9050):

    def __init__(self, base_url, username, password):
        super(SystemSettings9060, self).__init__(base_url, username, password)


class SystemSettings9070(SystemSettings9060):

    def __init__(self, base_url, username, password):
        super(SystemSettings9070, self).__init__(base_url, username, password)


class SystemSettings9071(SystemSettings9070):

    def __init__(self, base_url, username, password):
        super(SystemSettings9071, self).__init__(base_url, username, password)


class SystemSettings9080(SystemSettings9071):

    def __init__(self, base_url, username, password):
        super(SystemSettings9080, self).__init__(base_url, username, password)


class SystemSettings10000(SystemSettings9080):

    def __init__(self, base_url, username, password):
        super(SystemSettings10000, self).__init__(base_url, username, password)
        self.static_routes = StaticRoutes10000(base_url, username, password)
        self.interfaces = Interfaces10000(base_url, username, password)
        self.managementauthrization = ManagementAuthorisaton(url, username, password)
