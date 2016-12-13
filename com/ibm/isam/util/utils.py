"""
@copyright: IBM
"""

def add_string_value(dictionary, key, value):
    if value is not None:
        dictionary[key] = str(value)

def add_value(dictionary, key, value):
    if value is not None:
        dictionary[key] = value
