"""
@copyright: IBM
"""

import logging

from pyisam.util.model import DataObject
from pyisam.util.restclient import RESTClient


PUSH_NOTIFICATION = "/iam/access/v8/push-notification"

logger = logging.getLogger(__name__)


class PushNotification(object):

    def __init__(self, base_url, username, password):
        super(PushNotification, self).__init__()
        self.client = RESTClient(base_url, username, password)

    def create(
            self, app_id=None, platform=None, provider_address=None,
            apple_key_store=None, apple_key_label=None,
            firebase_server_key=None):
        apple = DataObject()
        apple.add_value_string("key_store", apple_key_store)
        apple.add_value_string("key_label", apple_key_label)
        if apple.data:
            apple.add_value_string("provider_address", provider_address)

        firebase = DataObject()
        firebase.add_value_string("server_key", firebase_server_key)
        if firebase.data:
            firebase.add_value_string("provider_address", provider_address)

        provider = DataObject()
        provider.add_value_not_empty("apple", apple.data)
        provider.add_value_not_empty("firebase", firebase.data)

        data = DataObject()
        data.add_value_string("app_id", app_id)
        data.add_value_string("platform", platform)
        data.add_value_not_empty("provider", provider.data)

        response = self.client.post_json(PUSH_NOTIFICATION, data.data)
        response.success = response.status_code == 200

        return response


class PushNotification9021(PushNotification):

    def __init__(self, base_url, username, password):
        super(PushNotification9021, self).__init__(base_url, username, password)

    def create(
            self, app_id=None, platform=None, provider_address=None,
            apple_key_store=None, apple_key_label=None,
            firebase_server_key=None, imc_client_id=None,
            imc_client_secret=None, imc_refresh_token=None, imc_app_key=None):
        apple = DataObject()
        apple.add_value_string("key_store", apple_key_store)
        apple.add_value_string("key_label", apple_key_label)
        if apple.data:
            apple.add_value_string("provider_address", provider_address)

        firebase = DataObject()
        firebase.add_value_string("server_key", firebase_server_key)
        if firebase.data:
            firebase.add_value_string("provider_address", provider_address)

        imc = DataObject()
        imc.add_value_string("client_id", imc_client_id)
        imc.add_value_string("client_secret", imc_client_secret)
        imc.add_value_string("refresh_token", imc_refresh_token)
        imc.add_value_string("app_key", imc_app_key)
        if imc.data:
            imc.add_value_string("provider_address", provider_address)

        provider = DataObject()
        provider.add_value_not_empty("apple", apple.data)
        provider.add_value_not_empty("firebase", firebase.data)
        provider.add_value_not_empty("imc", imc.data)

        data = DataObject()
        data.add_value_string("app_id", app_id)
        data.add_value_string("platform", platform)
        data.add_value_not_empty("provider", provider.data)

        response = self.client.post_json(PUSH_NOTIFICATION, data.data)
        response.success = response.status_code == 200

        return response
