"""
@copyright: IBM
"""

from .web.policyadmin import PolicyAdmin
from .web.reverseproxy import ReverseProxy
from .web.runtimecomponent import RuntimeComponent


class WebSettings9020(object):

    def __init__(self, base_url, username, password):
        self.policy_administration = PolicyAdmin(base_url, username, password)
        self.reverse_proxy = ReverseProxy(base_url, username, password)
        self.runtime_component = RuntimeComponent(base_url, username, password)


class WebSettings9021(WebSettings9020):

    def __init__(self, base_url, username, password):
        super(WebSettings9021, self).__init__(base_url, username, password)
