"""
@copyright: IBM
"""

import json


class DataObject(object):

    def __init__(self):
        super(DataObject, self).__init__()
        self.data = {}

    def add_value(self, key, value):
        if value is not None:
            self.data[key] = value

    def add_value_not_empty(self, key, value):
        if value:
            self.data[key] = value

    def add_value_string(self, key, value):
        if value is not None:
            self.data[key] = str(value)


class Response(object):

    def __init__(self):
        super(Response, self).__init__()
        self.data = None
        self.json = None
        self.status_code = None
        self.success = None

    def __str__(self):
        return "<Response [%s, %s]>" % (self.success, self.status_code)

    def decode_json(self, data):
        try:
            self.json = json.loads(data)
        except:
            self.json = None
