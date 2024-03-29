"""
@copyright: IBM
"""

from .federation.federations import Federations, Federations9040, Federations10000
from .federation.pointofcontact import PointOfContact
from .federation.accesspolicy import AccessPolicy
from .federation.attributesources import AttributeSources
from .federation.securitytokenservice import SecurityTokenService
from .federation.aliasservice import AliasService

class Federation(object):
    '''
    Object is used to manage the Federations endpoints of a Verify Access deployment.

    :var federations: Create and manage :ref:`Federation<Federations>` and Partners.
    :var attribute_sources: Manage :ref:`attributes<AttributeSources>` added to identities in federation flows.
    :var alias_service: Manage user :ref:`aliases<AliasService>` for federated identity sources.
    :var sts: Create and manage :ref:`Security Token Service<SecurityTokenService>` chains.
    :var poc: Create and manage :ref:`Point of Contact<PointOfContact>` profiles.
    :var access_policy: Create and manage :ref:`Access Policy<AccessPolicy>` rules.
    '''

class Federation9020(object):

    def __init__(self, base_url, username, password):
        super(Federation9020, self).__init__()
        self.federations = Federations(base_url, username, password)
        self.attribute_sources = AttributeSources(base_url, username, password)
        self.sts = SecurityTokenService(base_url, username, password)


class Federation9021(Federation9020):

    def __init__(self, base_url, username, password):
        super(Federation9021, self).__init__(base_url, username, password)

class Federation9030(Federation9021):

    def __init__(self, base_url, username, password):
        super(Federation9030, self).__init__(base_url, username, password)

class Federation9040(Federation9030):

    def __init__(self, base_url, username, password):
        super(Federation9040, self).__init__(base_url, username, password)
        self.federations = Federations9040(base_url, username, password)
        self.poc = PointOfContact(base_url, username, password)
        self.access_policy = AccessPolicy(base_url, username, password)
        self.alias_service = AliasService(base_url, username, password)


class Federation9050(Federation9040):

    def __init__(self, base_url, username, password):
        super(Federation9050, self).__init__(base_url, username, password)


class Federation9060(Federation9050):

    def __init__(self, base_url, username, password):
        super(Federation9060, self).__init__(base_url, username, password)


class Federation9070(Federation9060):

    def __init__(self, base_url, username, password):
        super(Federation9070, self).__init__(base_url, username, password)


class Federation9071(Federation9070):

    def __init__(self, base_url, username, password):
        super(Federation9071, self).__init__(base_url, username, password)


class Federation9080(Federation9071):

    def __init__(self, base_url, username, password):
        super(Federation9080, self).__init__(base_url, username, password)


class Federation10000(Federation9080):

    def __init__(self, base_url, username, password):
        super(Federation10000, self).__init__(base_url, username, password)
        self.federations = Federations10000(base_url, username, password)


class Federation10010(Federation10000):

    def __init__(self, base_url, username, password):
        super(Federation10010, self).__init__(base_url, username, password)
 

class Federation10020(Federation10010):

    def __init__(self, base_url, username, password):
        super(Federation10020, self).__init__(base_url, username, password)


class Federation10030(Federation10020):

    def __init__(self, base_url, username, password):
        super(Federation10030, self).__init__(base_url, username, password)


class Federation10031(Federation10030):

    def __init__(self, base_url, username, password):
        super(Federation10031, self).__init__(base_url, username, password)


class Federation10040(Federation10031):

    def __init__(self, base_url, username, password):
        super(Federation10040, self).__init__(base_url, username, password)


class Federation10050(Federation10040):

    def __init__(self, base_url, username, password):
        super(Federation10050, self).__init__(base_url, username, password)

class Federation10060(Federation10050):

    def __init__(self, base_url, username, password):
            super(Federation10060, self).__init__(base_url, username, password)
