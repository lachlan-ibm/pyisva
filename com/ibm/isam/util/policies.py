"""
@copyright: IBM
"""

import time


ATTRIBUTE = [
    "<AttributeAssignment AttributeId=\"%(attribute_id)s\">",
    "<AttributeDesignator AttributeId=\"%(designator_id)s\" Namespace=\"%(namespace)s\" Source=\"%(source)s\" DataType=\"%(data_type)s\"/>",
    "</AttributeAssignment>"
]
ATTRIBUTE_VALUE = [
    "<AttributeAssignment AttributeId=\"%(attribute_id)s\">",
    "<AttributeValue DataType=\"%(data_type)s\">%(attribute_value)s</AttributeValue>",
    "</AttributeAssignment>"
]
MMFA_AUTHENTICATOR = [
    "<Step id=\"id%(id_a)s\" type=\"Authenticator\">",
    "<Authenticator id=\"id%(id_b)s\" AuthenticatorId=\"urn:ibm:security:authentication:asf:mechanism:mmfa\">",
    "<Parameters>",
    "%(context_message)s",
    "%(mode)s",
    "%(policy_uri)s",
    "%(reauthenticate)s",
    "%(username)s",
    "</Parameters>",
    "</Authenticator>",
    "</Step>"
]
POLICY = [
    "<Policy xmlns=\"urn:ibm:security:authentication:policy:1.0:schema\" PolicyId=\"%(policy_id)s\">",
    "<Description>%(policy_description)s</Description>",
    "%(workflow)s",
    "</Policy>"
]
REQUEST_SCOPE = "urn:ibm:security:asf:scope:request"
SESSION_SCOPE = "urn:ibm:security:asf:scope:session"
USER_PRESENCE_AUTHENTICATOR = [
    "<Step id=\"id%(id_a)s\" type=\"Authenticator\">",
    "<Authenticator id=\"id%(id_b)s\" AuthenticatorId=\"urn:ibm:security:authentication:asf:mechanism:mobile_user_approval:user_presence\">",
    "<Parameters>",
    "%(username)s",
    "</Parameters>",
    "</Authenticator>",
    "</Step>"
]


class PolicyBuilder(object):

    def mmfa_authenticator(self, context_message="", mode="", policy_uri="", reauthenticate="", username=""):
        millis = int(time.time() * 1000)
        id_a = millis
        id_b = millis + 1
        return ''.join(MMFA_AUTHENTICATOR) % locals()

    def user_presence_authenticator(self, username=""):
        millis = int(time.time() * 1000)
        id_a = millis
        id_b = millis + 1
        return ''.join(USER_PRESENCE_AUTHENTICATOR) % locals()

    def policy(self, policy_id, policy_description, workflow):
        return ''.join(POLICY) % locals()

    def request_parameter(self, attribute_id, designator_id, namespace, data_type="String"):
        source = REQUEST_SCOPE
        return ''.join(ATTRIBUTE) % locals()

    def session_parameter(self, attribute_id, designator_id, namespace, data_type="String"):
        source = SESSION_SCOPE
        return ''.join(ATTRIBUTE) % locals()

    def value_parameter(self, attribute_id, attribute_value, data_type="String"):
        return ''.join(ATTRIBUTE_VALUE) % locals()
