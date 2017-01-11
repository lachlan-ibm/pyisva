"""
@copyright: IBM
"""


from .system.firststeps import FirstSteps


class SystemSettings9020(object):

    def __init__(self, base_url, username, password):
        self.first_steps = FirstSteps(base_url, username, password)


class SystemSettings9021(SystemSettings9020):

    def __init__(self, base_url, username, password):
        super(SystemSettings9021, self).__init__(base_url, username, password)
