"""
@copyright: IBM
"""

#import logging

#from .access.accesscontrol import AccessControl


#logger = logging.getLogger(__name__)


class AccessControl9020(object):

    def __init__(self, base_url, username, password):
        #self.access_control = AccessControl(base_url, username, password)
        pass


class AccessControl9021(AccessControl9020):

    def __init__(self, base_url, username, password):
        super(AccessControl9021, self).__init__(base_url, username, password)
