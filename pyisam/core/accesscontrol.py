"""
@copyright: IBM
"""

from .access.accesscontrol import AccessControl
from .access.accesscontrol import AccessControl9030 as AC9030
from .access.advancedconfig import AdvancedConfig
from .access.apiprotection import APIProtection, APIProtection9040
from .access.attributes import Attributes
from .access.authentication import Authentication, Authentication9021
from .access.filedownloads import FileDownloads
from .access.mmfaconfig import MMFAConfig, MMFAConfig9021
from .access.pushnotification import PushNotification, PushNotification9021
from .access.riskprofiles import RiskProfiles
from .access.runtimeparameters import RuntimeParameters
from .access.scimconfig import SCIMConfig, SCIMConfig9050
from .access.serverconnections import ServerConnections, ServerConnections9050
from .access.templatefiles import TemplateFiles
from .access.userregistry import UserRegistry
from .access.mappingrules import MappingRules
from .access.fido2config import FIDO2Config


class AccessControl9020(object):

    def __init__(self, base_url, username, password):
        super(AccessControl9020, self).__init__()
        self.access_control = AccessControl(base_url, username, password)
        self.advanced_config = AdvancedConfig(base_url, username, password)
        self.api_protection = APIProtection(base_url, username, password)
        self.attributes = Attributes(base_url, username, password)
        self.authentication = Authentication(base_url, username, password)
        self.file_downloads = FileDownloads(base_url, username, password)
        self.mmfa_config = MMFAConfig(base_url, username, password)
        self.push_notification = PushNotification(base_url, username, password)
        self.risk_profiles = RiskProfiles(base_url, username, password)
        self.runtime_parameters = RuntimeParameters(
            base_url, username, password)
        self.scim_config = SCIMConfig(base_url, username, password)
        self.server_connections = ServerConnections(
            base_url, username, password)
        self.template_files = TemplateFiles(base_url, username, password)
        self.user_registry = UserRegistry(base_url, username, password)
        self.mapping_rules = MappingRules(base_url, username, password)


class AccessControl9021(AccessControl9020):

    def __init__(self, base_url, username, password):
        super(AccessControl9021, self).__init__(base_url, username, password)
        self.mmfa_config = MMFAConfig9021(base_url, username, password)
        self.push_notification = PushNotification9021(base_url, username, password)
        self.authentication = Authentication9021(base_url, username, password)


class AccessControl9030(AccessControl9021):

    def __init__(self, base_url, username, password):
        super(AccessControl9030, self).__init__(base_url, username, password)
        self.access_control = AC9030(base_url, username, password)


class AccessControl9040(AccessControl9030):

    def __init__(self, base_url, username, password):
        super(AccessControl9040, self).__init__(base_url, username, password)
        self.api_protection = APIProtection9040(base_url, username, password)

class AccessControl9050(AccessControl9040):

    def __init__(self, base_url, username, password):
        super(AccessControl9050, self).__init__(base_url, username, password)
        self.server_connections = ServerConnections9050(base_url, username, password)
        self.scim_config = SCIMConfig9050(base_url, username, password)

class AccessControl9060(AccessControl9050):

    def __init__(self, base_url, username, password):
              super(AccessControl9060, self).__init__(base_url, username, password)


class AccessControl9070(AccessControl9060):

    def __init__(self, base_url, username, password):
              super(AccessControl9070, self).__init__(base_url, username, password)
              self.fido2_config = FIDO2Config(base_url, username, password)


class AccessControl9071(AccessControl9070):

    def __init__(self, base_url, username, password):
              super(AccessControl9071, self).__init__(base_url, username, password)
              self.fido2_config = FIDO2Config(base_url, username, password)


class AccessControl9080(AccessControl9071):

    def __init__(self, base_url, username, password):
              super(AccessControl9080, self).__init__(base_url, username, password)


class AccessControl10000(AccessControl9080):

    def __init__(self, base_url, username, password):
              super(AccessControl10000, self).__init__(base_url, username, password)


class AccessControl10010(AccessControl10000):

    def __init__(self, base_url, username, password):
              super(AccessControl10010, self).__init__(base_url, username, password)


class AccessControl10020(AccessControl10010):

    def __init__(self, base_url, username, password):
              super(AccessControl10020, self).__init__(base_url, username, password)
