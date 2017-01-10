"""
@copyright: IBM
"""


from pyisam.core.accesscontrol import AccessControl9020, AccessControl9021


class AccessAuxiliary9020(object):

    def __init__(self, base_url, username, password):
        pass


class AccessAuxiliary9021(AccessAuxiliary9020):

    def __init__(self, base_url, username, password):
        super(AccessAuxiliary9021, self).__init__(base_url, username, password)
        pass
