"""
@copyright: IBM
"""

from .federation.federations import Federations, Federations9040
from .federation.pointofcontact import PointOfContact
from .federation.accesspolicy import AccessPolicy
from .federation.attributesources import AttributeSources

class Federation9020(object):

    def __init__(self, base_url, username, password):
        super(Federation9020, self).__init__()
        self.federations = Federations(base_url, username, password)
        self.attribute_sources = AttributeSources(base_url, username, password)

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
        self.poc= PointOfContact(base_url, username, password)
        self.access_policy = AccessPolicy(base_url, username, password)


class Federation9050(Federation9040):

    def __init__(self, base_url, username, password):
            super(Federation9050, self).__init__(base_url, username, password)


class Federation9060(Federation9050):

    def __init__(self, base_url, username, password):
            super(Federation9060, self).__init__(base_url, username, password)


class Federation9070(Federation9060):

    def __init__(self, base_url, username, password):
            super(Federation9070, self).__init__(base_url, username, password)


class Federation9080(Federation9070):

    def __init__(self, base_url, username, password):
            super(Federation9080, self).__init__(base_url, username, password)
