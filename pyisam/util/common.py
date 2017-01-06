"""
@copyright: IBM
"""

def add_value_string(dictionary, key, value):
    if value is not None:
        dictionary[key] = str(value)

def add_value_not_empty(dictionary, key, value):
    if value:
        dictionary[key] = value

def add_value(dictionary, key, value):
    if value is not None:
        dictionary[key] = value
