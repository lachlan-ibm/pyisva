"""
@copyright: IBM
"""

from .web.dscadmin import DSCAdmin
from .web.policyadmin import PolicyAdmin
from .web.reverseproxy import ReverseProxy, ReverseProxy9040
from .web.runtimecomponent import RuntimeComponent


class WebSettings9020(object):

    def __init__(self, base_url, username, password):
        super(WebSettings9020, self).__init__()
        self.dsc_admin = DSCAdmin(base_url, username, password)
        self.policy_administration = PolicyAdmin(base_url, username, password)
        self.reverse_proxy = ReverseProxy(base_url, username, password)
        self.runtime_component = RuntimeComponent(base_url, username, password)


class WebSettings9021(WebSettings9020):

    def __init__(self, base_url, username, password):
        super(WebSettings9021, self).__init__(base_url, username, password)


class WebSettings9030(WebSettings9021):

    def __init__(self, base_url, username, password):
        super(WebSettings9030, self).__init__(base_url, username, password)


class WebSettings9040(WebSettings9030):

    def __init__(self, base_url, username, password):
        super(WebSettings9040, self).__init__(base_url, username, password)
        self.reverse_proxy = ReverseProxy9040(base_url, username, password)


class WebSettings9050(WebSettings9040):

    def __init__(self, base_url, username, password):
            super(WebSettings9050, self).__init__(base_url, username, password)


class WebSettings9060(WebSettings9050):

    def __init__(self, base_url, username, password):
            super(WebSettings9060, self).__init__(base_url, username, password)


class WebSettings9070(WebSettings9060):

    def __init__(self, base_url, username, password):
            super(WebSettings9070, self).__init__(base_url, username, password)


class WebSettings9071(WebSettings9070):

    def __init__(self, base_url, username, password):
            super(WebSettings9071, self).__init__(base_url, username, password)


class WebSettings9080(WebSettings9071):

    def __init__(self, base_url, username, password):
            super(WebSettings9080, self).__init__(base_url, username, password)


class WebSettings10000(WebSettings9080):

    def __init__(self, base_url, username, password):
            super(WebSettings10000, self).__init__(base_url, username, password)


class WebSettings10010(WebSettings10000):

    def __init__(self, base_url, username, password):
            super(WebSettings10010, self).__init__(base_url, username, password)


class WebSettings10020(WebSettings10010):

    def __init__(self, base_url, username, password):
            super(WebSettings10020, self).__init__(base_url, username, password)
