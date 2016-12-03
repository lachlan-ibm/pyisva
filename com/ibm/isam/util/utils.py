"""
Created on Nov 23, 2016

@copyright: IBM
"""

def addOnStringValue(dictionary, key, value):
    if value is not None:
        dictionary[key] = str(value)

def addOnValue(dictionary, key, value):
    if value is not None:
        dictionary[key] = value
